import streamlit as st
import pandas as pd
import sqlite3
from io import BytesIO
import io

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="SQL Explorer", layout="wide")

# ----------------------------
# CSS Styling
# ----------------------------
st.markdown("""
<style>
textarea {
    font-family: "Source Code Pro", monospace !important;
    font-size: 14px !important;
    background-color: #0f172a !important;
    color: #e5e7eb !important;
    border-radius: 6px !important;
    border: 1px solid #334155 !important;
}

/* Chat bubbles */
.chat-bubble {
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 18px;
    border: 1px solid #e5e7eb;
}

/* Successful query */
.chat-success {
    background: #f8fafc;
    border: 1px solid #34d399; /* green border */
}

/* Error query */
.chat-error {
    background: #fee2e2; /* light red */
    border: 1px solid #ef4444; /* red border */
}

/* SQL Query display */
.chat-query {
    font-family: monospace;
    font-size: 13px;
    background: #020617;
    color: #e5e7eb;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 10px;
    white-space: pre-wrap;
}

.copy-button {
    margin-top: 4px;
}

.schema-column {
    padding: 6px 0;
    border-bottom: 1px solid #e5e7eb;
}

.schema-name {
    font-weight: 600;
    font-size: 14px;
}

.schema-meta {
    font-size: 12px;
    color: #6b7280;
    margin-top: 2px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Session State
# ----------------------------
if "db_dump" not in st.session_state:
    st.session_state.db_dump = None
if "table_names" not in st.session_state:
    st.session_state.table_names = []
if "current_file" not in st.session_state:
    st.session_state.current_file = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------
# Utility Functions
# ----------------------------
def excel_to_sqlite_dump(uploaded_file):
    excel_file = pd.ExcelFile(BytesIO(uploaded_file.getvalue()))
    conn = sqlite3.connect(":memory:")
    for sheet in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        df.columns = [c.strip().replace(" ", "_") for c in df.columns]
        df.to_sql(sheet, conn, if_exists="replace", index=False)
    dump = "\n".join(conn.iterdump()).encode()
    conn.close()
    return dump, excel_file.sheet_names

def execute_query(sql, db_dump):
    conn = sqlite3.connect(":memory:")
    conn.executescript(db_dump.decode())
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def extract_schema(db_dump):
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

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.header("Database Explorer")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
    if uploaded_file and uploaded_file.name != st.session_state.current_file:
        with st.spinner("Loading Excel..."):
            db_dump, tables = excel_to_sqlite_dump(uploaded_file)
            st.session_state.db_dump = db_dump
            st.session_state.table_names = tables
            st.session_state.current_file = uploaded_file.name
            st.session_state.chat_history = []
        st.success("Database loaded")

    if st.session_state.db_dump:
        st.subheader("Database Structure")
        schema = extract_schema(st.session_state.db_dump)
        for table, cols in schema.items():
            with st.expander(f"📁 {table}", expanded=False):
                for _, name, dtype, notnull, _, _ in cols:
                    st.markdown(f"""
                        <div class="schema-column">
                            <div class="schema-name">{name}</div>
                            <div class="schema-meta">Type: {dtype}</div>
                            <div class="schema-meta">
                                Constraint: {"NOT NULL" if notnull else "NULLABLE"}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

# ----------------------------
# Main Interface
# ----------------------------
st.title("SQL Query Interface")
st.caption("Run SQL queries against your Excel data")

if st.session_state.db_dump:
    default_query = ""
    if st.session_state.table_names:
        default_query = f"SELECT * FROM {st.session_state.table_names[0]} LIMIT 10"

    sql_query = st.text_area("SQL Query", value=default_query, height=120)
    run_query = st.button("Run Query", type="primary")

    if run_query and sql_query.strip():
        try:
            df = execute_query(sql_query.strip(), st.session_state.db_dump)
            st.session_state.chat_history.insert(0, {"query": sql_query.strip(), "result": df, "error": None})
        except Exception as e:
            st.session_state.chat_history.insert(0, {"query": sql_query.strip(), "result": None, "error": str(e)})

    # Display history (newest first)
    for idx, item in enumerate(st.session_state.chat_history):
        bubble_class = "chat-success" if item["error"] is None else "chat-error"
        st.markdown(f"<hr class={bubble_class}'>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-query'>{item['query']}</div>", unsafe_allow_html=True)

        # Show results or error
        if item["error"]:
            st.error(item["error"])
            # Copy button for error
            copy_text = f"Query:\n{item['query']}\n\nError:\n{item['error']}"
        else:
            st.dataframe(item["result"], use_container_width=True)
            copy_text = f"Query:\n{item['query']}\n\nResult:\n{item['result'].to_csv(index=False)}"

        # Copy to clipboard
        btn = st.button("Copy Response", key=f"copy_{idx}")
        if btn:
            st.text_area("Copied Response", value=copy_text, height=200)
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Upload an Excel file from the sidebar to start querying.")
