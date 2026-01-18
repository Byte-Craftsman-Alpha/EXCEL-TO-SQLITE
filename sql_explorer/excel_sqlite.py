from io import BytesIO
from typing import Dict, List, Tuple

import pandas as pd
import sqlite3


def excel_to_sqlite_dump(file_bytes: bytes) -> Tuple[bytes, List[str]]:
    excel_file = pd.ExcelFile(BytesIO(file_bytes))
    conn = sqlite3.connect(":memory:")
    for sheet in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        df.columns = [c.strip().replace(" ", "_") for c in df.columns]
        df.to_sql(sheet, conn, if_exists="replace", index=False)
    dump = "\n".join(conn.iterdump()).encode()
    conn.close()
    return dump, excel_file.sheet_names


def extract_schema(db_dump: bytes) -> Dict[str, list]:
    conn = sqlite3.connect(":memory:")
    conn.executescript(db_dump.decode())
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    schema = {}
    for t in tables:
        cur.execute(f"PRAGMA table_info({t})")
        schema[t] = cur.fetchall()
    conn.close()
    return schema


def execute_query(sql: str, db_dump: bytes):
    conn = sqlite3.connect(":memory:")
    conn.executescript(db_dump.decode())
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df
