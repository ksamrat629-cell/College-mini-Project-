"""
MetroCare Health Systems - Operational Intelligence & Patient Visit Analytics Platform
Entrypoint & Global Navigation Management
MCA Capstone Project 2026 | US Samrat (Roll: 2500320140158) | Mentor: Prof. Anjali Pandey
"""

import os
import streamlit as st
import pandas as pd
from src.data_loader import load_analytics_view, load_all_tables
from src.data_cleaner import clean_analytics_data, audit_data_quality
from src.analytics import compute_wait_time_sla, compute_no_show_matrix, compute_revenue_payer_mix
from src.ui import render_tailwind_header, render_kpi_grid, render_insight_box

# 1. Configure Streamlit Page
st.set_page_config(
    page_title="MetroCare Operational Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Render Executive Header Banner
render_tailwind_header(
    title="MetroCare Health Systems",
    subtitle="Healthcare Patient Visit Analysis & Operational Intelligence Platform | 450-Bed Tertiary Hospital, Delhi NCR",
    badge_text="Active Production v1.0",
    badge_color="bg-emerald-100 text-emerald-800"
)

# 3. Load Data Mart and Clean
try:
    raw_df = load_analytics_view()
    clean_df, anomaly_df = clean_analytics_data(raw_df)
    tables = load_all_tables()
except Exception as e:
    st.error(f"Failed to load analytics data mart from SQLite: {e}")
    st.stop()

# 4. Initialize Global Sidebar Filters (st.session_state)
st.sidebar.markdown("### 🏥 Operational Filter Controls")
st.sidebar.caption("Shared state across all operational modules")

# Department Filter
all_depts = sorted(clean_df["department_name"].dropna().unique().tolist())
if "selected_departments" not in st.session_state:
    st.session_state["selected_departments"] = all_depts

selected_depts = st.sidebar.multiselect(
    "Select Clinical Departments",
    options=all_depts,
    default=st.session_state["selected_departments"],
    help="Filter across 8 specialized OPD clinics"
)
st.session_state["selected_departments"] = selected_depts if selected_depts else all_depts

# Visit Type Filter
all_visit_types = sorted(clean_df["visit_type"].dropna().unique().tolist())
if "selected_visit_types" not in st.session_state:
    st.session_state["selected_visit_types"] = all_visit_types

selected_vtypes = st.sidebar.multiselect(
    "Select Visit Types",
    options=all_visit_types,
    default=st.session_state["selected_visit_types"],
    help="Filter by clinical visit category"
)
st.session_state["selected_visit_types"] = selected_vtypes if selected_vtypes else all_visit_types

# Appointment Type (Walk-in vs Pre-booked)
all_appt_types = sorted(clean_df["appointment_type"].dropna().unique().tolist())
selected_atypes = st.sidebar.multiselect(
    "Appointment Nature",
    options=all_appt_types,
    default=all_appt_types,
    help="Walk-in vs Pre-scheduled encounter"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Database Diagnostics")
st.sidebar.info(
    f"**Active Records:** {len(clean_df):,} encounters\n\n"
    f"**Anomalies Quarantined:** {len(anomaly_df)} (RULE-01)\n\n"
    f"**Clinics Monitored:** {len(all_depts)} departments\n\n"
    f"**Engine:** SQLite3 ACID Mart"
)
st.sidebar.markdown("---")
st.sidebar.caption("ABES Engineering College • MCA Capstone 2026")

# 5. Apply Active Global Filters
filtered_df = clean_df[
    (clean_df["department_name"].isin(st.session_state["selected_departments"])) &
    (clean_df["visit_type"].isin(st.session_state["selected_visit_types"])) &
    (clean_df["appointment_type"].isin(selected_atypes if selected_atypes else all_appt_types))
]

# 6. Compute Macro Metrics
wait_kpis = compute_wait_time_sla(filtered_df)
ns_metrics = compute_no_show_matrix(tables["appointments"])
rev_metrics = compute_revenue_payer_mix(filtered_df)

total_visits = len(filtered_df)
mean_wait = wait_kpis["mean_wait"]
sla_rate = wait_kpis["breach_rate"]
ns_rate = ns_metrics["no_show_rate"]
readmit_rate = (filtered_df["is_30day_readmission"].sum() / total_visits * 100.0) if total_visits > 0 else 0.0

# 7. Render Executive KPI Grid
kpi_cards = [
    {
        "title": "Hospital Throughput",
        "value": f"{total_visits:,}",
        "subtext": f"{len(st.session_state['selected_departments'])} Clinics Selected",
        "badge_text": "Live Encounters",
        "badge_color": "bg-blue-100 text-blue-800"
    },
    {
        "title": "Average Wait Time",
        "value": f"{mean_wait:.1f} Mins",
        "subtext": f"SLA Breach Rate: {sla_rate:.1f}% (>30m)",
        "badge_text": "SLA Breach" if mean_wait > 30 else "Compliant",
        "badge_color": "bg-red-100 text-red-800" if mean_wait > 30 else "bg-emerald-100 text-emerald-800"
    },
    {
        "title": "Appointment No-Show Rate",
        "value": f"{ns_rate:.1f}%",
        "subtext": f"{ns_metrics.get('unfulfilled', 0)} Unfulfilled of {ns_metrics.get('total_appointments', 0)}",
        "badge_text": "High Risk" if ns_rate > 15 else "Normal",
        "badge_color": "bg-amber-100 text-amber-800" if ns_rate > 15 else "bg-emerald-100 text-emerald-800"
    },
    {
        "title": "30-Day Readmission",
        "value": f"{readmit_rate:.1f}%",
        "subtext": "Quality Target: < 8.0%",
        "badge_text": "High" if readmit_rate > 8 else "Within SLA",
        "badge_color": "bg-emerald-100 text-emerald-800" if readmit_rate <= 8 else "bg-red-100 text-red-800"
    }
]
render_kpi_grid(kpi_cards)

# 8. Operational Insight Banner
if mean_wait > 30.0:
    render_insight_box(
        title="High Patient Wait Times Detected",
        text=f"The current filtered cohort exhibits an average wait of {mean_wait:.1f} minutes, with {sla_rate:.1f}% of encounters exceeding the 30-minute SLA benchmark. Cardiology and Orthopedics are the primary bottleneck drivers.",
        category="Warning"
    )
else:
    render_insight_box(
        title="Hospital Operations Stable",
        text=f"Average wait time ({mean_wait:.1f} min) is within the hospital benchmark. Continuous queue monitoring remains active.",
        category="Success"
    )

# 9. Multi-Module Directory Cards
st.markdown("### 📑 Specialized Analytics Modules")
st.markdown("Select any module from the sidebar or click through the direct access panels below:")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-bottom: 12px;">
            <div style="font-weight: 700; color: #1B365D; font-size: 15px;">📊 1. Executive Overview</div>
            <p style="font-size: 12px; color: #64748B; margin-top: 6px;">Hospital-wide volume curves, 24-hr peak hourly arrival surge, CSAT correlation scatter, and breach exception log.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-bottom: 12px;">
            <div style="font-weight: 700; color: #1B365D; font-size: 15px;">⏱️ 2. Queue Wait Times</div>
            <p style="font-size: 12px; color: #64748B; margin-top: 6px;">Registration-to-consultation wait monitoring against 30m SLA, ANOVA F-test, and consultation duration box plots.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-bottom: 12px;">
            <div style="font-weight: 700; color: #1B365D; font-size: 15px;">📅 3. No-Show Analytics</div>
            <p style="font-size: 12px; color: #64748B; margin-top: 6px;">Lead time × Age group 2D risk heatmap, Chi-Square independence test, booking channels, and lost revenue.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-bottom: 12px;">
            <div style="font-weight: 700; color: #1B365D; font-size: 15px;">🩺 4. Clinical Readmissions</div>
            <p style="font-size: 12px; color: #64748B; margin-top: 6px;">Top 10 ICD-10 diagnoses Pareto chart, 30-day unplanned readmission rate tracking, and monthly acute disease trends.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-bottom: 12px;">
            <div style="font-weight: 700; color: #1B365D; font-size: 15px;">💰 5. Revenue & Payer Mix</div>
            <p style="font-size: 12px; color: #64748B; margin-top: 6px;">Gross vs net billing realization, Cash vs Insurance vs Ayushman Bharat mix, and interactive no-show recovery simulator.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-bottom: 12px;">
            <div style="font-weight: 700; color: #1B365D; font-size: 15px;">👨‍⚕️ 6. Doctor Workload</div>
            <p style="font-size: 12px; color: #64748B; margin-top: 6px;">Physician slot utilization gauges, burnout risk detection (>95%), and 7-day walk-in vs pre-booked counter rostering.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-bottom: 12px;">
            <div style="font-weight: 700; color: #1B365D; font-size: 15px;">🔍 7. Data Explorer & Quality</div>
            <p style="font-size: 12px; color: #64748B; margin-top: 6px;">Self-service multi-filter tabular grid, missing cell audit, duplicate check, and direct CSV/Excel report downloads.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; margin-bottom: 12px;">
            <div style="font-weight: 700; color: #1B365D; font-size: 15px;">ℹ️ 8. About & Governance</div>
            <p style="font-size: 12px; color: #64748B; margin-top: 6px;">ABES MCA academic accreditation, author credentials (US Samrat), mentor attribution, and end-to-end SDLC traceability.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# 10. Data Quality Summary Alert
quality_audit = audit_data_quality(clean_df)
st.caption(
    f"Data Integrity Status: Completeness Score: {quality_audit['completeness_score']}% | "
    f"Total Ingestion Records: {quality_audit['total_records']} | Duplicate PKs: {quality_audit['duplicate_count']} | "
    f"Quarantined Anomalies: {len(anomaly_df)}"
)
