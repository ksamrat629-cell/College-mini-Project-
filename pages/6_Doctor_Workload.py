"""
Page 6: Doctor Workload, Capacity & Rostering Intelligence
MetroCare Health Systems | Operational Intelligence Platform
US-09, US-11 | Features F-09, F-11
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_analytics_view
from src.data_cleaner import clean_analytics_data
from src.analytics import compute_doctor_utilization
from src.ui import render_tailwind_header, render_kpi_grid, render_insight_box

st.set_page_config(page_title="Doctor Workload | MetroCare", page_icon="👨‍⚕️", layout="wide")

# Header
render_tailwind_header(
    title="Doctor Workload, Capacity & Rostering Intelligence",
    subtitle="Clinician utilization analysis, burnout surveillance (>95%), and 7-day walk-in vs pre-booked counter rostering",
    badge_text="Staffing & Capacity",
    badge_color="bg-blue-100 text-blue-800"
)

# Load data
raw_df = load_analytics_view()
clean_df, _ = clean_analytics_data(raw_df)

# Sidebar filters
st.sidebar.markdown("### 🎛️ Clinician & Shift Filters")
depts = sorted(clean_df["department_name"].dropna().unique().tolist())
selected_depts = st.sidebar.multiselect("Departments", options=depts, default=depts)

filtered_df = clean_df[clean_df["department_name"].isin(selected_depts if selected_depts else depts)].copy()

# Compute Doctor Utilization
doc_util = compute_doctor_utilization(filtered_df)

overutilized = doc_util[doc_util["utilization_pct"] > 95.0]
underutilized = doc_util[doc_util["utilization_pct"] < 50.0]
avg_duration = filtered_df["consultation_duration_minutes"].mean() if "consultation_duration_minutes" in filtered_df.columns else 0.0

kpis = [
    {
        "title": "Active Clinicians",
        "value": f"{len(doc_util):,}",
        "subtext": f"Across {len(selected_depts if selected_depts else depts)} Departments",
        "badge_text": "Rostered",
        "badge_color": "bg-blue-100 text-blue-800"
    },
    {
        "title": "Overburdened Doctors",
        "value": f"{len(overutilized):,}",
        "subtext": "Utilization > 95% (Burnout Risk)",
        "badge_text": "High Risk" if len(overutilized) > 0 else "Normal",
        "badge_color": "bg-red-100 text-red-800" if len(overutilized) > 0 else "bg-emerald-100 text-emerald-800"
    },
    {
        "title": "Underutilized Doctors",
        "value": f"{len(underutilized):,}",
        "subtext": "Utilization < 50% (Idle Capacity)",
        "badge_text": "Excess Capacity" if len(underutilized) > 0 else "Balanced",
        "badge_color": "bg-amber-100 text-amber-800" if len(underutilized) > 0 else "bg-emerald-100 text-emerald-800"
    },
    {
        "title": "Avg Consultation Time",
        "value": f"{avg_duration:.1f} Mins",
        "subtext": "Standard Clinical Consultation",
        "badge_text": "Clinical Pace",
        "badge_color": "bg-purple-100 text-purple-800"
    }
]
render_kpi_grid(kpis)

# Layout: 2 Columns for Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🩺 Clinician Capacity Utilization (% of Scheduled Shift)")
    if not doc_util.empty:
        # Sort for clean horizontal bar chart
        chart_data = doc_util.sort_values("utilization_pct", ascending=True).copy()
        chart_data["color"] = np.where(
            chart_data["utilization_pct"] > 95.0,
            "#E53E3E", # Red
            np.where(chart_data["utilization_pct"] < 50.0, "#F59E0B", "#10B981") # Amber or Green
        )
        
        fig_util = go.Figure()
        fig_util.add_trace(go.Bar(
            y=chart_data["doctor_name"],
            x=chart_data["utilization_pct"],
            orientation="h",
            marker_color=chart_data["color"],
            text=[f"{v:.1f}%" for v in chart_data["utilization_pct"]],
            textposition="auto"
        ))
        
        # Benchmark lines
        fig_util.add_vline(x=95.0, line_dash="dash", line_color="#E53E3E", annotation_text="Burnout (95%)", annotation_position="top right")
        fig_util.add_vline(x=50.0, line_dash="dash", line_color="#F59E0B", annotation_text="Underutilized (50%)", annotation_position="bottom right")
        
        fig_util.update_layout(
            xaxis=dict(title="Utilization (% of Scheduled Time)", range=[0, max(110, chart_data['utilization_pct'].max() + 10)]),
            yaxis=dict(title="Doctor"),
            margin=dict(l=20, r=20, t=30, b=20),
            height=420
        )
        st.plotly_chart(fig_util, use_container_width=True)

with col2:
    st.markdown("#### 🚶‍♂️ Walk-In vs. Pre-Booked Arrival Curves (Rostering)")
    filtered_df["hour"] = filtered_df["check_in_time"].dt.hour
    
    hourly_types = filtered_df.groupby(["hour", "appointment_type"]).size().reset_index(name="Encounters")
    
    fig_line = px.line(
        hourly_types,
        x="hour",
        y="Encounters",
        color="appointment_type",
        markers=True,
        color_discrete_map={"Walk-in": "#E53E3E", "Pre-booked": "#2B6CB0"},
        labels={"hour": "Arrival Hour of Day (24-Hour)", "Encounters": "Patient Check-in Volume"}
    )
    fig_line.add_vrect(
        x0=9, x1=11.5,
        fillcolor="red", opacity=0.1,
        layer="below", line_width=0,
        annotation_text="Morning Walk-in Surge", annotation_position="top left"
    )
    fig_line.update_layout(
        xaxis=dict(dtick=2),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=30, b=20),
        height=420
    )
    st.plotly_chart(fig_line, use_container_width=True)

# Rostering & Staffing Recommendation Callout
overburdened_names = ", ".join(overutilized["doctor_name"].tolist()) if not overutilized.empty else "None"
render_insight_box(
    title=f"Rostering & Shift Counter Recommendations (Overburdened: {overburdened_names})",
    text=(
        "Walk-in patient registration peaks sharply between 09:00 AM and 11:30 AM (reaching max queue load at 10:00 AM). "
        "Recommend deploying 2 additional registration counters during morning peak hours. Doctors with >95% utilization "
        "should have daily scheduled slot caps reduced by 15% to prevent burnout."
    ),
    category="Warning" if len(overutilized) > 0 else "Success"
)

# Physician Workload Summary Table
st.markdown("#### 📋 Detailed Clinician Workload & Utilization Audit")
st.dataframe(
    doc_util.style.format({
        "encounters": "{:,}",
        "consult_minutes": "{:.0f} mins",
        "scheduled_minutes": "{:.0f} mins",
        "utilization_pct": "{:.1f}%"
    }),
    use_container_width=True,
    hide_index=True
)
