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


if __name__ == "__main__":
    inspect_raw_data()
    preview_table_1()
    clean_table_1_2023()

