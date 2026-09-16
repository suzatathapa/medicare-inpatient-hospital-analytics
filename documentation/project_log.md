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

## Step 5D.1 — Inspect Table 1 Structure

I used Python to inspect the raw structure of the 2023 CMS Medicare Inpatient Hospital Table 1 before performing any transformations.

### Findings

The raw 2023 Table 1 contains 36 rows and 28 columns.

The worksheet is not immediately analysis-ready. The first rows contain report titles and reporting-period information before the actual column headers.

The table contains 28 measures related to Medicare inpatient hospital utilization, enrollment, program payments, cost sharing, and other utilization measures.

The observations are organized hierarchically by entitlement category and calendar year. For example, an entitlement category such as `All Beneficiaries` is followed by separate observations for calendar years 2018 through 2023.

### Data Preparation Implications

The cleaning process will need to:

- Remove report-title and formatting rows
- Identify and assign the correct column headers
- Separate entitlement category from calendar year
- Propagate entitlement categories to their corresponding annual observations
- Remove blank and non-data rows
- Standardize column names
- Convert appropriate measures to numeric data types
- Preserve CMS suppression indicators during processing
- Validate the cleaned output against the original CMS table

### What I Learned

I learned why inspecting raw data before cleaning is important. Although the Excel worksheet visually represents a report, its structure is different from an analysis-ready dataset.

I also learned that hierarchical report layouts may require transformation before the data can be analyzed with SQL, Python, or Tableau.


## Step 5D — Clean and Validate CMS Table 1

I inspected, cleaned, validated, and exported the 2023 CMS Medicare Inpatient Hospital Table 1 using Python.

### What I Did

- Opened the 2023 CMS ZIP archive with Python
- Located the Excel workbook inside the archive
- Identified the Table 1 worksheet
- Read the worksheet without headers to inspect its raw structure
- Identified the true header row
- Removed title and formatting rows
- Separated entitlement category from calendar year
- Forward-filled entitlement categories to their corresponding annual observations
- Removed non-data rows
- Converted calendar year values to integers
- Reordered identifying fields so `Entitlement_Type` and `Calendar_Year` appear first
- Added automated data quality checks
- Exported the cleaned dataset to:

`data/cleaned/cms_table1_2023_cleaned.csv`

### Validation Results

The cleaned dataset contains:

- 18 observations
- 29 columns
- 3 entitlement categories:
  - All Beneficiaries
  - Aged Beneficiaries
  - Disabled Beneficiaries
- Calendar years 2018 through 2023

The validation checks confirmed:

- Expected calendar years were present
- No entitlement categories were missing
- No duplicate entitlement/year combinations existed
- The expected 18 observations were produced

### Problems Encountered and Resolutions

**FileNotFoundError**

The first version of the script expected the 2023 CMS source to be a direct Excel file.

**Resolution:**  
Updated the script to locate the 2023 ZIP archive, open it with Python, and access the Excel workbook inside the archive.

---

**IndentationError**

While updating the Python function, inconsistent indentation caused the script to fail.

**Resolution:**  
Replaced the affected function using consistent four-space indentation.

### What I Learned

I learned that real-world government data is often distributed in reporting formats rather than analysis-ready tables.

I also learned how to:

- Inspect Excel files programmatically before transformation
- Read Excel workbooks directly from ZIP archives
- Identify and remove report formatting rows
- Transform hierarchical report layouts into structured tabular data
- Use forward filling to assign category labels to related observations
- Add automated validation checks with Python assertions
- Export cleaned data for later SQL and Tableau analysis



## Step 5D — Clean and Validate CMS Table 1

I inspected, cleaned, validated, and exported the 2023 CMS Medicare Inpatient Hospital Table 1 using Python.

### What I Did

- Opened the 2023 CMS ZIP archive with Python
- Located the Excel workbook inside the archive
- Identified the Table 1 worksheet
- Read the worksheet without headers to inspect its raw structure
- Identified the actual header row
- Removed report title, blank, and formatting rows
- Separated entitlement category from calendar year
- Forward-filled entitlement categories to their corresponding annual observations
- Converted calendar year values to integers
- Added automated data quality checks
- Exported the cleaned dataset to `data/cleaned/cms_table1_2023_cleaned.csv`

### Validation Results

The cleaned dataset contains:

- 18 observations
- 29 columns
- 3 entitlement categories: All Beneficiaries, Aged Beneficiaries, and Disabled 
Beneficiaries
- Calendar years 2018 through 2023

The validation checks confirmed:

- Expected calendar years were present
- No entitlement categories were missing
- No duplicate entitlement/year combinations existed
- The expected 18 observations were produced

### Problems Encountered and Resolutions

**FileNotFoundError**

