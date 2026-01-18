from flask import Blueprint, jsonify, request

from ..store import get_session


api_bp = Blueprint("api", __name__)


@api_bp.get("/schema")
def schema():
    session_id = request.cookies.get("sx_session")
    if not session_id:
        return jsonify({"tables": []})

    sx = get_session(session_id)
    return jsonify({"tables": sx.table_names, "schema": sx.schema})
