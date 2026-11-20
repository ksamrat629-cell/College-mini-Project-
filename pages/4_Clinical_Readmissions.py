"""
Page 4: Clinical Diagnoses, ICD-10 & 30-Day Readmission Analytics
MetroCare Health Systems | Operational Intelligence Platform
US-05, US-06 | Features F-05, F-06
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_analytics_view
from src.data_cleaner import clean_analytics_data
from src.analytics import compute_readmission_rate
from src.ui import render_tailwind_header, render_kpi_grid, render_insight_box, apply_plotly_theme

st.set_page_config(page_title="Clinical Readmissions | MetroCare", page_icon="🩺", layout="wide")

# Header
render_tailwind_header(
    title="Clinical Diagnoses, ICD-10 & 30-Day Readmissions",
    subtitle="Top ICD-10 clinical conditions, disease burden trends, and 30-day unplanned readmission surveillance",
    badge_text="Clinical Quality Monitor",
    badge_color="bg-emerald-100 text-emerald-800"
)

# Load data
raw_df = load_analytics_view()
clean_df, _ = clean_analytics_data(raw_df)

# Sidebar filters
st.sidebar.markdown("### 🎛️ Clinical Cohort Filters")
depts = sorted(clean_df["department_name"].dropna().unique().tolist())
selected_depts = st.sidebar.multiselect("Departments", options=depts, default=depts)

categories = sorted(clean_df["disease_category"].dropna().unique().tolist()) if "disease_category" in clean_df.columns else []
selected_cats = st.sidebar.multiselect("Disease Category", options=categories, default=categories) if categories else []

# Filter
filtered_df = clean_df[
    (clean_df["department_name"].isin(selected_depts if selected_depts else depts))
].copy()
if selected_cats and "disease_category" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["disease_category"].isin(selected_cats)]

# Compute 30-day readmission analytics
readmit_metrics = compute_readmission_rate(filtered_df, window_days=30)
total_enc = readmit_metrics["total_encounters"]
readmit_count = readmit_metrics["readmission_count"]
readmit_rate = readmit_metrics["readmission_rate"]
unique_icd = filtered_df["primary_icd10_code"].nunique() if "primary_icd10_code" in filtered_df.columns else 0

kpis = [
    {
        "title": "Clinical Encounters",
        "value": f"{total_enc:,}",
        "subtext": f"{len(selected_depts if selected_depts else depts)} Active Clinics",
        "badge_text": "Monitored",
        "badge_color": "bg-blue-100 text-blue-800"
    },
    {
        "title": "30-Day Readmissions",
        "value": f"{readmit_count:,}",
        "subtext": "Unplanned Clinical Returns",
        "badge_text": "Compliant" if readmit_rate <= 8.0 else "Breach",
        "badge_color": "bg-emerald-100 text-emerald-800" if readmit_rate <= 8.0 else "bg-red-100 text-red-800"
    },
    {
        "title": "Unplanned Readmission Rate",
        "value": f"{readmit_rate:.1f}%",
        "subtext": "Quality Target: < 8.0%",
        "badge_text": "Target Met" if readmit_rate <= 8.0 else "Elevated Risk",
        "badge_color": "bg-emerald-100 text-emerald-800" if readmit_rate <= 8.0 else "bg-red-100 text-red-800"
    },
    {
        "title": "Unique Diagnoses",
        "value": f"{unique_icd}",
        "subtext": "Active ICD-10 Classifications",
        "badge_text": "ICD-10",
        "badge_color": "bg-purple-100 text-purple-800"
    }
]
render_kpi_grid(kpis)

# Layout: 2 Columns for Visuals
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📊 Top 10 ICD-10 Diagnoses Pareto Analysis")
    if "primary_diagnosis_name" in filtered_df.columns and "primary_icd10_code" in filtered_df.columns:
        diag_counts = filtered_df.groupby(["primary_icd10_code", "primary_diagnosis_name"]).size().reset_index(name="Encounters")
        diag_counts["Label"] = diag_counts["primary_icd10_code"] + " - " + diag_counts["primary_diagnosis_name"]
        diag_counts = diag_counts.sort_values("Encounters", ascending=False).head(10)
        
        diag_counts["Cumulative_Pct"] = (diag_counts["Encounters"].cumsum() / diag_counts["Encounters"].sum() * 100.0).round(1)
        
        fig_pareto = go.Figure()
        # Bar trace
        fig_pareto.add_trace(go.Bar(
            x=diag_counts["Label"],
            y=diag_counts["Encounters"],
            name="Encounter Volume",
            marker_color="#2B6CB0",
            yaxis="y1"
        ))
        # Cumulative line trace
        fig_pareto.add_trace(go.Scatter(
            x=diag_counts["Label"],
            y=diag_counts["Cumulative_Pct"],
            name="Cumulative %",
            marker_color="#E53E3E",
            mode="lines+markers",
            yaxis="y2"
        ))
        
        apply_plotly_theme(fig_pareto, height=400)
        fig_pareto.update_layout(
            yaxis=dict(title="Encounter Count", side="left"),
            yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0, 105]),
            xaxis=dict(tickangle=-35),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_pareto, use_container_width=True)
    else:
        st.info("No ICD-10 diagnosis columns found in dataset.")

with col2:
    st.markdown("#### 📈 Disease Burden Distribution Over Time")
    if "visit_date" in filtered_df.columns and "disease_category" in filtered_df.columns:
        filtered_df["Month"] = filtered_df["visit_date"].dt.strftime("%Y-%m")
        monthly_disease = filtered_df.groupby(["Month", "disease_category"]).size().reset_index(name="Encounters")
        
        fig_area = px.bar(
            monthly_disease,
            x="Month",
            y="Encounters",
            color="disease_category",
            barmode="stack",
            labels={"Encounters": "Monthly Encounters", "disease_category": "Disease Category", "Month": "Visit Month"}
        )
        apply_plotly_theme(fig_area, height=400)
        fig_area.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_area, use_container_width=True)

# Quality Insight Box
render_insight_box(
    title=f"Clinical Readmission Surveillance: {readmit_rate:.1f}% Unplanned Return Rate",
    text=(
        f"Among {total_enc} analyzed encounters, {readmit_count} unplanned clinical readmissions occurred within 30 days of discharge. "
        "Scheduled routine follow-ups are strictly excluded per NABH quality guidelines. Cardiology and Internal Medicine represent the highest frequency return conditions."
    ),
    category="Success" if readmit_rate <= 8.0 else "Warning"
)

# Detailed Readmission Audit Log Table
st.markdown("#### 🚨 30-Day Unplanned Readmissions Patient Registry")
readmitted_encounters = filtered_df[filtered_df["is_30day_readmission"] == 1][
    ["visit_id", "patient_id", "patient_name", "department_name", "doctor_name", "visit_date", "primary_diagnosis_name", "visit_type"]
].sort_values("visit_date", ascending=False)

if not readmitted_encounters.empty:
    st.dataframe(
        readmitted_encounters.head(15),
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("No unplanned 30-day readmissions recorded for the selected filter cohort.")
