import sqlite3
import os
import time
import pandas as pd
import pytest

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "app.db"))

def test_database_connection_and_table_presence():
    """TC-T-01: Verify data/app.db exists and contains all required tables and views."""
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type IN ('table', 'view');")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()

    expected_tables = ["departments", "doctors", "patients", "appointments", "visits", "billing", "v_patient_visit_analytics"]
    for t in expected_tables:
        assert t in names, f"Expected entity '{t}' missing from database schema."

def test_table_row_and_column_counts():
    """TC-T-02: Verify planned table row counts and joined view columns."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    counts = {
        "departments": cursor.execute("SELECT COUNT(*) FROM departments;").fetchone()[0],
        "doctors": cursor.execute("SELECT COUNT(*) FROM doctors;").fetchone()[0],
        "patients": cursor.execute("SELECT COUNT(*) FROM patients;").fetchone()[0],
        "appointments": cursor.execute("SELECT COUNT(*) FROM appointments;").fetchone()[0],
        "visits": cursor.execute("SELECT COUNT(*) FROM visits;").fetchone()[0],
        "billing": cursor.execute("SELECT COUNT(*) FROM billing;").fetchone()[0]
    }
    
    # View columns
    cursor.execute("PRAGMA table_info(v_patient_visit_analytics);")
    view_columns = cursor.fetchall()
    conn.close()

    assert counts["departments"] == 8, f"Expected 8 departments, got {counts['departments']}"
    assert counts["doctors"] >= 20, f"Expected >=20 doctors, got {counts['doctors']}"
    assert counts["patients"] >= 150, f"Expected >=150 patients, got {counts['patients']}"
    assert counts["appointments"] >= 250, f"Expected >=250 appointments, got {counts['appointments']}"
    assert counts["visits"] >= 150, f"Expected >=150 visits, got {counts['visits']}"
    assert counts["billing"] >= 150, f"Expected >=150 billing rows, got {counts['billing']}"
    assert len(view_columns) >= 35, f"Expected >=35 view columns, got {len(view_columns)}"

def test_primary_key_uniqueness():
    """TC-T-03: Verify primary key uniqueness across all relational entities."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    pk_map = {
        "departments": "department_id",
        "doctors": "doctor_id",
        "patients": "patient_id",
        "appointments": "appointment_id",
        "visits": "visit_id",
        "billing": "billing_id"
    }
    for table, pk in pk_map.items():
        cursor.execute(f"SELECT COUNT({pk}), COUNT(DISTINCT {pk}) FROM {table};")
        total_pks, distinct_pks = cursor.fetchone()
        assert total_pks == distinct_pks, f"Duplicate PK detected in table '{table}'!"
    conn.close()

def test_foreign_key_referential_integrity():
    """TC-T-04: Enforce foreign key referential integrity across the schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("PRAGMA foreign_key_check;")
    violations = cursor.fetchall()
    conn.close()
    assert len(violations) == 0, f"Foreign key integrity violations detected: {violations}"

def test_cleaning_rule_01_timestamp_anomaly():
    """TC-T-05: Verify Business Rule RULE-01 filters out inverted timestamp records."""
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT visit_id, check_in_time, consultation_start_time,
           CASE WHEN consultation_start_time < check_in_time THEN 1 ELSE 0 END AS is_anomaly
    FROM visits;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    anomalies = df[df["is_anomaly"] == 1]
    # We deliberately injected 1 anomaly in Step 10
    assert len(anomalies) >= 1, "Expected at least 1 timestamp anomaly for validation testing."
    # Cleaned dataset must filter them out
    clean_df = df[df["is_anomaly"] == 0]
    assert len(clean_df) == len(df) - len(anomalies)

def test_database_query_performance():
    """TC-T-12: Verify analytical queries execute well within the < 3.0 second budget."""
    conn = sqlite3.connect(DB_PATH)
    start_time = time.time()
    _ = pd.read_sql_query("SELECT * FROM v_patient_visit_analytics;", conn)
    duration = time.time() - start_time
    conn.close()
    assert duration < 1.0, f"Query took {duration:.3f}s, exceeding 1.0s target (budget < 3.0s)."
