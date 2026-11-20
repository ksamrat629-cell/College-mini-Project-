"""
Page 3: Appointment Attendance & No-Show Risk Analytics
MetroCare Health Systems | Operational Intelligence Platform
US-02, US-15 | Features F-02, F-13
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_all_tables
from src.analytics import compute_no_show_matrix
from src.stats import calculate_no_show_chi2
from src.ui import render_tailwind_header, render_kpi_grid, render_insight_box, apply_plotly_theme

st.set_page_config(page_title="No-Show Analytics | MetroCare", page_icon="📅", layout="wide")

# Header
render_tailwind_header(
    title="Appointment Attendance & No-Show Risk Analytics",
    subtitle="Lead-time correlation, booking channel disparities, and demographic no-show risk heatmaps",
    badge_text="Attendance Intelligence",
    badge_color="bg-purple-100 text-purple-800"
)

# Load data
tables = load_all_tables()
appts_df = tables["appointments"].copy()
patients_df = tables["patients"].copy()
depts_df = tables["departments"].copy()

# Join patient demographics
merged_df = appts_df.merge(
    patients_df[["patient_id", "age", "age_group", "gender"]],
    on="patient_id",
    how="left"
).merge(
    depts_df[["department_id", "department_name", "standard_consultation_fee"]],
    on="department_id",
    how="left"
)

# Sidebar Filters
st.sidebar.markdown("### 🎛️ Appointment Cohort Filters")
channels = sorted(merged_df["booking_channel"].dropna().unique().tolist())
selected_channels = st.sidebar.multiselect("Booking Channels", options=channels, default=channels)

lead_cats = sorted(merged_df["lead_time_category"].dropna().unique().tolist())
selected_leads = st.sidebar.multiselect("Lead Time Category", options=lead_cats, default=lead_cats)

# Filter cohort
filtered_appts = merged_df[
    (merged_df["booking_channel"].isin(selected_channels if selected_channels else channels)) &
    (merged_df["lead_time_category"].isin(selected_leads if selected_leads else lead_cats))
].copy()

# Compute KPIs
ns_metrics = compute_no_show_matrix(filtered_appts)
total_appts = ns_metrics["total_appointments"]
completed = ns_metrics["completed"]
no_shows = ns_metrics["no_shows"]
unfulfilled_rate = ns_metrics["no_show_rate"]

kpis = [
    {
        "title": "Scheduled Appointments",
        "value": f"{total_appts:,}",
        "subtext": "OPD Pre-booked Capacity",
        "badge_text": "Total Booked",
        "badge_color": "bg-blue-100 text-blue-800"
    },
    {
        "title": "Attended Encounters",
        "value": f"{completed:,}",
        "subtext": f"Completion Rate: {(completed / total_appts * 100.0 if total_appts > 0 else 0):.1f}%",
        "badge_text": "Fulfilled",
        "badge_color": "bg-emerald-100 text-emerald-800"
    },
    {
        "title": "Patient No-Shows",
        "value": f"{no_shows:,}",
        "subtext": f"{ns_metrics.get('cancelled', 0)} Additional Cancellations",
        "badge_text": "Unfulfilled",
        "badge_color": "bg-red-100 text-red-800"
    },
    {
        "title": "Overall No-Show Rate",
        "value": f"{unfulfilled_rate:.1f}%",
        "subtext": "Hospital Target: < 12.0%",
        "badge_text": "High Risk" if unfulfilled_rate > 15 else "Target Met",
        "badge_color": "bg-red-100 text-red-800" if unfulfilled_rate > 15 else "bg-emerald-100 text-emerald-800"
    }
]
render_kpi_grid(kpis)

# Layout: 2 Columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🗺️ 2D Risk Heatmap: Lead Time vs. Demographic Age Group")
    # Compute no-show probability per cell
    filtered_appts["is_unfulfilled"] = filtered_appts["appointment_status"].isin(["No-Show", "Cancelled"]).astype(int)
    
    heatmap_data = filtered_appts.groupby(["lead_time_category", "age_group"])["is_unfulfilled"].agg(
        rate=lambda x: round(x.sum() / len(x) * 100.0, 1) if len(x) > 0 else 0.0
    ).reset_index()
    
    pivot_heatmap = heatmap_data.pivot(index="lead_time_category", columns="age_group", values="rate").fillna(0)
    
    fig_heat = px.imshow(
        pivot_heatmap,
        labels=dict(x="Demographic Age Group", y="Lead Time Category", color="No-Show %"),
        x=pivot_heatmap.columns,
        y=pivot_heatmap.index,
        color_continuous_scale="YlOrRd",
        text_auto=True,
        aspect="auto"
    )
    apply_plotly_theme(fig_heat, height=380)
    st.plotly_chart(fig_heat, use_container_width=True)

with col2:
    st.markdown("#### 🍩 Appointment Disposition by Booking Channel")
    channel_counts = filtered_appts.groupby(["booking_channel", "appointment_status"]).size().reset_index(name="count")
    
    fig_donut = px.pie(
        channel_counts,
        values="count",
        names="appointment_status",
        hole=0.45,
        color="appointment_status",
        color_discrete_map={
            "Completed": "#10B981",
            "No-Show": "#E53E3E",
            "Cancelled": "#F59E0B"
        }
    )
    apply_plotly_theme(fig_donut, height=380)
    fig_donut.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# Chi-Square Test Box
chi2_res = calculate_no_show_chi2(filtered_appts, cat_col1="booking_channel", cat_col2="appointment_status")
render_insight_box(
    title=f"Chi-Square Independence Test: Channel Disparity (χ² = {chi2_res['chi2']:.2f}, p = {chi2_res['p_value']:.4e})",
    text=chi2_res["interpretation"],
    category="Danger" if chi2_res["significant"] else "Info"
)

# Department Revenue Loss Analysis Table
st.markdown("#### 💸 Department Financial Impact: Unfulfilled Slot Opportunity Loss")
dept_impact = filtered_appts.groupby("department_name").agg(
    total_appts=("appointment_id", "count"),
    completed=("appointment_status", lambda x: (x == "Completed").sum()),
    no_shows=("appointment_status", lambda x: (x == "No-Show").sum()),
    cancelled=("appointment_status", lambda x: (x == "Cancelled").sum()),
    standard_fee=("standard_consultation_fee", "first")
).reset_index()

dept_impact["unfulfilled_total"] = dept_impact["no_shows"] + dept_impact["cancelled"]
dept_impact["no_show_rate"] = (dept_impact["unfulfilled_total"] / dept_impact["total_appts"] * 100.0).round(1)
dept_impact["estimated_revenue_lost"] = dept_impact["unfulfilled_total"] * dept_impact["standard_fee"]
dept_impact = dept_impact.sort_values("estimated_revenue_lost", ascending=False)

st.dataframe(
    dept_impact.style.format({
        "total_appts": "{:,}",
        "completed": "{:,}",
        "no_shows": "{:,}",
        "cancelled": "{:,}",
        "standard_fee": "₹{:,.0f}",
        "unfulfilled_total": "{:,}",
        "no_show_rate": "{:.1f}%",
        "estimated_revenue_lost": "₹{:,.2f}"
    }),
    use_container_width=True,
    hide_index=True
)
