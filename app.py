import streamlit as st
import pandas as pd
import sqlite3
from io import BytesIO

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="Excel to SQL Explorer",
    layout="wide"
)

# ------------------------------------------------------------
# Session State Initialization
# ------------------------------------------------------------
if "db_dump" not in st.session_state:
    st.session_state.db_dump = None

if "table_names" not in st.session_state:
    st.session_state.table_names = []

if "query_history" not in st.session_state:
    st.session_state.query_history = []

if "current_file" not in st.session_state:
    st.session_state.current_file = None

if "pasted_query" not in st.session_state:
    st.session_state.pasted_query = ""

# ------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------
def excel_to_sqlite_dump(uploaded_file):
    """
    Converts an Excel file into a serialized SQLite database dump.
    """
    bytes_data = uploaded_file.getvalue()
    excel_file = pd.ExcelFile(BytesIO(bytes_data))

    conn = sqlite3.connect(":memory:")

    for sheet in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet)
        df.columns = [
            c.strip().replace(" ", "_").replace("-", "_")
            for c in df.columns
        ]
        df.to_sql(sheet, conn, if_exists="replace", index=False)

    dump_buffer = BytesIO()
    for line in conn.iterdump():
        dump_buffer.write(f"{line}\n".encode())

    conn.close()

    return dump_buffer.getvalue(), excel_file.sheet_names


def execute_query(sql, db_dump):
    """
    Executes a SQL query against a fresh SQLite connection.
    """
    conn = sqlite3.connect(":memory:")
    conn.executescript(db_dump.decode())
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

# ------------------------------------------------------------
# Sidebar UI
# ------------------------------------------------------------
with st.sidebar:
    st.header("Database Explorer")

    uploaded_file = st.file_uploader(
        "Upload Excel File",
        type=["xlsx", "xls"]
    )

    if uploaded_file:
        if uploaded_file.name != st.session_state.current_file:
            with st.spinner("Loading Excel into SQLite..."):
                db_dump, tables = excel_to_sqlite_dump(uploaded_file)

                st.session_state.db_dump = db_dump
                st.session_state.table_names = tables
                st.session_state.current_file = uploaded_file.name
                st.session_state.query_history = []
                st.session_state.pasted_query = ""

            st.success("Database loaded successfully")

    st.divider()

    if st.session_state.db_dump:
        st.subheader("Database Info")
        st.caption(f"File: {st.session_state.current_file}")

        st.write("Tables:")
        for t in st.session_state.table_names:
            st.markdown(f"- `{t}`")

        st.divider()

        st.subheader("Query History")
        if not st.session_state.query_history:
            st.caption("No queries executed yet.")
        else:
            for i, q in enumerate(reversed(st.session_state.query_history)):
                with st.expander(f"Query #{len(st.session_state.query_history) - i}"):
                    st.code(q, language="sql")
                    if st.button("Load to Editor", key=f"hist_{i}"):
                        st.session_state.pasted_query = q
                        st.rerun()

    else:
        st.info("Upload an Excel file to begin.")

# ------------------------------------------------------------
# Main UI
# ------------------------------------------------------------
st.title("SQL Query Interface")
st.caption("Run SQL queries directly against your Excel data")

if st.session_state.db_dump:
    default_query = (
        st.session_state.pasted_query
        if st.session_state.pasted_query
        else f"SELECT * FROM {st.session_state.table_names[0]} LIMIT 10"
    )

    col1, col2 = st.columns([4, 1])

    with col1:
        sql_query = st.text_area(
            "SQL Query",
            value=default_query,
            height=120
        )

    with col2:
        st.write("")
        st.write("")
        run_query = st.button(
            "Run Query",
            type="primary",
            use_container_width=True
        )

    if run_query:
        if not sql_query.strip():
            st.warning("Please enter a SQL query.")
        else:
            if (
                not st.session_state.query_history
                or sql_query.strip() != st.session_state.query_history[-1]
            ):
                st.session_state.query_history.append(sql_query.strip())

            try:
                result_df = execute_query(
                    sql_query,
                    st.session_state.db_dump
                )

                st.subheader("Results")
                st.dataframe(result_df, use_container_width=True)
                st.caption(
                    f"Returned {len(result_df)} rows "
                    f"and {len(result_df.columns)} columns."
                )

            except Exception as e:
                st.error(f"SQL Error: {e}")

else:
    st.info("Upload an Excel file from the sidebar to start querying.")
