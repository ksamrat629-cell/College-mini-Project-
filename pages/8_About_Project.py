"""
Page 8: Project Governance, Academic Attribution & Architectural Lineage
MetroCare Health Systems | Operational Intelligence Platform
MCA Capstone Project 2026 | ABES Engineering College
"""

import textwrap
import streamlit as st
import pandas as pd
from src.ui import render_tailwind_header, render_kpi_grid, render_insight_box

st.set_page_config(page_title="About & Governance | MetroCare", page_icon="ℹ️", layout="wide")

# Header
render_tailwind_header(
    title="Project Governance, Attribution & Architecture",
    subtitle="MCA Capstone Project 2026 | ABES Engineering College, Ghaziabad | Department of Computer Applications",
    badge_text="Academic Capstone",
    badge_color="bg-emerald-100 text-emerald-800"
)

# Academic Credentials Grid
kpis = [
    {
        "title": "Candidate Author",
        "value": "US Samrat",
        "subtext": "Roll No: 2500320140158",
        "badge_text": "MCA 2nd Year",
        "badge_color": "bg-blue-100 text-blue-800"
    },
    {
        "title": "Academic Mentor",
        "value": "Prof. Anjali Pandey",
        "subtext": "Dept of Computer Applications",
        "badge_text": "Faculty Guide",
        "badge_color": "bg-purple-100 text-purple-800"
    },
    {
        "title": "Case Study Organisation",
        "value": "MetroCare Health",
        "subtext": "450-Bed Tertiary Care Hospital",
        "badge_text": "Delhi NCR",
        "badge_color": "bg-emerald-100 text-emerald-800"
    },
    {
        "title": "SDLC Verification",
        "value": "100% Passed",
        "subtext": "14 Automated Pytest Tests",
        "badge_text": "Verified",
        "badge_color": "bg-emerald-100 text-emerald-800"
    }
]
render_kpi_grid(kpis)

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🏛️ Academic Institutional Details")
    st.markdown(
        textwrap.dedent("""
        - **Institution:** ABES Engineering College, Ghaziabad, Uttar Pradesh (College Code: 032)
        - **Affiliating University:** Dr. A.P.J. Abdul Kalam Technical University (AKTU), Lucknow
        - **Program:** Master of Computer Applications (MCA) — 2 Year Full-Time Degree
        - **Specialization Stream:** Data Analytics & Clinical Operational Intelligence
        - **Academic Session:** 2024–2026
        - **Project Title:** *Healthcare Patient Visit Analysis & Operational Intelligence Platform*
        - **Supervisory Faculty:** Prof. Anjali Pandey, Assistant Professor, Department of Computer Applications
        """).strip()
    )
    
    st.markdown("### 🛠️ Approved Technology Stack")
    st.markdown(
        textwrap.dedent("""
        - **Core Language:** Python 3.12 / 3.11
        - **Data Processing & Manipulation:** pandas `2.2.3`, NumPy `1.26.4`
        - **Inferential Statistical Engine:** SciPy `1.14.1` (One-Way ANOVA, Kruskal-Wallis, Chi-Square), statsmodels `0.14.4` (OLS)
        - **Interactive Visualization:** Plotly Express & Plotly Graph Objects `5.24.1`
        - **Application Framework:** Streamlit Multipage `1.40.2`
        - **UI/UX Design System:** Tailwind CSS CDN embedded via `st.iframe` (isolated shadow DOM)
        - **Relational Data Layer:** SQLite3 ACID-compliant embedded database (`data/app.db`)
        - **Testing & Quality Assurance:** pytest `8.3.3`, Streamlit AppTest framework
        - **Version Control & Hosting:** Git, GitHub, Streamlit Community Cloud
        """).strip()
    )

