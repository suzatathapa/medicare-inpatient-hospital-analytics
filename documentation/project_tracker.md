# Medicare Inpatient Hospital Analytics — Project Tracker

This tracker documents the progress of the Medicare Inpatient Hospital Analytics portfolio project.

Last major milestone completed: Table 1 — 2017–2023 Trend Dataset

---

## ✅ Completed

### Project Setup

- [x] Created GitHub repository
- [x] Cloned repository locally
- [x] Established project folder structure
- [x] Created README files for project folders
- [x] Created root project README
- [x] Connected local project to GitHub
- [x] Established Git version-control workflow

### Project Documentation & Development Tracking

- [x] Created detailed project development log
- [x] Documented completed Table 1 data-preparation milestones
- [x] Documented meaningful errors and their resolutions
- [x] Created project status tracker
- [x] Created Terminal, Python, and Git command reference
- [x] Documented Git repository setup and workflow
- [x] Documented development troubleshooting lessons
- [x] Established milestone workflow: inspect → understand → clean → validate → sanity check → document → commit → push
- [x] Created clean GitHub checkpoint before beginning Table 2

### Data Collection

- [x] Selected CMS Program Statistics — Medicare Inpatient Hospital as the primary data source
- [x] Collected CMS Medicare Inpatient Hospital datasets for 2017–2023
- [x] Collected CMS methodology documentation
- [x] Collected CMS glossary documentation
- [x] Preserved original source files in `data/raw`

### Analysis Planning

- [x] Reviewed available CMS inpatient hospital tables
- [x] Defined initial project analysis scope
- [x] Selected Tables 1, 2, 3, 4, and 9 as core analytical tables
- [x] Identified Tables 5–8 as optional later analysis
- [x] Identified Table 10 as outside the initial scope
- [x] Documented data-quality considerations
- [x] Identified CMS suppression values as different from zero
- [x] Identified overlapping historical reporting periods in annual CMS releases

### Python Data Preparation

- [x] Created Python data-preparation script
- [x] Added raw-file inspection workflow
- [x] Added ZIP archive inspection
- [x] Added Excel workbook inspection
- [x] Installed and used Pandas
- [x] Installed and used OpenPyXL
- [x] Read CMS Excel workbooks directly from ZIP archives

### Table 1 — 2023

- [x] Located 2023 Table 1
- [x] Inspected raw Table 1 structure
- [x] Identified actual header row
- [x] Removed CMS report-title and formatting rows
- [x] Separated entitlement categories from calendar years
- [x] Forward-filled entitlement categories
- [x] Converted calendar years to integers
- [x] Added automated validation assertions
- [x] Checked expected calendar years
- [x] Checked missing entitlement categories
- [x] Checked duplicate entitlement/year observations
- [x] Validated expected row count
- [x] Exported cleaned 2023 Table 1 dataset

### Table 1 — 2017 Inspection

- [x] Located 2017 Table 1 inside ZIP archive
- [x] Inspected raw dimensions
- [x] Confirmed 28 source columns
- [x] Confirmed reporting period 2012–2017
- [x] Compared 2017 structure with 2023 structure

### Table 1 — 2017 Cleaning

- [x] Cleaned hierarchical CMS report structure
- [x] Extracted entitlement categories
- [x] Extracted calendar years
- [x] Validated 2012–2017 observations
- [x] Selected calendar year 2017 for final trend analysis
- [x] Validated three 2017 entitlement observations

### Table 1 — Schema Standardization

- [x] Compared cleaned 2017 and 2023 schemas
- [x] Confirmed both datasets contained 29 cleaned columns
- [x] Identified four CMS footnote-formatting differences
- [x] Standardized 2017 column names to the 2023 schema
- [x] Detected inconsistent trailing whitespace in entitlement categories
- [x] Used `.str.strip()` to standardize category values
- [x] Retained diagnostic code as comments for development reference

### Table 1 — Final 2017–2023 Dataset

