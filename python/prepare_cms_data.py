import pandas as pd
import zipfile
from pathlib import Path

# --------------------------------------------------
# CMS Medicare Inpatient Hospital Data Preparation
# --------------------------------------------------

RAW_DATA_DIR = Path("data/raw")
CLEAN_DATA_DIR = Path("data/cleaned")

CLEAN_DATA_DIR.mkdir(parents=True, exist_ok=True)


def inspect_excel_file(file_path):
    """
    Display the worksheet names contained in an Excel workbook.
    """
    print(f"\nInspecting: {file_path.name}")

    excel_file = pd.ExcelFile(file_path)

    print("Worksheets:")
    for sheet in excel_file.sheet_names:
        print(f"  - {sheet}")


def inspect_zip_file(file_path):
    """
    Display the files contained inside a ZIP archive.
    """
    print(f"\nInspecting ZIP: {file_path.name}")

    with zipfile.ZipFile(file_path, "r") as zip_file:
        for name in zip_file.namelist():
            print(f"  - {name}")


def inspect_raw_data():
    """
    Inspect all CMS source files before data transformation.
    """

    print("CMS Medicare Inpatient Hospital Data Inspection")
    print("=" * 50)

    for file_path in sorted(RAW_DATA_DIR.iterdir()):

        if file_path.name.startswith("."):
            continue

        if file_path.suffix.lower() == ".xlsx":
            inspect_excel_file(file_path)

        elif file_path.suffix.lower() == ".zip":
            inspect_zip_file(file_path)

def preview_table_1():
   

    """
    Preview Table 1 from the 2023 CMS ZIP file.
    """

    zip_matches = list(RAW_DATA_DIR.glob("*2023*.zip"))

    if not zip_matches:
        raise FileNotFoundError("No 2023 ZIP file found in data/raw")

    zip_path = zip_matches[0]

    print(f"\nUsing 2023 ZIP: {zip_path.name}")

    with zipfile.ZipFile(zip_path, "r") as zip_file:
        excel_files = [
            name
            for name in zip_file.namelist()
            if name.lower().endswith(".xlsx")
            and not name.startswith("__MACOSX")
        ]

        if not excel_files:
            raise FileNotFoundError(
                "No Excel workbook found inside the 2023 ZIP file"
            )

        excel_name = excel_files[0]

        print(f"Excel file inside ZIP: {excel_name}")

        with zip_file.open(excel_name) as excel_data:
            excel_file = pd.ExcelFile(excel_data)

            table_1_sheets = [
                sheet
                for sheet in excel_file.sheet_names
                if "HOSP 1" in sheet
            ]

            if not table_1_sheets:
                raise ValueError("Table 1 worksheet was not found")

            table_1_sheet = table_1_sheets[0]

            print(f"Table 1 sheet: {table_1_sheet}")

            df = pd.read_excel(
                excel_file,
                sheet_name=table_1_sheet,
                header=None
            )

    print("\n" + "=" * 70)
    print("2023 TABLE 1 PREVIEW")
    print("=" * 70)

    print(f"Raw dimensions: {df.shape}")

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)

    print("\nFirst 15 rows:")
    print(df.head(15).to_string(index=False))

