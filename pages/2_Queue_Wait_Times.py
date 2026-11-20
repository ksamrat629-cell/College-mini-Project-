"""
Page 2: Queue Dynamics & 30-Minute Wait SLA Benchmark
MetroCare Health Systems | Operational Intelligence Platform
US-03, US-04, US-12 | Features F-03, F-04, F-12
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_analytics_view
from src.data_cleaner import clean_analytics_data
from src.analytics import compute_wait_time_sla, compute_consultation_duration
from src.stats import calculate_wait_time_anova, calculate_duration_kruskal
from src.ui import render_tailwind_header, render_kpi_grid, render_insight_box

st.set_page_config(page_title="Queue Dynamics | MetroCare", page_icon="⏱️", layout="wide")

# Header
render_tailwind_header(
    title="Queue Dynamics & 30-Minute Wait SLA Benchmark",
    subtitle="Patient wait time distributions, SLA breach monitoring, and clinical consultation durations",
    badge_text="Operational SLA Monitor",
    badge_color="bg-amber-100 text-amber-800"
)

# Load data
raw_df = load_analytics_view()
clean_df, _ = clean_analytics_data(raw_df)

# Sidebar filters with session state persistence
st.sidebar.markdown("### 🎛️ Queue SLA Filters")
all_depts = sorted(clean_df["department_name"].dropna().unique().tolist())
selected_depts = st.sidebar.multiselect(
    "Filter Departments",
    options=all_depts,
    default=st.session_state.get("selected_departments", all_depts)
)
st.session_state["selected_departments"] = selected_depts if selected_depts else all_depts

all_vtypes = sorted(clean_df["visit_type"].dropna().unique().tolist())
selected_vtypes = st.sidebar.multiselect(
    "Filter Visit Types",
    options=all_vtypes,
    default=st.session_state.get("selected_visit_types", all_vtypes)
)
st.session_state["selected_visit_types"] = selected_vtypes if selected_vtypes else all_vtypes

# Filter dataset
filtered_df = clean_df[
    (clean_df["department_name"].isin(st.session_state["selected_departments"])) &
    (clean_df["visit_type"].isin(st.session_state["selected_visit_types"]))
].copy()

# Compute KPI metrics
wait_metrics = compute_wait_time_sla(filtered_df, threshold=30.0)

kpis = [
    {
        "title": "Mean Wait Time",
        "value": f"{wait_metrics['mean_wait']:.1f} Mins",
        "subtext": "SLA Benchmark: 30.0 Mins",
        "badge_text": "Breach" if wait_metrics['mean_wait'] > 30 else "Compliant",
        "badge_color": "bg-red-100 text-red-800" if wait_metrics['mean_wait'] > 30 else "bg-emerald-100 text-emerald-800"
    },
    {
        "title": "Median Wait Time",
        "value": f"{wait_metrics['median_wait']:.1f} Mins",
        "subtext": "50% of Patients Wait Below",
        "badge_text": "P50 Metric",
        "badge_color": "bg-blue-100 text-blue-800"
    },
    {
        "title": "90th Percentile Wait",
        "value": f"{wait_metrics['p90_wait']:.1f} Mins",
        "subtext": "Severe Wait Tail (P90)",
        "badge_text": "Tail Risk",
        "badge_color": "bg-purple-100 text-purple-800"
    },
    {
        "title": "SLA Breach Rate",
        "value": f"{wait_metrics['breach_rate']:.1f}%",
        "subtext": f"{wait_metrics['breach_count']} of {wait_metrics['total_encounters']} > 30 mins",
        "badge_text": "High" if wait_metrics['breach_rate'] > 35 else "Normal",
        "badge_color": "bg-red-100 text-red-800" if wait_metrics['breach_rate'] > 35 else "bg-emerald-100 text-emerald-800"
    }
]
render_kpi_grid(kpis)

# Layout: 2 Columns for Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📊 Departmental Wait Times vs. 30-Minute SLA Benchmark")
    dept_waits = filtered_df.groupby("department_name")["wait_time_minutes"].agg(["mean", "count"]).reset_index()
    dept_waits.columns = ["department_name", "mean_wait", "encounters"]
    dept_waits = dept_waits.sort_values("mean_wait", ascending=True)
    dept_waits["status"] = np.where(dept_waits["mean_wait"] > 30.0, "Breaching SLA (>30m)", "Compliant (≤30m)")
    dept_waits["color"] = np.where(dept_waits["mean_wait"] > 30.0, "#E53E3E", "#10B981")
    
    fig_dept = go.Figure()
    for status_label, color_code in [("Compliant (≤30m)", "#10B981"), ("Breaching SLA (>30m)", "#E53E3E")]:
        subset = dept_waits[dept_waits["status"] == status_label]
        if not subset.empty:
            fig_dept.add_trace(go.Bar(
                y=subset["department_name"],
                x=subset["mean_wait"],
                name=status_label,
                orientation="h",
                marker_color=color_code,
                text=[f"{v:.1f}m" for v in subset["mean_wait"]],
                textposition="auto"
            ))
            
    fig_dept.add_vline(
        x=30.0,
        line_dash="dash",
        line_color="#E53E3E",
        annotation_text="30-Min SLA Benchmark",
        annotation_position="top right"
    )
    
    fig_dept.update_layout(
        xaxis=dict(title="Average Patient Wait Time (Minutes)"),
        yaxis=dict(title="Department"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=30, b=20),
        height=390
    )
    st.plotly_chart(fig_dept, use_container_width=True)

with col2:
    st.markdown("#### 📦 Clinical Consultation Duration by Visit Type")
    fig_box = px.box(
        filtered_df,
        x="visit_type",
        y="consultation_duration_minutes",
        color="visit_type",
        points="outliers",
        labels={"visit_type": "Visit Type", "consultation_duration_minutes": "Consultation Duration (Mins)"}
    )
    fig_box.update_layout(
        xaxis=dict(title="Clinical Visit Nature"),
        yaxis=dict(title="Consultation Duration (Minutes)"),
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=20),
        height=390
    )
    st.plotly_chart(fig_box, use_container_width=True)

# Statistical Significance Tests
anova_res = calculate_wait_time_anova(filtered_df)
kruskal_res = calculate_duration_kruskal(filtered_df)

c_stat1, c_stat2 = st.columns(2)
with c_stat1:
    render_insight_box(
        title=f"One-Way ANOVA: Department Wait Variance (F = {anova_res['f_stat']:.2f}, p = {anova_res['p_value']:.4e})",
        text=anova_res["interpretation"],
        category="Warning" if anova_res["significant"] else "Info"
    )

with c_stat2:
    render_insight_box(
        title=f"Kruskal-Wallis: Consultation Duration Variance (H = {kruskal_res['h_stat']:.2f})",
        text=kruskal_res["interpretation"],
        category="Info"
    )

# Departmental Compliance Summary Table
st.markdown("#### 📋 Department Queue SLA Performance Breakdown")
dept_detail = filtered_df.groupby("department_name").agg(
    encounters=("visit_id", "count"),
    mean_wait=("wait_time_minutes", "mean"),
    median_wait=("wait_time_minutes", "median"),
    p90_wait=("wait_time_minutes", lambda x: np.percentile(x.dropna(), 90) if len(x.dropna()) > 0 else 0),
    breach_count=("is_sla_breach", "sum"),
    breach_rate=("is_sla_breach", lambda x: (x.sum() / len(x) * 100.0) if len(x) > 0 else 0)
).reset_index()

dept_detail["Compliance_Status"] = np.where(dept_detail["mean_wait"] > 30.0, "🔴 SLA Breach", "🟢 Compliant")
dept_detail = dept_detail.sort_values("mean_wait", ascending=False)

st.dataframe(
    dept_detail.style.format({
        "encounters": "{:,}",
        "mean_wait": "{:.1f} mins",
        "median_wait": "{:.1f} mins",
        "p90_wait": "{:.1f} mins",
        "breach_count": "{:,}",
        "breach_rate": "{:.1f}%"
    }),
    use_container_width=True,
    hide_index=True
)
