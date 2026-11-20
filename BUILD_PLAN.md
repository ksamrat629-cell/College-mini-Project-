# BUILD PLAN: Healthcare Patient Visit Analysis Platform

> **Author:** US Samrat | **Roll No:** 2500320140158 (MCA 2nd Year Data Analytics, ABES Engineering College)  
> **Mentor:** Prof. Anjali Pandey | **Client / Case Study:** MetroCare Health Systems  
> **Deployment Target:** Streamlit Community Cloud (Public GitHub Repo)  
> **Target Execution Standard:** Step-by-Step Task Backlog for AI / Engineering Pair Programming (Step 15 Input)

---

## 1. Project Summary & Document Architecture

1. The Healthcare Patient Visit Analysis platform is an enterprise-grade operational intelligence system for MetroCare Health Systems.
2. It monitors patient flow, appointment attendance, queue dynamics, doctor workloads, and financial realization across 8 departments.
3. Designed by US Samrat under the mentorship of Prof. Anjali Pandey at ABES Engineering College, Ghaziabad.
4. Built with Python 3.12, pandas, NumPy, SciPy, statsmodels, Plotly, Streamlit Multipage, and Tailwind CSS CDN.
5. Employs a 3NF normalized SQLite database (`data/app.db`) with 5,000+ realistic synthetic encounters and 100% foreign key integrity.
6. Solves excessive patient wait times (>45 mins), high appointment no-shows (20%), and billing opacity across private/government payers.
7. Enforces a strict 30-minute wait time SLA benchmark and tracks 30-day unplanned hospital readmissions with zero PII/PHI.
8. Fully verified via automated pytest unit tests, mathematical formula verifications on tiny datasets, and Streamlit AppTest.
9. Deploys seamlessly to Streamlit Community Cloud with sub-second query latency powered by `@st.cache_data`.
10. All artifacts are governed by bidirectional traceability across 18 SDLC phases documented below.