def clean_table_1_2023():
    """
    Clean the 2023 CMS Medicare Inpatient Hospital Table 1
    into an analysis-ready DataFrame.
    """

    zip_matches = list(RAW_DATA_DIR.glob("*2023*.zip"))

    if not zip_matches:
        raise FileNotFoundError("No 2023 ZIP file found in data/raw")

    zip_path = zip_matches[0]

    with zipfile.ZipFile(zip_path, "r") as zip_file:
        excel_files = [
            name
            for name in zip_file.namelist()
            if name.lower().endswith(".xlsx")
            and not name.startswith("__MACOSX")
        ]

        if not excel_files:
            raise FileNotFoundError(
                "No Excel workbook found inside the 2023 ZIP file"
            )

        with zip_file.open(excel_files[0]) as excel_data:
            excel_file = pd.ExcelFile(excel_data)

            table_1_sheets = [
                sheet
                for sheet in excel_file.sheet_names
                if "HOSP 1" in sheet
            ]

            if not table_1_sheets:
                raise ValueError("Table 1 worksheet was not found")

            df = pd.read_excel(
                excel_file,
                sheet_name=table_1_sheets[0],
                header=None
            )

    # The raw inspection showed that row 3 contains
    # the actual column names.
    headers = df.iloc[3].tolist()

    # Keep everything below the header row.
    data = df.iloc[4:].copy()
    data.columns = headers

    first_column = data.columns[0]

    # Remove completely empty rows.
    data = data.dropna(how="all")

    # Identify rows containing calendar years.
    year_values = pd.to_numeric(
        data[first_column],
        errors="coerce"
    )

    # Rows without a numeric year are potential
    # entitlement category labels.
    data["Entitlement_Type"] = data[first_column].where(
        year_values.isna()
    )

    # Do not treat CMS formatting labels as entitlement categories.
    data.loc[
        data["Entitlement_Type"].astype(str).str.upper().eq("BLANK"),
        "Entitlement_Type"
    ] = pd.NA

    # Carry the entitlement category down to its annual observations.
    data["Entitlement_Type"] = data["Entitlement_Type"].ffill()

    # Create the calendar year column.
    data["Calendar_Year"] = year_values

    # Keep only actual annual observations.
    data = data[data["Calendar_Year"].notna()].copy()

    data["Calendar_Year"] = data["Calendar_Year"].astype(int)

    # The original first column is no longer needed.
    data = data.drop(columns=[first_column])

    # Put our two identifying fields first.
    remaining_columns = [
        column
        for column in data.columns
        if column not in ["Entitlement_Type", "Calendar_Year"]
    ]

    data = data[
        ["Entitlement_Type", "Calendar_Year"] + remaining_columns
    ]

    print("\n" + "=" * 70)
    print("CLEANED 2023 TABLE 1")
    print("=" * 70)

    print(f"Rows: {len(data)}")
    print(f"Columns: {len(data.columns)}")

    print("\nEntitlement categories:")
    print(data["Entitlement_Type"].unique())

    print("\nCalendar years:")
    print(sorted(data["Calendar_Year"].unique()))

    print("\nFirst 10 cleaned rows:")
    print(data.head(10).to_string(index=False))

    # --------------------------------------------------
    # Data quality validation
    # --------------------------------------------------

    expected_years = [2018, 2019, 2020, 2021, 2022, 2023]

    assert sorted(data["Calendar_Year"].unique()) == expected_years, \
        "Unexpected calendar years found"

    assert data["Entitlement_Type"].notna().all(), \
        "Missing entitlement categories found"

    assert not data.duplicated(
        subset=["Entitlement_Type", "Calendar_Year"]
    ).any(), "Duplicate entitlement/year observations found"

    assert len(data) == 18, \
        f"Expected 18 observations, found {len(data)}"

    print("\nData quality checks: PASSED")
    print("✓ Expected calendar years found")
    print("✓ No missing entitlement categories")
    print("✓ No duplicate entitlement/year observations")
    print("✓ Expected 18 observations found")

    output_path = CLEAN_DATA_DIR / "cms_table1_2023_cleaned.csv"

    data.to_csv(output_path, index=False)

    print(f"\nCleaned file saved to: {output_path}")

    return data


def preview_table_1_2017():
    """
    Preview CMS Medicare Inpatient Hospital Table 1
    from the 2017 ZIP archive.
    """

    zip_matches = list(RAW_DATA_DIR.glob("*2017*.zip"))

    if not zip_matches:
        raise FileNotFoundError(
            "No 2017 ZIP file found in data/raw"
        )

    zip_path = zip_matches[0]

    print(f"\nUsing 2017 ZIP: {zip_path.name}")

    with zipfile.ZipFile(zip_path, "r") as zip_file:

        excel_files = [
            name
            for name in zip_file.namelist()
            if name.lower().endswith(".xlsx")
            and not name.startswith("__MACOSX")
        ]

        print("\nExcel files inside 2017 ZIP:")
        for name in excel_files:
            print(f"  - {name}")

        table_1_files = [
            name
            for name in excel_files
            if "HOSP 1." in name.upper()
        ]

        if not table_1_files:
            raise ValueError(
                "Could not automatically identify the 2017 Table 1 file"
            )

        table_1_file = table_1_files[0]

        print(f"\nSelected Table 1 file: {table_1_file}")

        with zip_file.open(table_1_file) as excel_data:
            df = pd.read_excel(
                excel_data,
                header=None
            )

    print("\n" + "=" * 70)
    print("2017 TABLE 1 PREVIEW")
    print("=" * 70)

    print(f"Raw dimensions: {df.shape}")

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)

    print("\nFirst 15 rows:")
    print(df.head(15).to_string(index=False))


