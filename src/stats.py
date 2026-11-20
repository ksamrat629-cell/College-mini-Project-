"""
Statistical Methods & Inferential Analysis Module for MetroCare Patient Visit Analytics Platform.
Provides ANOVA, Chi-Square Independence, Pearson Correlation, and Kruskal-Wallis hypothesis tests.
"""

import pandas as pd
import numpy as np
from scipy import stats

def calculate_wait_time_anova(df: pd.DataFrame, group_col: str = "department_name", val_col: str = "wait_time_minutes") -> dict:
    """
    Performs One-Way ANOVA across hospital departments to test for significant differences in wait times.
    """
    if df.empty or group_col not in df.columns or val_col not in df.columns:
        return {"f_stat": 0.0, "p_value": 1.0, "significant": False, "interpretation": "Insufficient data"}

    valid_df = df.dropna(subset=[group_col, val_col])
    groups = [group[val_col].values for _, group in valid_df.groupby(group_col) if len(group) >= 2]
    
    if len(groups) < 2:
        return {"f_stat": 0.0, "p_value": 1.0, "significant": False, "interpretation": "Fewer than 2 valid groups"}

    f_stat, p_val = stats.f_oneway(*groups)
    is_sig = bool(p_val < 0.05)
    
    interpretation = (
        f"Statistically significant difference detected (F={f_stat:.2f}, p={p_val:.4e} < 0.05). "
        "Departmental bottlenecks are structurally uneven across clinics."
        if is_sig else
        f"No statistically significant difference (F={f_stat:.2f}, p={p_val:.4f} >= 0.05)."
    )
    
    return {
        "f_stat": round(float(f_stat), 3),
        "p_value": float(p_val),
        "significant": is_sig,
        "interpretation": interpretation
    }

def calculate_no_show_chi2(appts_df: pd.DataFrame, cat_col1: str = "booking_channel", cat_col2: str = "status") -> dict:
    """
    Performs Chi-Square Test of Independence between booking channel and appointment attendance disposition.
    """
    if appts_df.empty or cat_col1 not in appts_df.columns or cat_col2 not in appts_df.columns:
        return {"chi2": 0.0, "p_value": 1.0, "dof": 0, "significant": False, "interpretation": "Insufficient data"}

    contingency = pd.crosstab(appts_df[cat_col1], appts_df[cat_col2])
    chi2, p_val, dof, _ = stats.chi2_contingency(contingency)
    is_sig = bool(p_val < 0.05)
    
    interpretation = (
        f"Statistically significant association between {cat_col1} and {cat_col2} "
        f"(χ²={chi2:.2f}, p={p_val:.4e}, df={dof}). Booking channel strongly influences no-show risk."
        if is_sig else
        f"No significant association detected (χ²={chi2:.2f}, p={p_val:.4f}, df={dof})."
    )
    
    return {
        "chi2": round(float(chi2), 3),
        "p_value": float(p_val),
        "dof": int(dof),
        "significant": is_sig,
        "contingency_table": contingency,
        "interpretation": interpretation
    }

def calculate_csat_pearson(df: pd.DataFrame, x_col: str = "wait_time_minutes", y_col: str = "csat_score") -> dict:
    """
    Calculates Pearson correlation coefficient and OLS regression between wait times and patient satisfaction (CSAT).
    """
    if df.empty or x_col not in df.columns or y_col not in df.columns:
        return {"r": 0.0, "p_value": 1.0, "slope": 0.0, "intercept": 0.0, "significant": False, "interpretation": "Insufficient data"}

    valid_df = df.dropna(subset=[x_col, y_col])
    if len(valid_df) < 3:
        return {"r": 0.0, "p_value": 1.0, "slope": 0.0, "intercept": 0.0, "significant": False, "interpretation": "Sample size too small"}

    r_val, p_val = stats.pearsonr(valid_df[x_col], valid_df[y_col])
    reg = stats.linregress(valid_df[x_col], valid_df[y_col])
    is_sig = bool(p_val < 0.05)
    
    strength = "Strong" if abs(r_val) >= 0.6 else ("Moderate" if abs(r_val) >= 0.3 else "Weak")
    direction = "Negative (Inverse)" if r_val < 0 else "Positive"
    
    interpretation = (
        f"{strength} {direction} correlation (r={r_val:.3f}, p={p_val:.4e} < 0.05). "
        f"Every 10-minute wait increase reduces CSAT by approximately {abs(reg.slope * 10):.2f} points."
        if is_sig else
        f"Correlation not statistically significant (r={r_val:.3f}, p={p_val:.4f})."
    )
    
    return {
        "r": round(float(r_val), 3),
        "p_value": float(p_val),
        "slope": round(float(reg.slope), 4),
        "intercept": round(float(reg.intercept), 3),
        "r_squared": round(float(r_val ** 2), 3),
        "significant": is_sig,
        "interpretation": interpretation
    }

def calculate_duration_kruskal(df: pd.DataFrame, group_col: str = "visit_type", val_col: str = "consultation_duration_minutes") -> dict:
    """
    Performs Kruskal-Wallis H-test for non-parametric evaluation of skewed consultation durations across visit types.
    """
    if df.empty or group_col not in df.columns or val_col not in df.columns:
        return {"h_stat": 0.0, "p_value": 1.0, "significant": False, "interpretation": "Insufficient data"}

    valid_df = df.dropna(subset=[group_col, val_col])
    groups = [group[val_col].values for _, group in valid_df.groupby(group_col) if len(group) >= 2]
    
    if len(groups) < 2:
        return {"h_stat": 0.0, "p_value": 1.0, "significant": False, "interpretation": "Fewer than 2 valid groups"}

    h_stat, p_val = stats.kruskal(*groups)
    is_sig = bool(p_val < 0.05)
    
    return {
        "h_stat": round(float(h_stat), 3),
        "p_value": float(p_val),
        "significant": is_sig,
        "interpretation": f"Kruskal-Wallis H={h_stat:.2f}, p={p_val:.4e} ({'Significant' if is_sig else 'Not significant'})."
    }