with col2:
    st.markdown("### 📐 System Architectural Pipeline")
    st.markdown(
        textwrap.dedent("""
        ```mermaid
        flowchart TD
            subgraph L1["Layer 1: Relational Data Mart"]
                DB[("data/app.db<br/>(SQLite 3NF Schema)")]
                CSV["data/*.csv &<br/>healthcare_patient_visit_data.xlsx"]
            end

            subgraph L2["Layer 2: Ingestion & Cache Engine"]
                DL["src/data_loader.py<br/>(@st.cache_data ttl=3600)"]
                DC["src/data_cleaner.py<br/>(RULE-01 Anomaly Quarantine)"]
            end

            subgraph L3["Layer 3: Analytical & Statistical Engine"]
                AN["src/analytics.py<br/>(Wait SLA, No-Show, Recovery)"]
                ST["src/stats.py<br/>(ANOVA, Chi2, Pearson r)"]
            end

            subgraph L4["Layer 4: Presentation & UI Layer"]
                UI["src/ui.py<br/>(Tailwind CDN in st.iframe)"]
                APP["app.py & pages/1..8<br/>(Interactive Multipage App)"]
            end

            DB --> DL
            CSV -.-> DB
            DL --> DC
            DC --> AN
            DC --> ST
            AN --> APP
            ST --> APP
            UI --> APP
        ```
        """).strip()
    )

st.markdown("---")
st.markdown("### 📋 18-Step SDLC Project Deliverables Matrix")

sdlc_steps = [
    ("Step 01", "Project Understanding & Stakeholder Needs", "docs/01_Project_Understanding.docx", "6 Stakeholders (SH-01..06), 10 OQs (OQ-01..10) defined", "Approved"),
    ("Step 02", "HMW Opportunity Framework", "docs/02_HMW_Statements.docx", "10 How-Might-We innovation statements established", "Approved"),
    ("Step 03", "Needs Analysis & Business Requirements", "docs/03_Needs_Analysis.docx", "13 BRs in BABOK syntax with MoSCoW prioritization", "Approved"),
    ("Step 04", "Requirements Traceability Matrix (RTM)", "docs/04_Traceability_Matrix.xlsx", "Master 12-column bidirectional traceability matrix", "Approved"),
    ("Step 05", "Business Requirements Document (BRD)", "docs/05_BRD.docx", "Executive BRD, RACI matrix, 8 business rules (RULE-01..08)", "Approved"),
    ("Step 07", "Technical Requirements Document (TRD)", "docs/07_TRD.docx", "Mermaid architecture, FR-01..13, statistical mappings", "Approved"),
    ("Step 08", "Database Design & Data Dictionary", "docs/08_Database_Design.xlsx", "3NF relational schema, 6 tables, analytical view, DDL", "Approved"),
    ("Step 09", "Entity Relationship (ER) Diagram", "docs/09_ER_Diagram.docx / .png", "Crow's foot ER diagram, cardinalities, business rule enforcement", "Approved"),
    ("Step 10", "Synthetic Healthcare Dataset Generation", "data/app.db / .xlsx / .csv", "SQLite DB (seed 42), 5 embedded patterns, quality anomaly", "Approved"),
    ("Step 11", "Agile User Stories & Sprint Plan", "docs/11_User_Stories.docx", "15 User Stories (US-01..15), Given/When/Then criteria", "Approved"),
    ("Step 12", "UI/UX Framework & Design System", "docs/12_UI_Framework.docx", "8 UI screens, ASCII wireframes, Tailwind CDN components", "Approved"),
    ("Step 13", "QA Test Cases Specification", "docs/13_Test_Cases.docx / tests/", "15 Functional + 14 Technical tests (100% pytest pass)", "Approved"),
    ("Step 14", "Build Plan & Engineering Blueprint", "BUILD_PLAN.md / docs/14_Build_Plan.docx", "Task backlog BUILD-01..15, DoD, commands, viva prep", "Approved"),
    ("Step 15", "System Build, Testing & Verification", "All pages/ & docs/15_Build_Test_Log.docx", "Working multi-page Streamlit application, 100% test pass", "Completed")
]

sdlc_df = pd.DataFrame(sdlc_steps, columns=["Phase", "Deliverable Name", "Artifact Reference", "Key Focus / Milestone Scope", "Status"])
st.dataframe(sdlc_df, use_container_width=True, hide_index=True)

render_insight_box(
    title="Bidirectional Lineage Guarantee",
    text="Every single metric, visualization, filter control, and database column traces directly back to an initial Stakeholder Operational Question (OQ) and Business Requirement (BR) via the master Traceability Matrix (docs/04_Traceability_Matrix.xlsx).",
    category="Info"
)
