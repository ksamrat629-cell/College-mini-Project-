"""
Page 5: Revenue Realization, Payer Mix & Financial Recovery Simulator
MetroCare Health Systems | Operational Intelligence Platform
US-07, US-08 | Features F-07, F-08
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_analytics_view, load_all_tables
from src.data_cleaner import clean_analytics_data
from src.analytics import compute_revenue_payer_mix, compute_no_show_matrix, simulate_no_show_recovery
from src.ui import render_tailwind_header, render_kpi_grid, render_insight_box

st.set_page_config(page_title="Revenue & Payer Mix | MetroCare", page_icon="💰", layout="wide")

# Header
render_tailwind_header(
    title="Revenue Realization, Payer Mix & Financial Simulator",
    subtitle="Billing realization, Insurance vs Cash distributions, and dynamic no-show slot recovery simulation",
    badge_text="Financial Intelligence",
    badge_color="bg-emerald-100 text-emerald-800"
)

# Load data
raw_df = load_analytics_view()
clean_df, _ = clean_analytics_data(raw_df)
tables = load_all_tables()
appts_df = tables["appointments"].copy()

# Sidebar filters
st.sidebar.markdown("### 🎛️ Financial Cohort Filters")
payers = sorted(clean_df["payer_type"].dropna().unique().tolist()) if "payer_type" in clean_df.columns else []
selected_payers = st.sidebar.multiselect("Payer Categories", options=payers, default=payers) if payers else []

depts = sorted(clean_df["department_name"].dropna().unique().tolist())
selected_depts = st.sidebar.multiselect("Departments", options=depts, default=depts)

filtered_df = clean_df[
    (clean_df["department_name"].isin(selected_depts if selected_depts else depts))
].copy()
if selected_payers and "payer_type" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["payer_type"].isin(selected_payers)]

# Compute Financial KPIs
rev_metrics = compute_revenue_payer_mix(filtered_df)
gross = rev_metrics["gross_revenue"]
net = rev_metrics["net_revenue"]
discounts = rev_metrics["discount_total"]
avg_rev = rev_metrics["avg_rev_per_visit"]

kpis = [
    {
        "title": "Gross Billed Revenue",
        "value": f"₹{gross:,.2f}",
        "subtext": "Pre-discount Encounter Charges",
        "badge_text": "Billed",
        "badge_color": "bg-blue-100 text-blue-800"
    },
    {
        "title": "Discounts & Waivers",
        "value": f"₹{discounts:,.2f}",
        "subtext": f"{(discounts / gross * 100.0 if gross > 0 else 0):.1f}% of Gross Billed",
        "badge_text": "Deductions",
        "badge_color": "bg-amber-100 text-amber-800"
    },
    {
        "title": "Net Realized Revenue",
        "value": f"₹{net:,.2f}",
        "subtext": "Hospital Actual Realization",
        "badge_text": "Collected",
        "badge_color": "bg-emerald-100 text-emerald-800"
    },
    {
        "title": "Average Revenue / Visit",
        "value": f"₹{avg_rev:,.2f}",
        "subtext": f"Across {len(filtered_df):,} Encounters",
        "badge_text": "Per Encounter",
        "badge_color": "bg-purple-100 text-purple-800"
    }
]
render_kpi_grid(kpis)

# Layout: 2 Columns for Visuals
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🍩 Revenue Distribution by Payer Category")
    payer_df = rev_metrics["payer_df"]
    if not payer_df.empty:
        fig_donut = px.pie(
            payer_df,
            values="total_amount",
            names="payer_type" if "payer_type" in payer_df.columns else payer_df.columns[0],
            hole=0.45,
            color_discrete_sequence=["#2B6CB0", "#10B981", "#F59E0B", "#8B5CF6"]
        )
        fig_donut.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            margin=dict(l=20, r=20, t=30, b=30),
            height=370
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("Payer category data not available.")

with col2:
    st.markdown("#### 🏢 Department Revenue Realization Breakdown")
    dept_rev = filtered_df.groupby("department_name")["net_billed_amount"].sum().reset_index()
    dept_rev = dept_rev.sort_values("net_billed_amount", ascending=True)
    
    fig_bar = px.bar(
        dept_rev,
        y="department_name",
        x="net_billed_amount",
        orientation="h",
        color="net_billed_amount",
        color_continuous_scale="Teal",
        labels={"net_billed_amount": "Net Realized Revenue (₹)", "department_name": "Department"}
    )
    fig_bar.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        height=370,
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Interactive Capacity Recovery Simulator
st.markdown("---")
st.markdown("### 🎚️ Interactive No-Show Financial Recovery Simulator")
st.markdown("Simulate financial recovery by mitigating appointment no-shows via automated WhatsApp/SMS reminders and deposit requirements.")

# Compute unfulfilled appointments
ns_overall = compute_no_show_matrix(appts_df)
unfulfilled_slots = ns_overall["unfulfilled"]

sim_col1, sim_col2 = st.columns([2, 3])

with sim_col1:
    recovery_slider = st.slider(
        "Projected No-Show Reduction Target (%)",
        min_value=0,
        max_value=100,
        value=30,
        step=5,
        help="Target percentage of unfulfilled slots converted into completed visits"
    )
    
    sim_result = simulate_no_show_recovery(unfulfilled_slots, avg_rev, recovery_slider)
    
    st.metric(
        label="Projected Revenue Recovery",
        value=f"₹{sim_result['recovered_revenue']:,.2f}",
        delta=f"+{sim_result['recovered_slots']} recovered consultations",
        delta_color="normal"
    )

with sim_col2:
    st.markdown(
        f"""
        <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 12px; padding: 18px;">
            <div style="font-weight: 700; color: #1E293B; font-size: 15px;">💡 Simulator Dynamics & ROI Analysis</div>
            <div style="font-size: 13px; color: #475569; margin-top: 8px; line-height: 1.6;">
                • <b>Baseline Unfulfilled Appointments:</b> {unfulfilled_slots} slots ({ns_overall['no_show_rate']:.1f}% no-show rate)<br>
                • <b>Target Mitigation:</b> {recovery_slider}% reduction target<br>
                • <b>Recovered Capacity:</b> <b>{sim_result['recovered_slots']} patient consultations</b> restored to OPD clinics<br>
                • <b>Recovered Net Revenue:</b> <span style="color: #0D9488; font-weight: bold; font-size: 16px;">₹{sim_result['recovered_revenue']:,.2f}</span> (calculated at ₹{avg_rev:,.2f} avg yield/visit)<br>
                • <b>Implementation Strategy:</b> 2-way WhatsApp appointment confirmations 48h prior + dynamic overbooking during peak morning hours.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Detailed Payer Settlement Audit Table
st.markdown("#### 📋 Payer Category Settlement Summary")
if "payer_type" in filtered_df.columns:
    payer_table = filtered_df.groupby("payer_type").agg(
        encounters=("visit_id", "count"),
        gross_billed=("gross_billed_amount", "sum"),
        discounts=("discount_amount", "sum"),
        net_collected=("net_billed_amount", "sum")
    ).reset_index()
    payer_table["avg_per_visit"] = (payer_table["net_collected"] / payer_table["encounters"]).round(2)
    payer_table["collection_rate"] = (payer_table["net_collected"] / payer_table["gross_billed"] * 100.0).round(1)
    
    st.dataframe(
        payer_table.style.format({
            "encounters": "{:,}",
            "gross_billed": "₹{:,.2f}",
            "discounts": "₹{:,.2f}",
            "net_collected": "₹{:,.2f}",
            "avg_per_visit": "₹{:,.2f}",
            "collection_rate": "{:.1f}%"
        }),
        use_container_width=True,
        hide_index=True
    )