The initial script expected the 2023 CMS source to be a direct Excel workbook, but 
the local source file was distributed as a ZIP archive.

**Resolution:** Updated the Python workflow to locate the 2023 ZIP archive, open the 
archive, locate the Excel workbook inside it, and read Table 1 from the workbook.

**IndentationError**

While modifying the Python function, inconsistent indentation caused the script to
 fail.

**Resolution:** Replaced the affected code using consistent four-space Python 
indentation.

### What I Learned

I learned that real-world government datasets may be distributed and formatted 
differently from analysis-ready datasets. Inspecting the source structure before 
transformation helped me avoid making incorrect assumptions about the data.

I also gained hands-on experience reading Excel files from ZIP archives, transforming
 hierarchical report layouts, forward-filling category values, validating transformed 
 data with Python assertions, and exporting analysis-ready data.


## Step 5E — Build the 2017–2023 Table 1 Trend Dataset

I inspected the 2017 CMS Medicare Inpatient Hospital Table 1 and compared its structure with the cleaned 2023 Table 1 before combining the datasets.

### What I Did

- Opened the 2017 CMS ZIP archive with Python
- Located the Table 1 Excel workbook inside the archive
- Inspected the raw 2017 Table 1 structure
- Confirmed that the 2017 and 2023 Table 1 files both contained 28 source columns
- Confirmed that the 2017 release contains calendar years 2012–2017
- Compared the cleaned 2017 and 2023 column names
- Identified four column-name differences caused by CMS footnote formatting
- Standardized the 2017 column names to match the 2023 schema
- Cleaned entitlement category labels by removing leading and trailing whitespace
- Selected calendar year 2017 from the 2017 release
- Used calendar years 2018–2023 from the 2023 release
- Combined the datasets into a single 2017–2023 trend dataset
- Added validation checks for years, categories, duplicates, and expected row count
- Performed a final sanity check on enrollment, utilization, discharge, and program payment measures
- Exported the final dataset to `data/cleaned/cms_table1_2017_2023_cleaned.csv`

### Overlapping Reporting Years

CMS Table 1 annual releases contain overlapping historical reporting periods.

The 2017 release contains calendar years 2012–2017, while the 2023 release contains calendar years 2018–2023.

Rather than stacking annual releases and creating duplicate observations, I used:

- Calendar year 2017 from the 2017 release
- Calendar years 2018–2023 from the 2023 release

This produced one observation per entitlement category and calendar year for the 2017–2023 analysis period.

### Schema Differences Identified

The cleaned 2017 and 2023 datasets both contained 29 columns, but four column names differed because CMS used different footnote formatting between releases.

Examples included:

- `Persons With Coinsurance 1` vs. `Persons With Coinsurance¹`
- `Coinsurance Days Per Person With Coinsurance 1` vs. `Coinsurance Days Per Person With Coinsurance¹`
- `Coinsurance Payments Per Person With Coinsurance 1` vs. `Coinsurance Payments Per Person With Coinsurance¹`
- `Persons with Lifetime Reserve Days 2` vs. `Persons with Lifetime Reserve Days²`

I standardized the 2017 column names before combining the datasets.

### Problem Encountered — Inconsistent Category Whitespace

During validation, the combined dataset failed the expected entitlement-category check.

Python identified five unique category values instead of the expected three because some category labels contained trailing spaces:

- `Aged Beneficiaries`
- `Aged Beneficiaries `
- `Disabled Beneficiaries`
- `Disabled Beneficiaries `

### Resolution

I used Python string cleaning with `.str.strip()` to remove leading and trailing whitespace from the entitlement category values before combining the datasets.

I reran the validation checks after the correction, and the dataset passed successfully.

The diagnostic code used to identify the whitespace issue was retained as comments in
 the Python script for development reference.  

### Final Validation Results

The final combined dataset contains:

- 21 observations
- 29 columns
- 3 entitlement categories
- Calendar years 2017 through 2023
- 7 observations per entitlement category

The validation checks confirmed:

- Expected calendar years were present
- Exactly three entitlement categories were present
- No entitlement categories were missing
- No duplicate entitlement/year combinations existed
- The expected 21 observations were produced
- The 2017 and 2023 schemas matched after standardization

A final sanity check was also performed on selected measures including Original 
Medicare Part A enrollment, persons with utilization, discharges, and total program 
payments.

### What I Learned

I learned why historical government data releases should be inspected before they are
 combined. Annual CMS releases can contain overlapping reporting periods, so simply 
 appending files can introduce duplicate observations.

I also learned how small schema differences, such as footnote formatting and trailing 
whitespace, can cause otherwise equivalent values to be treated differently during 
analysis.

Using schema comparisons, diagnostic output, string standardization, and automated 
assertions helped identify and resolve these issues before producing the final 
analysis-ready dataset.






