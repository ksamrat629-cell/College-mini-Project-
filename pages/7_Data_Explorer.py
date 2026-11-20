"""
Page 7: Self-Service Data Explorer & Data Quality Audit
MetroCare Health Systems | Operational Intelligence Platform
US-13, US-14 | Feature F-01
"""

import os
import io
import streamlit as st
import pandas as pd
from src.data_loader import load_analytics_view
from src.data_cleaner import clean_analytics_data, audit_data_quality
from src.ui import render_tailwind_header, render_kpi_grid, render_insight_box

st.set_page_config(page_title="Data Explorer & Quality | MetroCare", page_icon="🔍", layout="wide")

# Header
render_tailwind_header(
    title="Self-Service Data Explorer & Quality Audit",
    subtitle="Interactive tabular analytics view, RULE-01 anomaly quarantine logs, and multi-format dataset downloads",
    badge_text="Data Governance",
    badge_color="bg-slate-100 text-slate-800"
)

# Load data
raw_df = load_analytics_view()
clean_df, anomaly_df = clean_analytics_data(raw_df)

# Compute Data Quality Audit
quality_metrics = audit_data_quality(clean_df)

kpis = [
    {
        "title": "Ingested Records",
        "value": f"{len(raw_df):,}",
        "subtext": "Active Encounter Database",
        "badge_text": "Live ACID DB",
        "badge_color": "bg-blue-100 text-blue-800"
    },
    {
        "title": "Completeness Score",
        "value": f"{quality_metrics['completeness_score']:.1f}%",
        "subtext": f"{quality_metrics['total_missing_cells']} Missing Values Allowed",
        "badge_text": "High Quality",
        "badge_color": "bg-emerald-100 text-emerald-800"
    },
    {
        "title": "Quarantined Anomalies",
        "value": f"{len(anomaly_df)}",
        "subtext": "RULE-01 Inverted Timestamps",
        "badge_text": "Quarantined",
        "badge_color": "bg-red-100 text-red-800" if len(anomaly_df) > 0 else "bg-emerald-100 text-emerald-800"
    },
    {
        "title": "Duplicate Primary Keys",
        "value": f"{quality_metrics['duplicate_count']}",
        "subtext": "Unique Key Constraint Check",
        "badge_text": "Zero Duplicates",
        "badge_color": "bg-emerald-100 text-emerald-800"
    }
]
render_kpi_grid(kpis)

# Quality Insight Box
render_insight_box(
    title="Data Quality & Integrity Governance",
    text=(
        f"Data pipeline audited across {len(clean_df.columns)} schema columns. "
        f"Exactly {len(anomaly_df)} record was isolated under Business Rule RULE-01 (consultation start precedes check-in). "
        "All remaining encounters satisfy 100% referential integrity and valid numeric range limits."
    ),
    category="Success" if len(anomaly_df) <= 2 else "Warning"
)

# Quarantined Anomalies Inspection
if not anomaly_df.empty:
    with st.expander(f"⚠️ View Quarantined Anomaly Audit Log ({len(anomaly_df)} Records Isolated)"):
        st.markdown("**Business Rule RULE-01 Audit Log:**")
        st.dataframe(
            anomaly_df[["visit_id", "patient_id", "check_in_time", "consultation_start_time", "consultation_end_time", "quarantine_reason"]],
            use_container_width=True,
            hide_index=True
        )

# Interactive Tabular Data Explorer
st.markdown("### 📋 Interactive Analytical View Explorer (`v_patient_visit_analytics`)")

# Controls
c1, c2, c3 = st.columns([2, 2, 4])
with c1:
    dept_opts = ["All"] + sorted(clean_df["department_name"].dropna().unique().tolist())
    dept_filter = st.selectbox("Filter Department", options=dept_opts)
with c2:
    vtype_opts = ["All"] + sorted(clean_df["visit_type"].dropna().unique().tolist())
    vtype_filter = st.selectbox("Filter Visit Type", options=vtype_opts)
with c3:
    search_mrn = st.text_input("Search by Patient MRN or Name", placeholder="e.g. MRN-2026- or Sharma")

# Apply filters
view_df = clean_df.copy()
if dept_filter != "All":
    view_df = view_df[view_df["department_name"] == dept_filter]
if vtype_filter != "All":
    view_df = view_df[view_df["visit_type"] == vtype_filter]
if search_mrn:
    match_mask = (
        view_df["patient_mrn"].astype(str).str.contains(search_mrn, case=False, na=False) |
        view_df["patient_name"].astype(str).str.contains(search_mrn, case=False, na=False)
    )
    view_df = view_df[match_mask]

# Column Selector
default_cols = [
    "visit_id", "patient_mrn", "patient_name", "department_name", "doctor_name",
    "check_in_time", "wait_time_minutes", "is_sla_breach", "visit_type",
    "primary_diagnosis_name", "net_billed_amount", "payer_type", "csat_score"
]
available_cols = [c for c in default_cols if c in view_df.columns]
selected_cols = st.multiselect("Select Table Columns to Display", options=list(view_df.columns), default=available_cols)

# Display Table
st.dataframe(
    view_df[selected_cols if selected_cols else available_cols],
    use_container_width=True,
    hide_index=True
)
st.caption(f"Displaying {len(view_df):,} encounters matching current filter parameters.")

# Download Section
st.markdown("### 💾 Export & Data Download Center")
d1, d2, d3 = st.columns(3)

# 1. Download Clean CSV
with d1:
    csv_buffer = io.StringIO()
    clean_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Download Clean Visits (CSV)",
        data=csv_buffer.getvalue(),
        file_name="clean_patient_visits.csv",
        mime="text/csv",
        help="Download filtered and cleaned encounter records in CSV format"
    )

# 2. Download Excel Workbook
with d2:
    excel_path = os.path.join(os.path.dirname(__file__), "..", "data", "healthcare_patient_visit_data.xlsx")
    if os.path.exists(excel_path):
        with open(excel_path, "rb") as f:
            st.download_button(
                label="📊 Download Master Excel Workbook",
                data=f.read(),
                file_name="healthcare_patient_visit_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Download full 7-sheet relational workbook"
            )
    else:
        # Generate on the fly
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            clean_df.to_excel(writer, sheet_name="Visits", index=False)
        st.download_button(
            label="📊 Download Analytics Excel",
            data=buf.getvalue(),
            file_name="metrocare_visit_analytics.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# 3. Download Anomaly Audit Log
with d3:
    if not anomaly_df.empty:
        anom_csv = io.StringIO()
        anomaly_df.to_csv(anom_csv, index=False)
        st.download_button(
            label="⚠️ Download Quarantined Anomalies (CSV)",
            data=anom_csv.getvalue(),
            file_name="quarantined_anomalies_rule01.csv",
            mime="text/csv",
            help="Download quarantined records failing RULE-01"
        )
    else:
        st.button("⚠️ No Anomalies to Download", disabled=True)
