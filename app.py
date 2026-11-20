"""
MetroCare Health Systems - Operational Intelligence & Patient Visit Analytics Platform
Entrypoint & Global Navigation Management
MCA Capstone Project 2026 | US Samrat (Roll: 2500320140158) | Mentor: Prof. Anjali Pandey
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_analytics_view, load_all_tables
from src.data_cleaner import clean_analytics_data, audit_data_quality
from src.analytics import (
    compute_wait_time_sla,
    compute_no_show_matrix,
    compute_revenue_payer_mix,
    compute_department_throughput
)
from src.ui import (
    render_tailwind_header,
    render_kpi_grid,
    render_insight_box,
    apply_plotly_theme,
    apply_custom_css
)

# 1. Configure Streamlit Page
st.set_page_config(
    page_title="MetroCare Operational Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Render Executive Header Banner & Inject Global CSS
render_tailwind_header(
    title="MetroCare Health Systems",
    subtitle="Healthcare Patient Visit Analysis & Operational Intelligence Platform | 450-Bed Tertiary Care Hospital, Delhi NCR",
    badge_text="Live Production v1.0",
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
st.sidebar.markdown(
    """
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
        <span style="font-size: 20px;">🏥</span>
        <span style="font-size: 16px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">
            METROCARE OPS
        </span>
    </div>
    <div style="font-size: 11px; color: #94A3B8; margin-bottom: 16px; font-weight: 500;">
        Operational Intelligence Command Center
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("### 🎛️ Operational Filters")
st.sidebar.caption("Global filter criteria shared across all 8 modules")

# Department Filter
all_depts = sorted(clean_df["department_name"].dropna().unique().tolist())
if "selected_departments" not in st.session_state:
    st.session_state["selected_departments"] = all_depts

# Quick Filter Preset Buttons in Sidebar
st.sidebar.markdown("<div style='font-size: 11px; font-weight: 700; color: #94A3B8; text-transform: uppercase; margin-bottom: 6px;'>Quick Department Presets</div>", unsafe_allow_html=True)
p_col1, p_col2 = st.sidebar.columns(2)
with p_col1:
    if st.button("All Clinics", use_container_width=True):
        st.session_state["selected_departments"] = all_depts
        st.rerun()
with p_col2:
    if st.button("Bottlenecks", use_container_width=True, help="Cardiology & Orthopedics"):
        st.session_state["selected_departments"] = [d for d in ["Cardiology", "Orthopedics"] if d in all_depts]
        st.rerun()

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
    help="Filter by clinical encounter category"
)
st.session_state["selected_visit_types"] = selected_vtypes if selected_vtypes else all_visit_types

# Appointment Type (Walk-in vs Pre-booked)
all_appt_types = sorted(clean_df["appointment_type"].dropna().unique().tolist())
selected_atypes = st.sidebar.multiselect(
    "Appointment Nature",
    options=all_appt_types,
    default=all_appt_types,
    help="Walk-in encounter vs Pre-scheduled appointment"
)

st.sidebar.markdown("---")

