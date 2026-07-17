import re
import pandas as pd


def parse_reference_range(reference_range):
    """
    Parse a reference range like '13-17' into (lower, upper).
    Returns (None, None) if parsing fails.
    """
    if pd.isna(reference_range):
        return None, None

    text = str(reference_range).strip()
    text = text.replace("to", "-")
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = re.sub(r"\s*[-]\s*", "-", text)

    # Match numbers like 13-17, 4.5-10.2, 70 - 99
    match = re.match(r"^\s*([0-9]*\.?[0-9]+)\s*-\s*([0-9]*\.?[0-9]+)\s*$", text)
    if not match:
        return None, None

    lower = float(match.group(1))
    upper = float(match.group(2))
    return lower, upper


def classify_result(result, lower, upper):
    """
    Classify a numeric result as Low, Normal, or High.
    """
    if result is None or lower is None or upper is None:
        return "Unknown"

    try:
        value = float(result)
    except (ValueError, TypeError):
        return "Unknown"

    if value < lower:
        return "Low"
    if value > upper:
        return "High"
    return "Normal"


def analyze_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add analysis columns to the report.

    Expected columns:
    - TestName
    - Result
    - ReferenceRange
    """
    df = df.copy()

    if "TestName" not in df.columns or "Result" not in df.columns:
        raise ValueError("DataFrame must contain 'TestName' and 'Result' columns")

    if "ReferenceRange" not in df.columns:
        df["ReferenceRange"] = ""

    findings = []
    lower_bounds = []
    upper_bounds = []

    for _, row in df.iterrows():
        lower, upper = parse_reference_range(row.get("ReferenceRange", ""))
        lower_bounds.append(lower)
        upper_bounds.append(upper)
        findings.append(classify_result(row.get("Result"), lower, upper))

    df["LowerBound"] = lower_bounds
    df["UpperBound"] = upper_bounds
    df["Finding"] = findings

    # A short human-readable observation for each row
    df["Observation"] = df.apply(
        lambda row: f"{row['TestName']} is {row['Finding']}" if row["Finding"] != "Unknown" else f"{row['TestName']} could not be classified",
        axis=1,
    )

    return df


def summarize_findings(df: pd.DataFrame) -> dict:
    """
    Create a simple summary of low, normal, and high findings.
    """
    summary = {
        "Low": int((df["Finding"] == "Low").sum()) if "Finding" in df.columns else 0,
        "Normal": int((df["Finding"] == "Normal").sum()) if "Finding" in df.columns else 0,
        "High": int((df["Finding"] == "High").sum()) if "Finding" in df.columns else 0,
        "Unknown": int((df["Finding"] == "Unknown").sum()) if "Finding" in df.columns else 0,
    }
    return summary
