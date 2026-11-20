import numpy as np
import pandas as pd
from scipy import stats
import pytest

def test_wait_time_and_sla_breach_calculation_on_known_dataset():
    """TC-T-06: Mathematical verification of wait time and SLA breach calculation on a known tiny dataset."""
    sample_data = pd.DataFrame({
        "visit_id": [1, 2, 3, 4, 5],
        "wait_time_minutes": [12, 28, 35, 45, 60]
    })
    # Business Rule: SLA Breach if wait_time > 30 minutes
    sample_data["is_sla_breach"] = (sample_data["wait_time_minutes"] > 30).astype(int)
    
    mean_wait = sample_data["wait_time_minutes"].mean()
    breach_count = sample_data["is_sla_breach"].sum()
    breach_rate = (breach_count / len(sample_data)) * 100

    assert mean_wait == 36.0, f"Expected mean wait 36.0, got {mean_wait}"
    assert breach_count == 3, f"Expected 3 breaches, got {breach_count}"
    assert breach_rate == 60.0, f"Expected breach rate 60.0%, got {breach_rate}%"

def test_no_show_rate_calculation_on_known_dataset():
    """TC-T-07: Mathematical verification of appointment no-show formula on known dataset."""
    sample_appts = pd.DataFrame({
        "appointment_id": list(range(1, 11)),
        "status": ["Completed", "Completed", "No-Show", "Completed", "Cancelled", 
                   "Completed", "No-Show", "Completed", "Completed", "Completed"]
    })
    unfulfilled = sample_appts["status"].isin(["No-Show", "Cancelled"]).sum()
    no_show_rate = (unfulfilled / len(sample_appts)) * 100
    assert unfulfilled == 3
    assert no_show_rate == 30.0

def test_doctor_utilization_formula_on_known_dataset():
    """TC-T-08: Mathematical verification of doctor capacity utilization formula."""
    scheduled_hours = 8.0
    scheduled_minutes = scheduled_hours * 60.0 # 480 minutes
    actual_consultation_minutes = [25, 30, 20, 35, 40, 30, 25, 35, 40, 45, 35] # sum = 360 mins
    total_delivered = sum(actual_consultation_minutes)
    
    utilization_pct = (total_delivered / scheduled_minutes) * 100.0
    assert total_delivered == 360
    assert utilization_pct == 75.0

def test_30day_readmission_calculation_on_known_dataset():
    """TC-T-09: Mathematical verification of 30-day unplanned readmission window."""
    patient_visits = pd.DataFrame({
        "patient_id": [101, 101, 101],
        "visit_date": pd.to_datetime(["2026-01-01", "2026-01-14", "2026-03-20"]),
        "visit_type": ["First Consultation", "Emergency Triage", "First Consultation"]
    }).sort_values("visit_date")

    patient_visits["days_since_prior"] = patient_visits["visit_date"].diff().dt.days
    patient_visits["is_readmit"] = (
        (patient_visits["days_since_prior"] > 0) & 
        (patient_visits["days_since_prior"] <= 30) & 
        (patient_visits["visit_type"] != "Follow-up")
    ).astype(int)

    results = patient_visits["is_readmit"].tolist()
    assert results == [0, 1, 0], f"Expected readmission sequence [0, 1, 0], got {results}"

def test_statistical_anova_and_correlation_functions():
    """TC-T-10: Verification of SciPy ANOVA and Pearson correlation statistical methods."""
    # Group A (Cardiology ~40m wait), Group B (ENT ~20m wait)
    np.random.seed(42)
    group_a = np.random.normal(40, 5, 30)
    group_b = np.random.normal(20, 4, 30)
    
    f_stat, p_val = stats.f_oneway(group_a, group_b)
    assert f_stat > 10.0, "Expected significant F-statistic between distinct department wait times."
    assert p_val < 0.001, f"Expected p-value < 0.001, got {p_val}"

    # Pearson correlation between wait times and CSAT (inverse relationship)
    wait_times = np.array([10, 15, 20, 30, 45, 60, 75, 90])
    csat_scores = np.array([5, 5, 4, 4, 3, 2, 1, 1])
    r_val, p_corr = stats.pearsonr(wait_times, csat_scores)
    assert r_val < -0.85, f"Expected strong negative correlation, got {r_val}"
    assert p_corr < 0.01, f"Expected significant correlation p-value, got {p_corr}"