def clean_table_1_2017():
    """
    Clean CMS Medicare Inpatient Hospital Table 1 from the 2017 release
    and keep only calendar year 2017 for the final trend dataset.
    """

    # Find the 2017 ZIP file
    zip_matches = list(RAW_DATA_DIR.glob("*2017*.zip"))

    if not zip_matches:
        raise FileNotFoundError(
            "No 2017 ZIP file found in data/raw"
        )

    zip_path = zip_matches[0]

    print(f"\nCleaning 2017 Table 1 from: {zip_path.name}")

    # Open the ZIP archive
    with zipfile.ZipFile(zip_path, "r") as zip_file:

        # Find Excel files inside the archive
        excel_files = [
            name
            for name in zip_file.namelist()
            if name.lower().endswith(".xlsx")
            and "__MACOSX" not in name
        ]

        # Identify Table 1
        table_1_files = [
            name
            for name in excel_files
            if "HOSP 1." in name.upper()
        ]

        if not table_1_files:
            raise ValueError(
                "Could not automatically identify the 2017 Table 1 file"
            )

        table_1_file = table_1_files[0]

        print(f"Selected Table 1 file: {table_1_file}")

        # Read Table 1 directly from the ZIP archive
        with zip_file.open(table_1_file) as excel_data:
            df = pd.read_excel(
                excel_data,
                header=None
            )

    # The actual CMS column headers are on row 4
    headers = df.iloc[3].copy()

    # Everything after the header row is report data
    data = df.iloc[4:].copy()
    data.columns = headers

    # Remove completely blank rows
    data = data.dropna(how="all")

    # First column contains both entitlement categories and years
    first_column = data.columns[0]

    # Try converting first column to numeric.
    # Category names become NaN; calendar years remain numeric.
    numeric_year = pd.to_numeric(
        data[first_column],
        errors="coerce"
    )

    # Extract entitlement category labels
    data["Entitlement_Type"] = data[first_column].where(
        numeric_year.isna()
    )

    # BLANK is a CMS formatting row, not an entitlement category
    data["Entitlement_Type"] = data["Entitlement_Type"].replace(
        "BLANK",
        pd.NA
    )

    # Carry each entitlement category down to its annual rows
    data["Entitlement_Type"] = data["Entitlement_Type"].ffill()

    # Create calendar year column
    data["Calendar_Year"] = numeric_year

    # Keep only actual annual observations
    data = data[
        data["Calendar_Year"].notna()
    ].copy()

    data["Calendar_Year"] = data["Calendar_Year"].astype(int)

    # Remove the original mixed category/year column
    data = data.drop(columns=[first_column])

    # Put our standardized identifier columns first
    remaining_columns = [
        column
        for column in data.columns
        if column not in ["Entitlement_Type", "Calendar_Year"]
    ]

    data = data[
        ["Entitlement_Type", "Calendar_Year"] + remaining_columns
    ]

    # Validate the full cleaned 2017 release
    expected_years = [2012, 2013, 2014, 2015, 2016, 2017]

    assert sorted(data["Calendar_Year"].unique()) == expected_years, \
        "Unexpected calendar years found in 2017 Table 1"

    assert data["Entitlement_Type"].notna().all(), \
        "Missing entitlement categories found"

    assert not data.duplicated(
        subset=["Entitlement_Type", "Calendar_Year"]
    ).any(), "Duplicate entitlement/year observations found"

    assert len(data) == 18, \
        f"Expected 18 observations, found {len(data)}"

    print("\n2017 Table 1 data quality checks: PASSED")
    print("✓ Expected calendar years 2012-2017 found")
    print("✓ No missing entitlement categories")
    print("✓ No duplicate entitlement/year observations")
    print("✓ Expected 18 observations found")

    # For this project, we only need 2017 from this release.
    # The 2023 release will provide 2018-2023.
    data_2017 = data[
        data["Calendar_Year"] == 2017
    ].copy()

    # Validate the extracted 2017 observations
    assert len(data_2017) == 3, \
        f"Expected 3 observations for 2017, found {len(data_2017)}"

    assert data_2017["Entitlement_Type"].nunique() == 3, \
        "Expected 3 entitlement categories for 2017"

    print("\n2017 extraction checks: PASSED")
    print("✓ Calendar year 2017 selected")
    print("✓ Expected 3 entitlement observations found")

    print("\n2017 cleaned data:")
    print(
        data_2017[
            ["Entitlement_Type", "Calendar_Year"]
        ].to_string(index=False)
    )

    return data_2017

def compare_table_1_columns(data_2017, data_2023):
    """
    Compare column names between the cleaned
    2017 and 2023 Table 1 datasets.
    """

    print("\n" + "=" * 70)
    print("2017 VS 2023 COLUMN COMPARISON")
    print("=" * 70)

    columns_2017 = list(data_2017.columns)
    columns_2023 = list(data_2023.columns)

    print(f"\n2017 column count: {len(columns_2017)}")
    print(f"2023 column count: {len(columns_2023)}")

    print("\nColumns with differences:")

    differences_found = False

    for position, (col_2017, col_2023) in enumerate(
        zip(columns_2017, columns_2023),
        start=1
    ):
        if col_2017 != col_2023:
            differences_found = True

            print(f"\nColumn {position}")
            print(f"2017: {col_2017}")
            print(f"2023: {col_2023}")

    if len(columns_2017) != len(columns_2023):
        print("\n⚠ Column counts are different.")

    elif not differences_found:
        print("\n✓ All column names match exactly.")