- [x] Selected 2017 from the 2017 CMS release
- [x] Selected 2018–2023 from the 2023 CMS release
- [x] Avoided duplicate observations from overlapping annual releases
- [x] Combined standardized datasets
- [x] Validated calendar years 2017–2023
- [x] Validated three entitlement categories
- [x] Validated no duplicate entitlement/year combinations
- [x] Validated expected 21 observations
- [x] Performed final sanity check on key measures
- [x] Exported `cms_table1_2017_2023_cleaned.csv`
- [x] Documented Table 1 workflow in project log
- [x] Committed and pushed completed Table 1 milestone to GitHub

---

## 🔄 Current / Next Milestone

### Table 2 — Demographic Characteristics

- [ ] Inspect 2023 Table 2 raw structure
- [ ] Identify header and category hierarchy
- [ ] Review demographic dimensions and measures
- [ ] Identify suppression and missing-value patterns
- [ ] Design Table 2 cleaning logic
- [ ] Clean Table 2 with Python
- [ ] Add data-quality validation
- [ ] Perform sanity checks
- [ ] Export analysis-ready Table 2 dataset
- [ ] Document methodology and issues
- [ ] Commit and push milestone

---

## 📋 Upcoming

### Table 3 — Area of Residence

- [ ] Inspect raw structure
- [ ] Clean geographic fields
- [ ] Handle suppressed values
- [ ] Validate geographic observations
- [ ] Export analysis-ready dataset
- [ ] Document and commit

### Table 4 — Hospital Type

- [ ] Inspect raw structure
- [ ] Clean hospital-type categories
- [ ] Validate measures
- [ ] Export analysis-ready dataset
- [ ] Document and commit

### Table 9 — Hospital Characteristics

- [ ] Inspect raw structure
- [ ] Review location and bed-size dimensions
- [ ] Review medical-school affiliation
- [ ] Review type-of-control categories
- [ ] Clean and validate dataset
- [ ] Export analysis-ready dataset
- [ ] Document and commit

### SQL Analysis

- [ ] Design analysis database
- [ ] Create SQL tables
- [ ] Load cleaned CMS datasets
- [ ] Write SQL data-quality queries
- [ ] Develop KPI queries
- [ ] Analyze utilization trends
- [ ] Analyze program-payment trends
- [ ] Analyze demographic differences
- [ ] Analyze geographic variation
- [ ] Analyze hospital-type differences
- [ ] Analyze hospital characteristics
- [ ] Develop year-over-year calculations

### Exploratory Analysis

- [ ] Perform exploratory analysis in Python
- [ ] Review distributions and trends
- [ ] Investigate unusual observations
- [ ] Develop analytical findings
- [ ] Validate important calculations

### Tableau Public Dashboard

- [ ] Define dashboard KPIs
- [ ] Prepare Tableau datasets
- [ ] Build utilization trend visual
- [ ] Build program-payment trend visual
- [ ] Build demographic comparison visual
- [ ] Build geographic analysis
- [ ] Build hospital-type analysis
- [ ] Build hospital-characteristics analysis
- [ ] Add interactive filters
- [ ] Create dashboard layout
- [ ] Perform dashboard QA
- [ ] Publish to Tableau Public
- [ ] Add Tableau link to GitHub README

### Final Portfolio Documentation

- [ ] Finalize data dictionary
- [ ] Document analytical methodology
- [ ] Document assumptions and limitations
- [ ] Document CMS suppression handling
- [ ] Summarize key findings
- [ ] Update root README with final workflow
- [ ] Add dashboard preview
- [ ] Add portfolio skills demonstrated
- [ ] Review repository organization
- [ ] Perform final code cleanup
- [ ] Perform final project QA
- [ ] Prepare project explanation for interviews

---

## Project Workflow

For each major dataset or analytical milestone:

**Inspect → Understand → Clean → Validate → Sanity Check → Document → Commit → Push**

Documentation should describe work that was actually completed rather than planned work.