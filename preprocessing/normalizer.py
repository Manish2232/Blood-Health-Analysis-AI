import re
import pandas as pd


# Standard names for common blood test variants
TEST_NAME_MAP = {
    "hb": "Hemoglobin",
    "hgb": "Hemoglobin",
    "hemoglobin": "Hemoglobin",
    "rbc": "RBC",
    "wbc": "WBC",
    "platelet": "Platelet Count",
    "platelets": "Platelet Count",
    "vit d": "Vitamin D",
    "vitamin d": "Vitamin D",
    "tsh": "TSH",
    "t3": "T3",
    "t4": "T4",
    "glucose": "Glucose",
    "fasting glucose": "Glucose",
    "cholesterol": "Cholesterol",
    "ldl": "LDL Cholesterol",
    "hdl": "HDL Cholesterol",
    "triglycerides": "Triglycerides",
}


def clean_text(value):
    """Normalize raw text by trimming spaces and lowering case."""
    if pd.isna(value):
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_test_name(test_name):
    """Map different naming styles to one standard test name."""
    text = clean_text(test_name)
    return TEST_NAME_MAP.get(text, str(test_name).strip().title())


def normalize_reference_range(reference_range):
    """Make reference range text cleaner and more consistent."""
    if pd.isna(reference_range):
        return ""

    text = str(reference_range).strip()
    text = text.replace("to", "-")
    text = text.replace("–", "-")
    text = re.sub(r"\s*[-]\s*", "-", text)
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize common blood report columns.

    Expected columns (if available):
    - TestName / Test Name
    - Result
    - Unit
    - ReferenceRange / Reference Range
    - Flag
    - Remarks
    """
    df = df.copy()

    # Remove accidental spaces in column names
    df.columns = [str(col).strip() for col in df.columns]

    # Try to support multiple column naming patterns
    column_aliases = {
        "TestName": ["TestName", "Test Name", "test_name", "name"],
        "Result": ["Result", "result", "value"],
        "Unit": ["Unit", "unit"],
        "ReferenceRange": ["ReferenceRange", "Reference Range", "reference_range", "range"],
        "Flag": ["Flag", "flag"],
        "Remarks": ["Remarks", "remarks", "Comment", "comment"],
    }

    rename_map = {}
    for standard_name, aliases in column_aliases.items():
        for alias in aliases:
            if alias in df.columns:
                rename_map[alias] = standard_name
                break

    df = df.rename(columns=rename_map)

    # Normalize if the key columns exist
    if "TestName" in df.columns:
        df["TestName"] = df["TestName"].apply(normalize_test_name)

    if "ReferenceRange" in df.columns:
        df["ReferenceRange"] = df["ReferenceRange"].apply(normalize_reference_range)

    if "Unit" in df.columns:
        df["Unit"] = df["Unit"].apply(lambda x: str(x).strip() if not pd.isna(x) else "")

    if "Flag" in df.columns:
        df["Flag"] = df["Flag"].apply(lambda x: str(x).strip().upper() if not pd.isna(x) else "")

    return df
