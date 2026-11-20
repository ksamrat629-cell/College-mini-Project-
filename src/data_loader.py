"""
Data Loader Module for MetroCare Patient Visit Analytics Platform.
Handles SQLite connection, query execution, and Streamlit caching via @st.cache_data.
"""

import os
import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "app.db"))

def get_connection(read_only: bool = True) -> sqlite3.Connection:
    """Return an SQLite connection. Uses read-only URI mode when specified."""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}")
    
    if read_only:
        # Use URI connection for read-only access to prevent inadvertent writes
        uri = f"file:{DB_PATH}?mode=ro"
        try:
            return sqlite3.connect(uri, uri=True)
        except sqlite3.OperationalError:
            return sqlite3.connect(DB_PATH)
    return sqlite3.connect(DB_PATH)

@st.cache_data(ttl=3600, show_spinner="Loading hospital encounter records...")
def load_analytics_view() -> pd.DataFrame:
    """Load the full joined view v_patient_visit_analytics from SQLite."""
    conn = get_connection(read_only=True)
    try:
        df = pd.read_sql_query("SELECT * FROM v_patient_visit_analytics;", conn)
    finally:
        conn.close()
    return df

@st.cache_data(ttl=3600)
def load_table(table_name: str) -> pd.DataFrame:
    """Load any individual master or fact table from the database."""
    valid_tables = {"departments", "doctors", "patients", "appointments", "visits", "billing"}
    if table_name not in valid_tables:
        raise ValueError(f"Table '{table_name}' is not an authorized database entity.")
    conn = get_connection(read_only=True)
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
    finally:
        conn.close()
    return df

@st.cache_data(ttl=3600)
def load_all_tables() -> dict[str, pd.DataFrame]:
    """Load all 6 database tables as a dictionary of DataFrames."""
    return {
        "departments": load_table("departments"),
        "doctors": load_table("doctors"),
        "patients": load_table("patients"),
        "appointments": load_table("appointments"),
        "visits": load_table("visits"),
        "billing": load_table("billing")
    }