def combine_table_1_trend(data_2017, data_2023):
    """
    Standardize column names and combine the 2017 observation
    with 2018-2023 observations from the 2023 CMS release.
    """

    print("\n" + "=" * 70)
    print("BUILDING FINAL 2017-2023 TABLE 1 DATASET")
    print("=" * 70)

    # Standardize 2017 footnote-based column names
    column_mapping = {
        "Persons With Coinsurance 1":
            "Persons With Coinsurance¹",

        "Coinsurance Days Per Person With Coinsurance 1":
            "Coinsurance Days Per Person With Coinsurance¹",

        "Coinsurance Payments Per Person With Coinsurance 1":
            "Coinsurance Payments Per Person With Coinsurance¹",

        "Persons with Lifetime Reserve Days 2":
            "Persons with Lifetime Reserve Days²"
    }

    data_2017 = data_2017.rename(
        columns=column_mapping
    )

    # Standardize entitlement category text
    data_2017["Entitlement_Type"] = (
    data_2017["Entitlement_Type"]
    .astype(str)
    .str.strip()
)

    data_2023["Entitlement_Type"] = (
    data_2023["Entitlement_Type"]
    .astype(str)
    .str.strip()
    )

    # Verify that the schemas now match exactly
    assert list(data_2017.columns) == list(data_2023.columns), \
        "2017 and 2023 column names still do not match"

    print("\n✓ 2017 and 2023 column names standardized")
    print("✓ Dataset schemas match")

    # Combine 2017 with 2018-2023
    combined_data = pd.concat(
        [data_2017, data_2023],
        ignore_index=True
    )

    # Sort by entitlement category and calendar year
    combined_data = combined_data.sort_values(
        ["Entitlement_Type", "Calendar_Year"]
    ).reset_index(drop=True)

    # ---------------------------------------------------------
    # DATA QUALITY VALIDATION
    # ---------------------------------------------------------

    expected_years = [
        2017,
        2018,
        2019,
        2020,
        2021,
        2022,
        2023
    ]

    assert sorted(
        combined_data["Calendar_Year"].unique()
    ) == expected_years, \
        "Unexpected calendar years in combined dataset"

    assert combined_data["Entitlement_Type"].notna().all(), \
        "Missing entitlement categories found"

    assert not combined_data.duplicated(
        subset=["Entitlement_Type", "Calendar_Year"]
    ).any(), \
        "Duplicate entitlement/year observations found"
    
    # Diagnostic check used during development:
    # This revealed that some 2017 entitlement categories contained
    # trailing spaces, causing Python to treat them as separate categories.
    #
    #print("\nEntitlement categories found:")
    #print(combined_data["Entitlement_Type"].value_counts(dropna=False))

    #print("\nUnique entitlement category values:")
    #for value in combined_data["Entitlement_Type"].unique():
    #    print(repr(value))

    assert combined_data["Entitlement_Type"].nunique() == 3, \
        "Expected 3 entitlement categories"

    assert len(combined_data) == 21, \
        f"Expected 21 observations, found {len(combined_data)}"

    print("\nCombined dataset validation: PASSED")
    print("✓ Calendar years 2017-2023 found")
    print("✓ 3 entitlement categories found")
    print("✓ No missing entitlement categories")
    print("✓ No duplicate entitlement/year observations")
    print("✓ Expected 21 observations found")

    # ---------------------------------------------------------
    # FINAL SANITY CHECK
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("FINAL TABLE 1 SANITY CHECK")
    print("=" * 70)

    sanity_columns = [
    "Entitlement_Type",
    "Calendar_Year",
    "Total Original Medicare Part A Enrollees",
    "Total Persons With Utilization",
    "Total Discharges",
    "Total Program Payments"
    ]

    print(
    combined_data[sanity_columns]
    .sort_values(["Entitlement_Type", "Calendar_Year"])
    .to_string(index=False)
    )

    # Display final structure
    print("\nFinal dataset:")
    print(
        combined_data[
            ["Entitlement_Type", "Calendar_Year"]
        ].to_string(index=False)
    )

    # Export final analysis-ready dataset
    output_path = (
        CLEAN_DATA_DIR /
        "cms_table1_2017_2023_cleaned.csv"
    )

    combined_data.to_csv(
        output_path,
        index=False
    )

    print(
        f"\nFinal cleaned dataset saved to: {output_path}"
    )

    return combined_data

if __name__ == "__main__":
    inspect_raw_data()
    preview_table_1()
    

    data_2023 = clean_table_1_2023()

    preview_table_1_2017()

    data_2017 = clean_table_1_2017()

    compare_table_1_columns(
        data_2017,
        data_2023
    )
    
    combined_table_1 = combine_table_1_trend(
        data_2017,
        data_2023
    )