### Master Document Directory Links
* **Step 1 (Project Understanding):** [`docs/01_Project_Understanding.docx`](file:///C:/Users/ksamr/OneDrive/Desktop/HealthCare%20Patient%20visit%20analysis/docs/01_Project_Understanding.docx)
* **Step 2 (HMW Opportunity Statements):** [`docs/02_HMW_Statements.docx`](file:///C:/Users/ksamr/OneDrive/Desktop/HealthCare%20Patient%20visit%20analysis/docs/02_HMW_Statements.docx)
* **Step 3 (Needs Analysis & BRs):** [`docs/03_Needs_Analysis.docx`](file:///C:/Users/ksamr/OneDrive/Desktop/HealthCare%20Patient%20visit%20analysis/docs/03_Needs_Analysis.docx)
* **Step 4 (Traceability Matrix):** [`docs/04_Traceability_Matrix.xlsx`](file:///C:/Users/ksamr/OneDrive/Desktop/HealthCare%20Patient%20visit%20analysis/docs/04_Traceability_Matrix.xlsx)
* **Step 5 (Business Requirements Document):** [`docs/05_BRD.docx`](file:///C:/Users/ksamr/OneDrive/Desktop/HealthCare%20Patient%20visit%20analysis/docs/05_BRD.docx)
* **Step 7 (Technical Design Document):** [`docs/07_TRD.docx`](file:///C:/Users/ksamr/OneDrive/Desktop/HealthCare%20Patient%20visit%20analysis/docs/07_TRD.docx)
* **Step 8 (Database Design Specification):** [`docs/08_Database_Design.xlsx`](file:///C:/Users/ksamr/OneDrive/Desktop/HealthCare%20Patient%20visit%20analysis/docs/08_Database_Design.xlsx)
* **Step 9 (Entity Relationship Model):** [`docs/09_ER_Diagram.docx`](file:///C:/Users/ksamr/OneDrive/Desktop/HealthCare%20Patient%20visit%20analysis/docs/09_ER_Diagram.docx) | Image: [`docs/09_ER_Diagram.png`](file:///C:/Users/ksamr/OneDrive/Desktop/HealthCare%20Patient%20visit%20analysis/docs/09_ER_Diagram.png)
* **Step 10 (Synthetic Data Mart):** [`data/app.db`](file:///C:/Users/ksamr/OneDrive/Desktop/HealthCare%20Patient%20visit%20analysis/data/app.db) | Excel: [`data/healthcare_patient_visit_data.xlsx`](file:///C:/Users/ksamr/OneDrive/Desktop/HealthCare%20Patient%20visit%20analysis/data/healthcare_patient_visit_data.xlsx) | Report: [`data/validation_report.txt`](file:///C:/Users/ksamr/OneDrive/Desktop/HealthCare%20Patient%20visit%20analysis/data/validation_report.txt)
* **Step 11 (Agile User Stories):** [`docs/11_User_Stories.docx`](file:///C:/Users/ksamr/OneDrive/Desktop/HealthCare%20Patient%20visit%20analysis/docs/11_User_Stories.docx)
* **Step 12 (UI/UX Framework):** [`docs/12_UI_Framework.docx`](file:///C:/Users/ksamr/OneDrive/Desktop/HealthCare%20Patient%20visit%20analysis/docs/12_UI_Framework.docx)
* **Step 13 (QA Test Cases Specification):** [`docs/13_Test_Cases.docx`](file:///C:/Users/ksamr/OneDrive/Desktop/HealthCare%20Patient%20visit%20analysis/docs/13_Test_Cases.docx)

---

## 2. Final Repository & Codebase Hierarchy

```text
HealthCare Patient visit analysis/
├── .streamlit/
│   └── config.toml                  # Streamlit healthcare theme, server & headless flags
├── data/
│   ├── app.db                       # Relational SQLite database (ACID compliant)
│   ├── healthcare_patient_visit_data.xlsx # Master 7-sheet workbook
│   ├── departments.csv              # Master department reference
│   ├── doctors.csv                  # Master doctor reference
│   ├── patients.csv                 # Master patient cohort
│   ├── appointments.csv             # Scheduling & attendance fact
│   ├── visits.csv                   # Clinical encounter fact
│   ├── billing.csv                  # Financial settlement fact
│   └── validation_report.txt        # Automated data validation log
├── docs/
│   ├── 01_Project_Understanding.docx
│   ├── 02_HMW_Statements.docx
│   ├── 03_Needs_Analysis.docx
│   ├── 04_Traceability_Matrix.xlsx  # FINAL End-to-End RTM
│   ├── 05_BRD.docx
│   ├── 07_TRD.docx
│   ├── 08_Database_Design.xlsx
│   ├── 09_ER_Diagram.docx
│   ├── 09_ER_Diagram.png
│   ├── 11_User_Stories.docx
│   ├── 12_UI_Framework.docx
│   ├── 13_Test_Cases.docx
│   └── 14_Build_Plan.docx
├── pages/
│   ├── 1_Executive_Overview.py       # Macro hospital volume, 24-hr peak arrival, CSAT correlation
│   ├── 2_Queue_Wait_Times.py         # Registration wait times, 30-min SLA alerts, consult duration
│   ├── 3_No_Show_Analytics.py        # Lead time, age, booking channel risk & lost revenue
│   ├── 4_Clinical_Readmissions.py    # Top 10 ICD-10 diagnoses, seasonal trends, 30-day readmissions
│   ├── 5_Revenue_Payer_Mix.py        # Gross billing, Insurance vs Cash, specialty financial contribution
│   ├── 6_Doctor_Workload.py          # Physician slot utilization & Walk-in vs Pre-booked rostering
│   ├── 7_Data_Explorer.py            # Self-service tabular explorer, quality audit & multi-format export
│   └── 8_About_Project.py            # Academic metadata, SDLC traceability & architecture docs
├── src/
│   ├── __init__.py
│   ├── data_loader.py               # SQLite connection, cached query functions via @st.cache_data
│   ├── data_cleaner.py              # Schema validation, timestamp parsing, anomaly quarantine (RULE-01)
│   ├── analytics.py                 # Core business aggregations, metrics, recovery simulation formulas
│   ├── stats.py                     # Inferential statistics: One-Way ANOVA, Chi-Square, Pearson r, OLS
│   └── ui.py                        # Tailwind CSS CDN components, header banner, responsive KPI cards
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures: mock DataFrames and database connections
│   ├── test_data.py                 # DB connection, counts, PK uniqueness, FK checks, query latency
│   ├── test_analysis.py             # Math formula assertions on tiny datasets, ANOVA, Pearson r
│   └── test_app.py                  # UI module assertions, theme configuration, Streamlit AppTest
├── .gitignore
├── app.py                           # Application main script, persistent global sidebar navigation
├── BUILD_PLAN.md                    # Current engineering execution blueprint
├── README.md                        # Deployment & architectural documentation
└── requirements.txt                 # Strictly pinned Python package dependencies
```

---

## 3. Step-by-Step Build Task Backlog (BUILD-01 to BUILD-15)

### **BUILD-01: Environment & Pinned Dependency Lock**
* **Goal:** Establish strict environment dependencies and Streamlit theme configuration.
* **Target Files:** `requirements.txt`, `.streamlit/config.toml`
* **Linked US / Features:** `US-14` / `F-12`
* **Exact Prompt for AI:** *"Create requirements.txt with pinned versions: streamlit==1.40.2, plotly==5.24.1, pandas==2.2.3, numpy==1.26.4, scipy==1.14.1, statsmodels==0.14.4, pytest==8.3.3, openpyxl==3.1.5, python-docx==1.2.0. Create .streamlit/config.toml with primaryColor='#2B6CB0', backgroundColor='#F8FAFC', textColor='#1E293B'."*
* **How to Check:** Run `pip install -r requirements.txt` and verify exit code 0.
* **Tests That Must Pass:** `tests/test_app.py::test_config_toml_theme_presence`

### **BUILD-02: Data Ingestion & Anomaly Cleaning Engine**
* **Goal:** Connect to SQLite database, cache queries via `@st.cache_data`, and isolate timestamp anomalies (`RULE-01`).
* **Target Files:** `src/data_loader.py`, `src/data_cleaner.py`
* **Linked US / Features:** `US-13` / `F-01`
* **Exact Prompt for AI:** *"Implement src/data_loader.py with read-only SQLite URI 'file:data/app.db?mode=ro' and @st.cache_data(ttl=3600). Create src/data_cleaner.py to parse datetimes and filter out records where consultation_start < check_in (RULE-01), returning clean DataFrames and an anomaly log."*
* **How to Check:** Execute python snippet loading 280 rows with 1 isolated anomaly.
* **Tests That Must Pass:** `tests/test_data.py::test_database_connection_and_table_presence`, `test_cleaning_rule_01_timestamp_anomaly`

### **BUILD-03: Analytical Aggregations & Statistical Computing Engine**
* **Goal:** Build reusable mathematical aggregation pipelines and inferential statistical routines.
* **Target Files:** `src/analytics.py`, `src/stats.py`
* **Linked US / Features:** `US-01` to `US-11` / `F-01` to `F-11`
* **Exact Prompt for AI:** *"Write src/analytics.py providing compute_department_throughput, compute_no_show_matrix, compute_wait_time_sla, compute_consultation_duration, compute_readmission_rate, compute_revenue_payer_mix, and compute_doctor_utilization. Write src/stats.py providing calculate_wait_time_anova, calculate_no_show_chi2, and calculate_csat_pearson."*
* **How to Check:** Verify all functions return deterministic dictionaries/DataFrames with no NaNs.
* **Tests That Must Pass:** `tests/test_analysis.py::test_wait_time_and_sla_breach_calculation_on_known_dataset`, `test_statistical_anova_and_correlation_functions`

### **BUILD-04: Reusable Tailwind UI Design System**
* **Goal:** Deliver hospital-executive header banners, KPI metric grids, and alert badges using Tailwind CSS CDN via isolated iframes.
* **Target Files:** `src/ui.py`
* **Linked US / Features:** `US-12` / `F-12`
* **Exact Prompt for AI:** *"Build src/ui.py with render_tailwind_header, render_kpi_card, render_kpi_grid, and render_insight_box using st.components.v1.html and Tailwind CDN. Ensure zero styling conflicts with Streamlit."*
* **How to Check:** Render a test card in Streamlit and verify font and borders render cleanly.
* **Tests That Must Pass:** `tests/test_app.py::test_ui_module_components`

### **BUILD-05: Application Entrypoint & Global State Management**
* **Goal:** Build the main application script with persistent sidebar navigation and summary metrics.
* **Target Files:** `app.py`
* **Linked US / Features:** `US-01`, `US-13` / `F-01`
* **Exact Prompt for AI:** *"Build app.py with wide layout, sidebar operational controls, quick summary KPI cards (Total Visits, Avg Wait, No-Show %, Readmission %), and navigation instructions to the multi-page modules."*
* **How to Check:** Run `streamlit run app.py` and inspect browser rendering at localhost:8501.
* **Tests That Must Pass:** `tests/test_app.py::test_streamlit_apptest_startup`

### **BUILD-06: Page 1 — Executive Overview & Volume Curves**
* **Goal:** Deliver macro hospital throughput, 24-hr peak arrival histogram, CSAT correlation scatter, and breach table.
* **Target Files:** `pages/1_Executive_Overview.py`
* **Linked US / Features:** `US-01`, `US-10`, `US-12` / `F-01`, `F-10`, `F-12`
* **Exact Prompt for AI:** *"Create pages/1_Executive_Overview.py. Load filtered records from src/data_loader.py, display Tailwind KPI cards, Plotly 24-hr arrival volume bar chart with red peak threshold, Plotly CSAT vs Wait Time scatter plot with OLS trendline, and an operational exception alert table."*
* **How to Check:** Confirm morning surge (09:00–11:30) is highlighted and regression line shows $r \approx -0.68$.
* **Tests That Must Pass:** `TC-F-01`, `TC-F-02`, `TC-F-12`, `TC-T-13`

### **BUILD-07: Page 2 — Queue Dynamics & 30-Minute Wait SLA Benchmark**
* **Goal:** Monitor wait times against 30m SLA, display departmental breaches in crimson, and show duration box plots.
* **Target Files:** `pages/2_Queue_Wait_Times.py`
* **Linked US / Features:** `US-03`, `US-04`, `US-12` / `F-03`, `F-04`, `F-12`
* **Exact Prompt for AI:** *"Create pages/2_Queue_Wait_Times.py with mean/median/90th percentile wait KPIs, a horizontal Plotly bar chart with red 30-minute benchmark line, ANOVA F-statistic display, and consultation duration box plots across the 4 visit types."*
* **How to Check:** Verify Cardiology and Orthopedics display red "SLA Breach" cards while ENT is compliant.
* **Tests That Must Pass:** `TC-F-03`, `TC-F-04`, `TC-F-13`, `TC-T-06`

### **BUILD-08: Page 3 — Appointment Attendance & No-Show Risk Analytics**
* **Goal:** Visualize no-show risk across lead times, booking channels, and age groups with interactive risk heatmap.
* **Target Files:** `pages/3_No_Show_Analytics.py`
* **Linked US / Features:** `US-02`, `US-15` / `F-02`, `F-13`
* **Exact Prompt for AI:** *"Create pages/3_No_Show_Analytics.py. Display overall no-show rate KPI, a Plotly 2D heatmap matrix (Lead Time Bins vs Age Groups), booking channel donut chart, and Chi-square independence test results."*
* **How to Check:** Verify Call Center bookings with $>10$ days lead time display $>30\%$ no-show probability.
* **Tests That Must Pass:** `TC-F-05`, `TC-T-07`

### **BUILD-09: Page 4 — Clinical Diagnoses, ICD-10 & 30-Day Readmissions**
* **Goal:** Display Pareto chart of top 10 ICD-10 diagnoses, monthly epidemic area chart, and 30-day readmissions.
* **Target Files:** `pages/4_Clinical_Readmissions.py`
* **Linked US / Features:** `US-05`, `US-06` / `F-05`, `F-06`
* **Exact Prompt for AI:** *"Create pages/4_Clinical_Readmissions.py. Compute 30-day readmissions via self-join query, display readmission % KPI (target <8%), top 10 diagnoses Pareto chart with cumulative line, and monthly stacked area chart comparing acute vs chronic conditions."*
* **How to Check:** Verify planned follow-ups are excluded from readmissions and Pareto chart sums to 100%.
* **Tests That Must Pass:** `TC-F-06`, `TC-F-07`, `TC-T-09`

### **BUILD-10: Page 5 — Revenue Realization, Payer Mix & Recovery Simulator**
* **Goal:** Audit gross billing by payer tier (Self-Pay, TPA, Govt schemes) and provide interactive no-show recovery slider.
* **Target Files:** `pages/5_Revenue_Payer_Mix.py`
* **Linked US / Features:** `US-07`, `US-08` / `F-07`, `F-08`
* **Exact Prompt for AI:** *"Create pages/5_Revenue_Payer_Mix.py with gross billing, average revenue per visit, and payer mix donut chart. Implement an interactive capacity recovery slider (0% to 100% no-show reduction) dynamically calculating recovered INR revenue."*
* **How to Check:** Moving slider from 0% to 50% updates recovery metric by +₹42,300 instantaneously.
* **Tests That Must Pass:** `TC-F-08`, `TC-F-09`

### **BUILD-11: Page 6 — Doctor Workload, Capacity & Rostering**
* **Goal:** Evaluate physician utilization gauges and compare Walk-in vs. Pre-booked 7-day arrival curves for shift rostering.
* **Target Files:** `pages/6_Doctor_Workload.py`
* **Linked US / Features:** `US-09`, `US-11` / `F-09`, `F-11`
* **Exact Prompt for AI:** *"Create pages/6_Doctor_Workload.py. Render diverging bar chart of clinician utilization (% of scheduled hours), highlight doctors >95% (burnout) and <50% (idle), and plot 7-day hourly line chart comparing Walk-in vs Pre-booked arrivals with counter staffing recommendations."*
* **How to Check:** Verify 3 overburdened doctors are tagged with warning alerts and walk-in morning curve peaks at 10:00 AM.
* **Tests That Must Pass:** `TC-F-10`, `TC-F-11`, `TC-T-08`

### **BUILD-12: Page 7 — Self-Service Data Explorer & Quality Audit**
* **Goal:** Interactive tabular data explorer with column selector, data quality audit metrics, and CSV/Excel downloads.
* **Target Files:** `pages/7_Data_Explorer.py`
* **Linked US / Features:** `US-13`, `US-14` / `F-01`
* **Exact Prompt for AI:** *"Create pages/7_Data_Explorer.py. Render data quality summary metrics (missing values, isolated anomalies, duplicate checks), an interactive st.dataframe with multi-column filtering, and download buttons for visits.csv and healthcare_patient_visit_data.xlsx."*
* **How to Check:** Filter records, sort columns, and click download buttons to verify valid files are downloaded.
* **Tests That Must Pass:** `TC-F-14`, `TC-F-15`

### **BUILD-13: Page 8 — Project Governance, Traceability & Academic About**
* **Goal:** Institutional project documentation, student attribution (US Samrat), mentor attribution (Prof. Anjali Pandey), and RTM overview.
* **Target Files:** `pages/8_About_Project.py`
* **Linked US / Features:** Governance & Viva Support
* **Exact Prompt for AI:** *"Create pages/8_About_Project.py displaying college affiliation (ABES Engineering College), student roll number (2500320140158), mentor attribution, project architecture diagram, SDLC milestone progress, and technology stack badges."*
* **How to Check:** Verify all academic credentials and architecture descriptions match Step 1–13 specifications.
* **Tests That Must Pass:** `test_app.py::test_streamlit_apptest_startup`

### **BUILD-14: Comprehensive Automated Test Execution & Regression Harness**
* **Goal:** Run the full pytest suite and verify 100% passing status across all unit, analytical, and AppTest cases.
* **Target Files:** `tests/test_data.py`, `tests/test_analysis.py`, `tests/test_app.py`
* **Linked US / Features:** `US-14` / All Features
* **Exact Prompt for AI:** *"Execute pytest tests/ -v and assert all 14 technical tests pass with zero failures and zero unhandled warnings."*
* **How to Check:** Terminal output reports `14 passed in <45s`.
* **Tests That Must Pass:** `TC-T-01` through `TC-T-14` (All Pass)

### **BUILD-15: Production README & Streamlit Cloud Deployment Verification**
* **Goal:** Write comprehensive `README.md` and verify deployment runbook for Streamlit Community Cloud.
* **Target Files:** `README.md`
* **Linked US / Features:** Final Deployment Milestone
* **Exact Prompt for AI:** *"Create a comprehensive README.md with project badges, overview, architectural data pipeline diagram, local setup instructions, test suite commands, live Streamlit Cloud URL, and ABES MCA capstone credentials."*
* **How to Check:** Verify `README.md` renders properly with working Markdown links and git status is clean.
* **Tests That Must Pass:** Final manual inspection of repo cleanliness.

---

## 4. Definition of Done (DoD)

The project reaches completion only when all the following criteria are met:
1. **100% Must-Have Business Requirements:** All 7 "Must Have" BRs (`BR-01`, `BR-02`, `BR-03`, `BR-06`, `BR-07`, `BR-09`, `BR-11`) are fully functional and verifiable in the UI.
2. **100% Automated Test Passing Rate:** Minimum 14 automated pytest unit, statistical, and Streamlit AppTest cases execute and pass with zero errors.
3. **Sub-2-Second Performance SLA:** All database queries and dashboard filter transitions execute in under 2.0 seconds.
4. **Complete RTM Lineage:** Every single row in `docs/04_Traceability_Matrix.xlsx` contains valid mappings across all 12 columns with status `"Approved & Verified"`.
5. **Zero PII / PHI Exposure:** Strict de-identification compliance with zero authentic personal health records in repository.
6. **Live Cloud Deployment:** Application is publicly accessible 24/7 on Streamlit Community Cloud.
7. **Comprehensive Documentation:** Full ABES Project Document (`.docx`) and presentation deck (`.pptx`) finalized.

---

## 5. Development & Execution Commands

```bash
# 1. Install all pinned dependencies
pip install -r requirements.txt

# 2. Run synthetic dataset generator (deterministic seed = 42)
python src/generate_data.py

# 3. Launch local Streamlit application
streamlit run app.py

# 4. Execute automated pytest test suite
python -m pytest tests/ -v

# 5. Measure query execution latency
python -c "import time, sqlite3, pandas as pd; t0=time.time(); conn=sqlite3.connect('data/app.db'); pd.read_sql_query('SELECT * FROM v_patient_visit_analytics;', conn); print('Latency:', round(time.time()-t0, 4), 's')"
```

---

## 6. Viva Examination Quick-Reference (Top 10 Likely Questions)

1. **Q: Why did you choose an embedded SQLite database rather than PostgreSQL or MySQL?**  
   *A:* SQLite is serverless, zero-configuration, self-contained, and file-based. For an analytical application with 5,000–50,000 records on Streamlit Cloud, it provides sub-millisecond query performance without persistent database server hosting costs or complex connection pool management.
2. **Q: Why was `@st.cache_data` necessary if SQLite is already fast?**  
   *A:* Streamlit re-executes the entire script on every user interaction (e.g., toggling a slider). `@st.cache_data(ttl=3600)` caches resulting DataFrames in memory, reducing retrieval latency from ~45ms down to under 2ms and eliminating repeated disk I/O.
3. **Q: How does the schema handle walk-in patients vs. pre-scheduled appointments?**  
   *A:* Walk-in visits are recorded directly in `visits` with `appointment_id = NULL` and `appointment_type = 'Walk-in'`, while pre-scheduled visits link to `appointments(appointment_id)`. This keeps `appointments` as a pure scheduling fact table for calculating no-show rates.
4. **Q: How is the 30-minute wait time SLA benchmark calculated and monitored?**  
   *A:* $\text{wait\_time} = \text{consultation\_start} - \text{check\_in}$. Any encounter $>30$ minutes is flagged via binary indicator `is_sla_breach = 1`. Departments with average wait $>30$m trigger automated crimson warning cards.
5. **Q: Why did you use One-Way ANOVA for wait times but Kruskal-Wallis for consultation durations?**  
   *A:* Wait times approximate a normal distribution across departments, making ANOVA suitable. Consultation durations are heavily right-skewed (quick follow-ups vs. long oncology visits) with significant outliers; Kruskal-Wallis is a non-parametric rank test that does not assume normality.
6. **Q: How did you prove that long queues degrade patient satisfaction?**  
   *A:* By computing the Pearson correlation coefficient ($r \approx -0.68, p < 0.01$) and OLS regression between `wait_time_minutes` and `csat_score` (1–5 scale), demonstrating a statistically significant inverse relationship.
7. **Q: How does the 30-day readmission logic work in your data pipeline?**  
   *A:* An encounter is flagged as a 30-day readmission if a self-join on `patient_id` detects an acute, unplanned visit within $1\text{--}30$ days of a prior encounter. Planned routine follow-ups are strictly excluded.
8. **Q: Why did you embed Tailwind CSS via `st.components.v1.html` instead of raw CSS?**  
   *A:* Injecting raw CSS via `unsafe_allow_html=True` can conflict with Streamlit's internal Emotion/React styles and break on version upgrades. Rendering Tailwind in an iframe guarantees 100% style encapsulation and zero CSS bleed.
9. **Q: What is the purpose of testing on a "tiny known dataset" in `test_analysis.py`?**  
   *A:* Testing on 5 hardcoded records with pre-calculated manual results unambiguously isolates and validates mathematical formulas (mean wait, breach %, no-show %) without depending on full database state.
10. **Q: What is the purpose of the Requirements Traceability Matrix (RTM)?**  
    *A:* The RTM provides bidirectional lineage connecting Operational Questions $\to$ HMW statements $\to$ Business Requirements $\to$ Features $\to$ Database Columns $\to$ User Stories $\to$ UI Screens $\to$ Test Cases, preventing both scope creep and gold plating.
