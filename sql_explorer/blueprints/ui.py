from flask import Blueprint, make_response, redirect, render_template, request, send_file, url_for

from ..excel_sqlite import excel_to_sqlite_dump, execute_query, extract_schema
from ..store import QueryHistoryItem, get_or_create_session_id, get_session

import io


ui_bp = Blueprint("ui", __name__)


@ui_bp.before_app_request
def ensure_session_cookie():
    session_id = request.cookies.get("sx_session")
    session_id = get_or_create_session_id(session_id)
    request.sx_session_id = session_id  # type: ignore[attr-defined]


@ui_bp.after_app_request
def set_session_cookie(response):
    session_id = getattr(request, "sx_session_id", None)
    if session_id and request.cookies.get("sx_session") != session_id:
        response.set_cookie("sx_session", session_id, httponly=True, samesite="Lax")
    return response


@ui_bp.get("/")
def index():
    sx = get_session(request.sx_session_id)  # type: ignore[attr-defined]
    default_query = ""
    if sx.table_names:
        default_query = f"SELECT * FROM {sx.table_names[0]} LIMIT 10"
    return render_template(
        "index.html",
        has_db=bool(sx.db_dump),
        table_names=sx.table_names,
        schema=sx.schema,
        history=sx.history,
        default_query=default_query,
    )


@ui_bp.get("/download/database.sql")
def download_database_sql():
    sx = get_session(request.sx_session_id)  # type: ignore[attr-defined]
    if not sx.db_dump:
        return redirect(url_for("ui.index"))
    mem = io.BytesIO(sx.db_dump)
    mem.seek(0)
    return send_file(mem, mimetype="application/sql", as_attachment=True, download_name="database.sql")


@ui_bp.post("/upload")
def upload():
    file = request.files.get("file")
    if not file or not file.filename:
        return redirect(url_for("ui.index"))

    sx = get_session(request.sx_session_id)  # type: ignore[attr-defined]
    file_bytes = file.read()
    db_dump, tables = excel_to_sqlite_dump(file_bytes)

    sx.db_dump = db_dump
    sx.table_names = tables
    sx.schema = extract_schema(db_dump)
    sx.history = []

    return redirect(url_for("ui.index"))


@ui_bp.post("/run")
def run_query():
    sx = get_session(request.sx_session_id)  # type: ignore[attr-defined]
    if not sx.db_dump:
        return redirect(url_for("ui.index"))

    sql = (request.form.get("sql") or "").strip()
    if not sql:
        return redirect(url_for("ui.index"))

    try:
        df = execute_query(sql, sx.db_dump)
        item = QueryHistoryItem(
            query=sql,
            error=None,
            columns=list(df.columns),
            rows=df.values.tolist(),
        )
    except Exception as e:  # noqa: BLE001
        item = QueryHistoryItem(query=sql, error=str(e))

    sx.history.insert(0, item)
    return redirect(url_for("ui.index"))


@ui_bp.get("/download/result/<int:idx>.csv")
def download_result_csv(idx: int):
    sx = get_session(request.sx_session_id)  # type: ignore[attr-defined]
    if idx < 0 or idx >= len(sx.history):
        return redirect(url_for("ui.index"))

    item = sx.history[idx]
    if item.error:
        return redirect(url_for("ui.index"))

    out = io.StringIO()
    out.write(",".join([_csv_escape(c) for c in item.columns]) + "\n")
    for row in item.rows:
        out.write(",".join([_csv_escape(v) for v in row]) + "\n")

    mem = io.BytesIO(out.getvalue().encode("utf-8"))
    mem.seek(0)
    return send_file(mem, mimetype="text/csv", as_attachment=True, download_name="query_result.csv")


def _csv_escape(value):
    if value is None:
        s = ""
    else:
        s = str(value)
    if any(ch in s for ch in [",", "\n", "\r", '"']):
        s = '"' + s.replace('"', '""') + '"'
    return s
