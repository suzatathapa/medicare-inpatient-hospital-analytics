# Project Log

## Project: Medicare Inpatient Hospital Analytics

This document tracks the major steps, decisions, tools, and lessons from the project.

---

## Step 1 — Repository Setup

Created a GitHub repository for the Medicare Inpatient Hospital Analytics project.

Initial project folders:

- data
- documentation
- python
- sql
- tableau

### What I learned

I learned how to organize an analytics project into separate folders for raw data, cleaned data, code, documentation, SQL, and visualization assets.

---

## Step 2 — Data Source Selection

Selected CMS Program Statistics Medicare Inpatient Hospital data as the primary data source.

The project uses publicly available Medicare inpatient hospital data covering multiple years.

### What I learned

I learned that real-world government datasets often contain multiple tables, different reporting periods, and methodology documentation that must be reviewed before analysis.

---

## Step 3 — Project Structure

Organized the repository so that:

- `data/raw` contains the original CMS files
- `data/cleaned` will contain processed datasets
- `python` contains data preparation scripts
- `sql` will contain analysis queries
- `documentation` contains scope and methodology notes
- `tableau` will contain dashboard documentation

### What I learned

I learned that a clear project structure makes the analysis easier to reproduce and maintain.

---

## Step 4 — Analysis Scope

Reviewed the CMS inpatient hospital tables and selected the main tables for analysis.

Primary tables:

- Table 1 — utilization, program payments, and cost sharing
- Table 2 — demographic characteristics
- Table 3 — area of residence
- Table 4 — hospital type
- Table 9 — hospital characteristics

Created:

`documentation/analysis_scope.md`

### What I learned

I learned that not every available table should automatically be included in an analysis. Selecting the most relevant tables helps keep the project focused and avoids mixing populations that are not directly comparable.

---

## Step 5 — Python Data Preparation

Created:

`python/prepare_cms_data.py`

The first version of the script was used to inspect the raw CMS files.

The script:

- reads files from `data/raw`
- identifies Excel workbooks
- identifies ZIP archives
- lists workbook sheet names
- lists files contained inside ZIP archives

### Terminal Commands Used

```bash
python3 -m pip install pandas openpyxl
```

```bash
python3 python/prepare_cms_data.py
```

### Result

The script ran successfully and confirmed that Python could access the CMS source files.

The inspection also showed that the CMS files are not packaged the same way across all years. Some years contain multiple Excel files inside ZIP archives, while later years contain multiple tables as worksheets within a workbook.

### What I Learned

I learned how to:

- Run a Python script from Terminal
- Install Python packages with pip
- Use `pandas` to inspect Excel workbooks
- Use Python's `zipfile` module to inspect ZIP archives
- Work with inconsistent real-world file structures
- Verify source data before performing transformations
## Next Step — Extract and Standardize CMS Table 1

The next phase of the project will begin the actual data preparation process.

I will start with CMS Table 1 rather than processing all selected tables at once.

### Tasks

1. Read Table 1 from each relevant CMS source file.
2. Examine the column names and structure across reporting years.
3. Identify differences in how CMS formatted Table 1 between years.
4. Standardize column names and data types where appropriate.
5. Identify overlapping calendar years contained in annual CMS releases to prevent duplicate observations.
6. Preserve CMS suppression indicators such as `*` and `+` during cleaning.
7. Validate the extracted data before creating a cleaned dataset.
8. Export the finalized Table 1 data to `data/cleaned` for later SQL analysis.

### Why Start With Table 1?

Table 1 contains important measures related to Medicare inpatient hospital utilization, program payments, and cost-sharing. It also contains historical calendar years within individual CMS releases.

Because the annual files contain overlapping reporting periods, simply combining every annual Table 1 would create duplicate year observations. Starting with one table allows me to understand and solve these structural issues before applying the process to Tables 2, 3, 4, and 9.

### Expected Output

The goal is to produce a clean, documented Table 1 dataset that can be used for SQL analysis and Tableau visualization.

After the Table 1 workflow is validated, the same data preparation approach will be extended to the other selected CMS tables.

