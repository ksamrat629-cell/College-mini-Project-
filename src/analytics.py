"""
Analytics & Aggregations Module for MetroCare Patient Visit Analytics Platform.
Implements core business formulas, KPI metrics, capacity analysis, and financial simulations.
"""

import pandas as pd
import numpy as np

def compute_department_throughput(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes volume, wait times, SLA breaches, and financial realization by department.
    """
    if df.empty or "department_name" not in df.columns:
        return pd.DataFrame()

    rev_col = None
    for cand in ["net_billed_amount", "final_amount", "gross_billed_amount", "total_bill_amount"]:
        if cand in df.columns:
            rev_col = cand
            break

    agg_dict = {
        "visit_id": "count",
        "wait_time_minutes": ["mean", "median"],
        "is_sla_breach": ["sum", lambda x: (x.sum() / len(x) * 100.0) if len(x) > 0 else 0.0]
    }
    cols = ["total_visits", "mean_wait_time", "median_wait_time", "sla_breach_count", "sla_breach_rate_pct"]
    
    if rev_col:
        agg_dict[rev_col] = "sum"
        cols.append("total_revenue")

    grouped = df.groupby("department_name").agg(agg_dict)
    grouped.columns = cols
    grouped["mean_wait_time"] = grouped["mean_wait_time"].round(1)
    grouped["median_wait_time"] = grouped["median_wait_time"].round(1)
    grouped["sla_breach_rate_pct"] = grouped["sla_breach_rate_pct"].round(1)
    if "total_revenue" in grouped.columns:
        grouped["total_revenue"] = grouped["total_revenue"].round(2)
        
    return grouped.reset_index().sort_values("total_visits", ascending=False)

def compute_wait_time_sla(df: pd.DataFrame, threshold: float = 30.0) -> dict:
    """
    Computes macro wait time distribution metrics and SLA breach rates.
    """
    if df.empty or "wait_time_minutes" not in df.columns:
        return {
            "total_encounters": 0, "mean_wait": 0.0, "median_wait": 0.0,
            "p90_wait": 0.0, "p95_wait": 0.0, "breach_count": 0, "breach_rate": 0.0
        }
        
    waits = df["wait_time_minutes"].dropna()
    total = len(waits)
    if total == 0:
        return {
            "total_encounters": 0, "mean_wait": 0.0, "median_wait": 0.0,
            "p90_wait": 0.0, "p95_wait": 0.0, "breach_count": 0, "breach_rate": 0.0
        }
        
    breaches = (waits > threshold).sum()
    return {
        "total_encounters": total,
        "mean_wait": round(float(waits.mean()), 1),
        "median_wait": round(float(waits.median()), 1),
        "p90_wait": round(float(np.percentile(waits, 90)), 1),
        "p95_wait": round(float(np.percentile(waits, 95)), 1),
        "breach_count": int(breaches),
        "breach_rate": round(float(breaches / total * 100.0), 1)
    }

def compute_no_show_matrix(appts_df: pd.DataFrame) -> dict:
    """
    Computes appointment fulfillment, no-show rate, and channel patterns.
    """
    status_col = "appointment_status" if "appointment_status" in appts_df.columns else ("status" if "status" in appts_df.columns else None)
    if appts_df.empty or status_col is None:
        return {
            "total_appointments": 0, "completed": 0, "no_shows": 0,
            "cancelled": 0, "unfulfilled": 0, "no_show_rate": 0.0, "pure_no_show_rate": 0.0
        }

    total = len(appts_df)
    completed = int((appts_df[status_col] == "Completed").sum())
    no_shows = int((appts_df[status_col] == "No-Show").sum())
    cancelled = int((appts_df[status_col] == "Cancelled").sum())
    unfulfilled = no_shows + cancelled
    no_show_rate = round(float(unfulfilled / total * 100.0), 1) if total > 0 else 0.0

    return {
        "total_appointments": total,
        "completed": completed,
        "no_shows": no_shows,
        "cancelled": cancelled,
        "unfulfilled": unfulfilled,
        "no_show_rate": no_show_rate,
        "pure_no_show_rate": round(float(no_shows / total * 100.0), 1) if total > 0 else 0.0
    }

def compute_consultation_duration(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes consultation duration statistics across visit types.
    """
    if df.empty or "consultation_duration_minutes" not in df.columns:
        return pd.DataFrame()
        
    grouped = df.groupby("visit_type")["consultation_duration_minutes"].agg(
        total_visits="count",
        mean_duration="mean",
        median_duration="median",
        min_duration="min",
        max_duration="max",
        std_duration="std"
    ).round(1).reset_index()
    
    return grouped

def compute_readmission_rate(df: pd.DataFrame, window_days: int = 30) -> dict:
    """
    Calculates 30-day unplanned hospital readmission rate using encounter chronology.
    Excludes scheduled routine follow-ups.
    """
    if df.empty or "patient_id" not in df.columns or "visit_date" not in df.columns:
        return {"total_patients": 0, "readmission_count": 0, "readmission_rate": 0.0}

    temp = df.copy()
    temp["visit_date"] = pd.to_datetime(temp["visit_date"])
    temp = temp.sort_values(["patient_id", "visit_date"])
    
    # Calculate days since prior visit for same patient
    temp["days_since_prior"] = temp.groupby("patient_id")["visit_date"].diff().dt.days
    
    # Unplanned readmission: 1-30 days, not a scheduled Follow-up
    is_readmit = (
        (temp["days_since_prior"] > 0) & 
        (temp["days_since_prior"] <= window_days) & 
        (temp["visit_type"] != "Follow-up")
    )
    
    readmit_count = int(is_readmit.sum())
    total_encounters = len(temp)
    rate = round(float(readmit_count / total_encounters * 100.0), 1) if total_encounters > 0 else 0.0
    
    return {
        "total_encounters": total_encounters,
        "readmission_count": readmit_count,
        "readmission_rate": rate,
        "readmitted_patient_ids": temp[is_readmit]["patient_id"].unique().tolist()
    }

def compute_revenue_payer_mix(df: pd.DataFrame) -> dict:
    """
    Computes financial metrics: gross billing, discounts, net realized, and payer distribution.
    """
    if df.empty:
        return {"gross_revenue": 0.0, "net_revenue": 0.0, "discount_total": 0.0, "avg_rev_per_visit": 0.0, "payer_df": pd.DataFrame()}
        
    gross_col = "gross_billed_amount" if "gross_billed_amount" in df.columns else ("total_bill_amount" if "total_bill_amount" in df.columns else None)
    net_col = "net_billed_amount" if "net_billed_amount" in df.columns else ("final_amount" if "final_amount" in df.columns else None)
    payer_col = "payer_type" if "payer_type" in df.columns else ("payer_category" if "payer_category" in df.columns else None)

    gross = float(df[gross_col].sum()) if gross_col else 0.0
    discounts = float(df["discount_amount"].sum()) if "discount_amount" in df.columns else 0.0
    net = float(df[net_col].sum()) if net_col else (gross - discounts)
    total_visits = len(df)
    avg_rev = round(net / total_visits, 2) if total_visits > 0 else 0.0
    
    payer_summary = pd.DataFrame()
    if payer_col:
        amt_col = net_col if net_col else gross_col
        if amt_col:
            payer_summary = df.groupby(payer_col).agg(
                encounters=("visit_id", "count"),
                total_amount=(amt_col, "sum")
            ).reset_index()
            total_payer_amt = payer_summary["total_amount"].sum()
            payer_summary["percentage"] = (payer_summary["total_amount"] / total_payer_amt * 100.0).round(1) if total_payer_amt > 0 else 0.0
            payer_summary["total_amount"] = payer_summary["total_amount"].round(2)
        
    return {
        "gross_revenue": round(gross, 2),
        "discount_total": round(discounts, 2),
        "net_revenue": round(net, 2),
        "avg_rev_per_visit": avg_rev,
        "payer_df": payer_summary
    }

def compute_doctor_utilization(df: pd.DataFrame, scheduled_hours_per_day: float = 8.0) -> pd.DataFrame:
    """
    Computes doctor capacity utilization based on delivered consultation minutes vs scheduled time.
    """
    if df.empty or "doctor_name" not in df.columns or "consultation_duration_minutes" not in df.columns:
        return pd.DataFrame()
        
    # Estimate working days in period or default to 5-day schedule
    total_delivered = df.groupby(["doctor_name", "department_name"])["consultation_duration_minutes"].agg(
        encounters="count",
        consult_minutes="sum"
    ).reset_index()
    
    # Standard benchmark: 5 scheduled days * 8 hours = 40 hours = 2400 minutes
    scheduled_minutes = 5.0 * scheduled_hours_per_day * 60.0
    total_delivered["scheduled_minutes"] = scheduled_minutes
    total_delivered["utilization_pct"] = (
        (total_delivered["consult_minutes"] / scheduled_minutes) * 100.0
    ).round(1)
    
    # Classify status
    conditions = [
        total_delivered["utilization_pct"] > 95.0,
        total_delivered["utilization_pct"] < 50.0
    ]
    choices = ["Overutilized (Burnout Risk)", "Underutilized (Excess Capacity)"]
    total_delivered["status"] = np.select(conditions, choices, default="Optimal Utilization")
    
    return total_delivered.sort_values("utilization_pct", ascending=False)

def simulate_no_show_recovery(unfulfilled_count: int, avg_revenue_per_visit: float, recovery_pct: float) -> dict:
    """
    Calculates recovered revenue and appointments from no-show mitigation.
    """
    recovered_slots = int(round(unfulfilled_count * (recovery_pct / 100.0)))
    recovered_revenue = round(recovered_slots * avg_revenue_per_visit, 2)
    return {
        "recovery_pct": recovery_pct,
        "recovered_slots": recovered_slots,
        "recovered_revenue": recovered_revenue
    }
