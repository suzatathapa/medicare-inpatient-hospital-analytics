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


if __name__ == "__main__":
    inspect_raw_data()
