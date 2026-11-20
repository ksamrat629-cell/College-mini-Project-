"""
Page 1: Executive Overview & Macro Volume Curves
MetroCare Health Systems | Operational Intelligence Platform
US-01, US-10, US-12 | Features F-01, F-10, F-12
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_analytics_view
from src.data_cleaner import clean_analytics_data
from src.analytics import compute_department_throughput, compute_wait_time_sla
from src.stats import calculate_csat_pearson
from src.ui import render_tailwind_header, render_kpi_grid, render_insight_box, apply_plotly_theme

st.set_page_config(page_title="Executive Overview | MetroCare", page_icon="🏥", layout="wide")

# Header
render_tailwind_header(
    title="Executive Overview & Arrival Curves",
    subtitle="Macro hospital volume, 24-hour peak arrival surges, and CSAT patient satisfaction dynamics",
    badge_text="Executive Dashboard",
    badge_color="bg-blue-100 text-blue-800"
)

# Load data
raw_df = load_analytics_view()
clean_df, _ = clean_analytics_data(raw_df)

# Sidebar filters with session state persistence
st.sidebar.markdown("### 🎛️ Operational Filters")
all_depts = sorted(clean_df["department_name"].dropna().unique().tolist())
selected_depts = st.sidebar.multiselect(
    "Filter Departments",
    options=all_depts,
    default=st.session_state.get("selected_departments", all_depts)
)
st.session_state["selected_departments"] = selected_depts if selected_depts else all_depts

# Filter dataset
filtered_df = clean_df[clean_df["department_name"].isin(st.session_state["selected_departments"])].copy()

# Compute KPI metrics
wait_metrics = compute_wait_time_sla(filtered_df)
mean_csat = filtered_df["csat_score"].dropna().mean() if "csat_score" in filtered_df.columns else 0.0

kpis = [
    {
        "title": "Hospital Throughput",
        "value": f"{len(filtered_df):,}",
        "subtext": f"{len(st.session_state['selected_departments'])} OPD Departments",
        "badge_text": "Volume",
        "badge_color": "bg-blue-100 text-blue-800"
    },
    {
        "title": "Average Wait Time",
        "value": f"{wait_metrics['mean_wait']:.1f} Mins",
        "subtext": f"Median: {wait_metrics['median_wait']:.1f} Mins",
        "badge_text": "Breach" if wait_metrics['mean_wait'] > 30 else "Compliant",
        "badge_color": "bg-red-100 text-red-800" if wait_metrics['mean_wait'] > 30 else "bg-emerald-100 text-emerald-800"
    },
    {
        "title": "SLA Breach Rate",
        "value": f"{wait_metrics['breach_rate']:.1f}%",
        "subtext": f"{wait_metrics['breach_count']} of {wait_metrics['total_encounters']} > 30 mins",
        "badge_text": "High" if wait_metrics['breach_rate'] > 35 else "Normal",
        "badge_color": "bg-red-100 text-red-800" if wait_metrics['breach_rate'] > 35 else "bg-emerald-100 text-emerald-800"
    },
    {
        "title": "Patient Satisfaction",
        "value": f"{mean_csat:.2f} / 5.0",
        "subtext": "CSAT Quality Benchmark: ≥ 4.0",
        "badge_text": "Sub-optimal" if mean_csat < 4.0 else "Satisfactory",
        "badge_color": "bg-amber-100 text-amber-800" if mean_csat < 4.0 else "bg-emerald-100 text-emerald-800"
    }
]
render_kpi_grid(kpis)

# Hourly Arrival Surges
filtered_df["arrival_hour"] = filtered_df["check_in_time"].dt.hour
hourly_counts = filtered_df.groupby("arrival_hour")["visit_id"].count().reset_index()
hourly_counts.columns = ["Hour", "Visits"]

# Ensure all 24 hours are represented
full_hours = pd.DataFrame({"Hour": list(range(24))})
hourly_counts = full_hours.merge(hourly_counts, on="Hour", how="left").fillna(0)
hourly_counts["Is_Peak"] = hourly_counts["Hour"].isin([9, 10, 11])

# Layout: 2 Columns for Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ⏰ 24-Hour Patient Arrival Volume & Morning Surge")
    fig_hourly = go.Figure()
    
    # Non-peak bars
    fig_hourly.add_trace(go.Bar(
        x=hourly_counts[~hourly_counts["Is_Peak"]]["Hour"],
        y=hourly_counts[~hourly_counts["Is_Peak"]]["Visits"],
        name="Standard Arrival",
        marker_color="#2B6CB0"
    ))
    # Peak surge bars (9-11 AM)
    fig_hourly.add_trace(go.Bar(
        x=hourly_counts[hourly_counts["Is_Peak"]]["Hour"],
        y=hourly_counts[hourly_counts["Is_Peak"]]["Visits"],
        name="Peak Surge (09:00–11:30)",
        marker_color="#E53E3E"
    ))
    
    peak_threshold = hourly_counts["Visits"].quantile(0.85)
    fig_hourly.add_hline(
        y=peak_threshold,
        line_dash="dash",
        line_color="#E53E3E",
        annotation_text="Surge Threshold",
        annotation_position="top right"
    )
    
    apply_plotly_theme(fig_hourly, height=380)
    st.plotly_chart(fig_hourly, use_container_width=True)

with col2:
    st.markdown("#### 📉 CSAT Score vs. Queue Wait Time (OLS Trend)")
    csat_stat = calculate_csat_pearson(filtered_df)
    
    fig_csat = px.scatter(
        filtered_df.dropna(subset=["wait_time_minutes", "csat_score"]),
        x="wait_time_minutes",
        y="csat_score",
        color="department_name",
        trendline="ols",
        trendline_color_override="#1E293B",
        labels={"wait_time_minutes": "Wait Time (Minutes)", "csat_score": "CSAT Score (1 to 5)", "department_name": "Department"},
        opacity=0.75
    )
    apply_plotly_theme(fig_csat, height=380)
    fig_csat.update_layout(
        xaxis=dict(title="Patient Wait Time (Minutes)"),
        yaxis=dict(title="CSAT Score (1 to 5)", range=[0.5, 5.5]),
        legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_csat, use_container_width=True)

# Statistical Insight
render_insight_box(
    title=f"Statistical Correlation Analysis (Pearson r = {csat_stat['r']:.3f}, R² = {csat_stat.get('r_squared', 0.0):.3f})",
    text=csat_stat["interpretation"],
    category="Danger" if csat_stat["r"] < -0.5 else "Info"
)

# Department Throughput Breakdown
st.markdown("#### 🏢 Departmental Operational & Financial Throughput")
dept_summary = compute_department_throughput(filtered_df)
st.dataframe(
    dept_summary.style.format({
        "total_visits": "{:,}",
        "mean_wait_time": "{:.1f} m",
        "median_wait_time": "{:.1f} m",
        "sla_breach_count": "{:,}",
        "sla_breach_rate_pct": "{:.1f}%",
        "total_revenue": "₹{:,.2f}"
    }),
    use_container_width=True,
    hide_index=True
)

# Operational Exception Alert Table (Long waits or severe dissatisfaction)
st.markdown("#### ⚠️ Operational Exception Incidents (Wait > 45m or CSAT ≤ 2)")
exceptions = filtered_df[
    (filtered_df["wait_time_minutes"] > 45) | (filtered_df["csat_score"] <= 2)
][["visit_id", "patient_id", "department_name", "doctor_name", "check_in_time", "wait_time_minutes", "csat_score"]].sort_values("wait_time_minutes", ascending=False)

if not exceptions.empty:
    st.dataframe(
        exceptions.head(10).style.format({
            "wait_time_minutes": "{:.1f} mins",
            "csat_score": "{:.0f} / 5"
        }),
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("No critical operational exceptions detected in the selected cohort.")
