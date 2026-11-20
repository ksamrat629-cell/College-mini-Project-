"""
Data Cleaner Module for MetroCare Patient Visit Analytics Platform.
Implements Business Rule RULE-01 (timestamp anomaly quarantine), schema validation,
and derived feature computation.
"""

import pandas as pd
import numpy as np

def clean_analytics_data(raw_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Cleans the patient visit analytics dataset:
    1. Parses ISO timestamp strings into pandas datetime objects.
    2. Identifies and isolates RULE-01 anomalies (consultation_start_time < check_in_time).
    3. Validates and recalculates wait times and consultation durations.
    4. Computes binary SLA breach flags (wait_time_minutes > 30.0).
    
    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: (clean_df, anomaly_df)
    """
    df = raw_df.copy()
    
    # Parse datetime columns
    datetime_cols = [
        "check_in_time", "consultation_start_time", "consultation_end_time",
        "appointment_date", "appointment_time", "visit_date", "invoice_date", "payment_date"
    ]
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    
    # Enforce RULE-01: Inverted timestamp detection
    # consultation_start_time must be >= check_in_time
    is_inverted = (df["consultation_start_time"] < df["check_in_time"])
    
    # Check for negative consultation duration if both exist
    is_neg_duration = (df["consultation_end_time"] < df["consultation_start_time"])
    
    anomaly_mask = is_inverted | is_neg_duration
    anomaly_df = df[anomaly_mask].copy()
    if not anomaly_df.empty:
        anomaly_df["quarantine_reason"] = np.where(
            is_inverted[anomaly_mask],
            "RULE-01: consultation_start_time precedes check_in_time",
            "RULE-01: consultation_end_time precedes consultation_start_time"
        )
    
    clean_df = df[~anomaly_mask].copy()
    
    # Recalculate / verify wait time and consultation duration in minutes
    if "consultation_start_time" in clean_df.columns and "check_in_time" in clean_df.columns:
        clean_df["wait_time_minutes"] = (
            (clean_df["consultation_start_time"] - clean_df["check_in_time"]).dt.total_seconds() / 60.0
        ).round(1)
        
    if "consultation_end_time" in clean_df.columns and "consultation_start_time" in clean_df.columns:
        clean_df["consultation_duration_minutes"] = (
            (clean_df["consultation_end_time"] - clean_df["consultation_start_time"]).dt.total_seconds() / 60.0
        ).round(1)
        
    # Recalculate 30-min SLA breach indicator
    if "wait_time_minutes" in clean_df.columns:
        clean_df["is_sla_breach"] = (clean_df["wait_time_minutes"] > 30.0).astype(int)
        
    return clean_df, anomaly_df

def audit_data_quality(df: pd.DataFrame) -> dict:
    """
    Generates summary data quality audit metrics:
    - Total record count
    - Missing values per column
    - Potential duplicate count
    - Anomaly counts
    """
    total_records = len(df)
    missing_counts = df.isnull().sum().to_dict()
    cols_with_missing = {k: v for k, v in missing_counts.items() if v > 0}
    
    # Duplicate check on visit_id or encounter identifiers
    duplicate_count = 0
    if "visit_id" in df.columns:
        duplicate_count = int(df["visit_id"].duplicated().sum())
        
    return {
        "total_records": total_records,
        "cols_with_missing": cols_with_missing,
        "total_missing_cells": int(df.isnull().sum().sum()),
        "duplicate_count": duplicate_count,
        "completeness_score": round((1 - (df.isnull().sum().sum() / (total_records * len(df.columns)))) * 100, 2) if total_records > 0 else 0.0
    }