# Database Diagnostics Box
quality_audit = audit_data_quality(clean_df)
st.sidebar.markdown(
    f"""
    <div style="
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 12px;
        font-size: 11.5px;
        color: #CBD5E1;
        line-height: 1.6;
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
            <span style="font-weight: 700; color: #FFFFFF; font-size: 12px;">📊 Diagnostics</span>
            <span style="display: flex; align-items: center; gap: 4px; color: #34D399; font-weight: 700;">
                <span class="pulse-dot"></span> Online
            </span>
        </div>
        <div>Active Records: <strong style="color: #60A5FA;">{len(clean_df):,} encounters</strong></div>
        <div>Quarantined: <strong style="color: #F87171;">{len(anomaly_df)} (RULE-01)</strong></div>
        <div>Clinics Monitored: <strong style="color: #FBBF24;">{len(all_depts)} departments</strong></div>
        <div>Integrity Score: <strong style="color: #34D399;">{quality_audit['completeness_score']:.1f}%</strong></div>
        <div style="margin-top: 4px; font-size: 10px; color: #94A3B8;">Engine: SQLite3 ACID In-Memory</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")
st.sidebar.caption("ABES Engineering College • MCA Capstone 2026\n\nLearner: US Samrat | Mentor: Prof. Anjali Pandey")

# 5. Apply Active Global Filters
filtered_df = clean_df[
    (clean_df["department_name"].isin(st.session_state["selected_departments"])) &
    (clean_df["visit_type"].isin(st.session_state["selected_visit_types"])) &
    (clean_df["appointment_type"].isin(selected_atypes if selected_atypes else all_appt_types))
].copy()

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
        "subtext": f"{len(st.session_state['selected_departments'])} Clinics Monitored",
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
        "title": "Appointment No-Show",
        "value": f"{ns_rate:.1f}%",
        "subtext": f"{ns_metrics.get('unfulfilled', 0)} of {ns_metrics.get('total_appointments', 0)} Unfulfilled",
        "badge_text": "High Risk" if ns_rate > 15 else "Normal",
        "badge_color": "bg-amber-100 text-amber-800" if ns_rate > 15 else "bg-emerald-100 text-emerald-800"
    },
    {
        "title": "30-Day Readmission",
        "value": f"{readmit_rate:.1f}%",
        "subtext": "Quality SLA Target: < 8.0%",
        "badge_text": "High" if readmit_rate > 8 else "Within SLA",
        "badge_color": "bg-emerald-100 text-emerald-800" if readmit_rate <= 8 else "bg-red-100 text-red-800"
    }
]
render_kpi_grid(kpi_cards)

# 8. Operational Insight Banner
if mean_wait > 30.0:
    render_insight_box(
        title="Elevated Patient Wait Times Detected Across Outpatient Clinics",
        text=f"The current filtered cohort registers an average queue wait of {mean_wait:.1f} minutes, with {sla_rate:.1f}% of encounters exceeding the 30-minute benchmark. Priority triage adjustment and morning surge doctor allocation recommended for Cardiology and Orthopedics.",
        category="Warning"
    )
else:
    render_insight_box(
        title="Outpatient Clinic Operations Operating Within Prescribed SLA",
        text=f"Current average patient wait time ({mean_wait:.1f} min) satisfies the hospital SLA threshold of 30 minutes. Queue pacing and staff load balancing are optimal.",
        category="Success"
    )

# 9. Interactive Command Center Tabs
tab_overview, tab_matrix, tab_simulator, tab_directory = st.tabs([
    "📊 Executive Command & Surges",
    "🗺️ OPD Department Matrix",
    "⚡ What-If Simulator",
    "📑 Specialized Modules Directory"
])

with tab_overview:
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown("#### ⏰ 24-Hour Patient Arrival Volume & Peak Surge")
        st.caption("Distribution of patient arrivals showing morning peak (09:00 - 11:00 AM) and evening surge")

        filtered_df["arrival_hour"] = filtered_df["check_in_time"].dt.hour
        hourly_df = filtered_df.groupby("arrival_hour")["visit_id"].count().reset_index()
        hourly_df.columns = ["Hour", "Visits"]
        full_hours = pd.DataFrame({"Hour": list(range(24))})
        hourly_df = full_hours.merge(hourly_df, on="Hour", how="left").fillna(0)
        hourly_df["Is_Peak"] = hourly_df["Hour"].isin([9, 10, 11])

        colors = ["#F59E0B" if is_p else "#2563EB" for is_p in hourly_df["Is_Peak"]]

        fig_surge = go.Figure()
        fig_surge.add_trace(go.Bar(
            x=hourly_df["Hour"],
            y=hourly_df["Visits"],
            marker_color=colors,
            marker_line_width=0,
            text=hourly_df["Visits"].astype(int),
            textposition="outside",
            name="Arrival Volume"
        ))
        fig_surge.add_vline(x=9, line_dash="dash", line_color="#EF4444", annotation_text="Peak Start (9 AM)")
        fig_surge.add_vline(x=11.5, line_dash="dash", line_color="#EF4444", annotation_text="Peak End (11:30 AM)")
        apply_plotly_theme(fig_surge, height=360)
        fig_surge.update_xaxes(title="Encounter Check-in Hour (24-Hour Military Format)", tickmode="linear", dtick=2)
        fig_surge.update_yaxes(title="Patient Arrivals")
        st.plotly_chart(fig_surge, use_container_width=True)

    with col_chart2:
        st.markdown("#### 🏥 Clinic Throughput vs SLA Breach Rate")
        st.caption("Cross-clinic comparison of patient volume and percentage of patients waiting > 30 minutes")

        dept_summary = filtered_df.groupby("department_name").agg(
            Volume=("visit_id", "count"),
            Mean_Wait=("wait_time_minutes", "mean"),
            Breach_Count=("is_sla_breach", "sum")
        ).reset_index()
        dept_summary["Breach_Rate"] = (dept_summary["Breach_Count"] / dept_summary["Volume"] * 100.0).round(1)
        dept_summary = dept_summary.sort_values("Volume", ascending=False)

        fig_dept = px.bar(
            dept_summary,
            x="department_name",
            y="Volume",
            color="Breach_Rate",
            color_continuous_scale="Blues",
            text="Volume",
            labels={"department_name": "Clinic Department", "Volume": "Patient Visits", "Breach_Rate": "SLA Breach %"}
        )
        fig_dept.update_traces(textposition="outside")
        apply_plotly_theme(fig_dept, height=360)
        fig_dept.update_xaxes(title="Specialized OPD Department", tickangle=-25)
        fig_dept.update_yaxes(title="Total Encounter Volume")
        st.plotly_chart(fig_dept, use_container_width=True)

with tab_matrix:
    st.markdown("#### 📋 Comprehensive Outpatient Clinic Operational Scorecard")
    st.caption("Holistic operational performance matrix across volume, wait times, SLA compliance, CSAT, and net revenue")

    dept_matrix = filtered_df.groupby("department_name").agg(
        Total_Encounters=("visit_id", "count"),
        Avg_Wait_Mins=("wait_time_minutes", lambda x: round(x.mean(), 1)),
        Median_Wait_Mins=("wait_time_minutes", lambda x: round(x.median(), 1)),
        SLA_Breach_Pct=("is_sla_breach", lambda x: round((x.sum() / len(x)) * 100, 1)),
        Avg_CSAT=("csat_score", lambda x: round(x.dropna().mean(), 2) if len(x.dropna()) > 0 else 0.0),
        Readmit_Count=("is_30day_readmission", "sum")
    ).reset_index()

    dept_matrix["Readmit_Rate_Pct"] = ((dept_matrix["Readmit_Count"] / dept_matrix["Total_Encounters"]) * 100.0).round(1)
    dept_matrix["Status"] = np.where(dept_matrix["Avg_Wait_Mins"] > 30.0, "⚠️ Action Needed", "✅ SLA Met")
    
    # Render interactive styled dataframe
    st.dataframe(
        dept_matrix.sort_values("Total_Encounters", ascending=False),
        use_container_width=True,
        column_config={
            "department_name": st.column_config.TextColumn("Department"),
            "Total_Encounters": st.column_config.NumberColumn("Visits", format="%d"),
            "Avg_Wait_Mins": st.column_config.NumberColumn("Avg Wait (m)", format="%.1f min"),
            "Median_Wait_Mins": st.column_config.NumberColumn("Median Wait", format="%.1f min"),
            "SLA_Breach_Pct": st.column_config.ProgressColumn("SLA Breach %", min_value=0, max_value=100, format="%.1f%%"),
            "Avg_CSAT": st.column_config.NumberColumn("CSAT Score", format="%.2f / 5"),
            "Readmit_Rate_Pct": st.column_config.NumberColumn("30d Readmit %", format="%.1f%%"),
            "Status": st.column_config.TextColumn("Operational Status")
        },
        hide_index=True
    )

with tab_simulator:
    st.markdown("#### ⚡ Executive Operations & Revenue Recovery Simulator")
    st.caption("Interactive scenario modeling: evaluate the operational impact of reducing queue wait times and recovering unfulfilled appointment slots")

    sim_col1, sim_col2 = st.columns(2)

    with sim_col1:
        st.markdown("##### 🎚️ Policy Levers")
        wait_reduction_pct = st.slider("Target Wait Time Reduction (%)", min_value=5, max_value=40, value=20, step=5)
        sms_recovery_pct = st.slider("SMS Reminder Attendance Recovery (%)", min_value=10, max_value=60, value=30, step=5)
        avg_consult_fee = st.number_input("Average Clinic Consultation Fee (₹)", value=650, step=50)

    with sim_col2:
        st.markdown("##### 📈 Projected Operational & Financial Outcomes")
        current_unfulfilled = ns_metrics.get("unfulfilled", 0)
        recovered_patients = int(current_unfulfilled * (sms_recovery_pct / 100.0))
        recovered_revenue = recovered_patients * avg_consult_fee
        new_projected_wait = max(5.0, mean_wait * (1.0 - (wait_reduction_pct / 100.0)))
        projected_csat_lift = min(5.0, 3.8 + (wait_reduction_pct * 0.025))

        sc1, sc2 = st.columns(2)
        with sc1:
            st.metric("Recovered Encounters", f"{recovered_patients:,} Patients", delta=f"+{sms_recovery_pct}% Attendance")
            st.metric("New Projected Avg Wait", f"{new_projected_wait:.1f} Mins", delta=f"-{wait_reduction_pct}% Wait Time", delta_color="inverse")
        with sc2:
            st.metric("Recovered Clinic Revenue", f"₹{recovered_revenue:,}", delta="Direct OPD Margin")
            st.metric("Projected CSAT Rating", f"{projected_csat_lift:.2f} / 5.0", delta=f"+{wait_reduction_pct * 0.025:.2f} Satisfaction")

with tab_directory:
    st.markdown("#### 📑 Specialized Analytics Modules Directory")
    st.caption("Direct access to the 8 dedicated multi-page operational intelligence modules")

    col1, col2, col3, col4 = st.columns(4)

    modules = [
        ("📊 1. Executive Overview", "Hospital-wide volume curves, 24-hr peak hourly arrival surge, CSAT correlation scatter, and breach exception log.", "pages/1_Executive_Overview.py", "Overview"),
        ("⏱️ 2. Queue Wait Times", "Registration-to-consultation wait monitoring against 30m SLA, ANOVA F-test, and consultation duration box plots.", "pages/2_Queue_Wait_Times.py", "SLA"),
        ("📅 3. No-Show Analytics", "Lead time × Age group 2D risk heatmap, Chi-Square independence test, booking channels, and lost revenue.", "pages/3_No_Show_Analytics.py", "Risk"),
        ("🩺 4. Clinical Readmissions", "Top 10 ICD-10 diagnoses Pareto chart, 30-day unplanned readmission rate tracking, and monthly acute disease trends.", "pages/4_Clinical_Readmissions.py", "Clinical"),
        ("💰 5. Revenue & Payer Mix", "Gross vs net billing realization, Cash vs Insurance vs Ayushman Bharat mix, and interactive no-show recovery simulator.", "pages/5_Revenue_Payer_Mix.py", "Financial"),
        ("👨‍⚕️ 6. Doctor Workload", "Physician slot utilization gauges, burnout risk detection (>95%), and 7-day walk-in vs pre-booked counter rostering.", "pages/6_Doctor_Workload.py", "Workload"),
        ("🔍 7. Data Explorer & Quality", "Self-service multi-filter tabular grid, missing cell audit, duplicate check, and direct CSV/Excel report downloads.", "pages/7_Data_Explorer.py", "Governance"),
        ("ℹ️ 8. About & Governance", "ABES MCA academic accreditation, author credentials (US Samrat), mentor attribution, and end-to-end SDLC traceability.", "pages/8_About_Project.py", "Institutional")
    ]

    cols_list = [col1, col2, col3, col4, col1, col2, col3, col4]
    for idx, (m_title, m_desc, m_path, m_badge) in enumerate(modules):
        with cols_list[idx]:
            st.markdown(
                f"""
                <div class="nav-module-card" style="margin-bottom: 14px;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <span style="font-size: 13.5px; font-weight: 700; color: #1E3A8A;">{m_title}</span>
                            <span style="font-size: 10px; font-weight: 700; background: #EFF6FF; color: #2563EB; padding: 2px 6px; border-radius: 4px;">{m_badge}</span>
                        </div>
                        <p style="font-size: 11.5px; color: #64748B; line-height: 1.4; margin: 0 0 10px 0;">{m_desc}</p>
                    </div>
                    <div style="font-size: 11px; font-weight: 700; color: #2563EB; display: flex; align-items: center; gap: 4px;">
                        Navigate in Sidebar &rarr;
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# 10. Institutional Governance Footer
st.markdown("---")
fcol1, fcol2, fcol3 = st.columns([2, 1, 1])
with fcol1:
    st.markdown(
        """
        <div style="font-size: 12px; color: #64748B;">
            <strong>MetroCare Health Systems Operational Intelligence Platform</strong><br/>
            HCLTech Career Shaper Programme • ABES Engineering College, Ghaziabad (MCA 2026)<br/>
            Learner: <strong>US Samrat</strong> (Roll No: <code>2500320140158</code>) | Mentor: <strong>Prof. Anjali Pandey</strong>
        </div>
        """,
        unsafe_allow_html=True
    )
with fcol2:
    st.markdown(
        f"""
        <div style="font-size: 11.5px; color: #64748B;">
            <strong>Data Integrity Score:</strong> {quality_audit['completeness_score']}%<br/>
            <strong>Quarantined Records:</strong> {len(anomaly_df)} (RULE-01)<br/>
            <strong>Duplicate Keys:</strong> {quality_audit['duplicate_count']}
        </div>
        """,
        unsafe_allow_html=True
    )
with fcol3:
    st.markdown(
        """
        <div style="font-size: 11.5px; color: #64748B; text-align: right;">
            <span class="pulse-dot"></span> <strong>Live Production</strong><br/>
            Repository: <code>College-mini-Project-</code><br/>
            Version: <code>v1.0.4 - Release</code>
        </div>
        """,
        unsafe_allow_html=True
    )
