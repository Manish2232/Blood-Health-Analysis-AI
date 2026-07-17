from pathlib import Path
import pandas as pd


def load_csv_report(file_obj) -> pd.DataFrame:
    """
    Read an uploaded CSV or Excel file and return a pandas DataFrame.

    Parameters
    ----------
    file_obj : Uploaded file object
        File returned by Streamlit's st.file_uploader.

    Returns
    -------
    pd.DataFrame
        Parsed report data.
    """
    suffix = Path(file_obj.name).suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(file_obj)

    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(file_obj)

    raise ValueError(f"Unsupported file format: {suffix}")


def preview_report(df: pd.DataFrame, rows: int = 5) -> pd.DataFrame:
    """Return the first few rows for preview."""
    return df.head(rows)


def basic_report_info(df: pd.DataFrame) -> dict:
    """Return simple shape and column information."""
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
    }
