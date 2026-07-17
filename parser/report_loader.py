from pathlib import Path
from parser.csv_parser import load_csv_report
from parser.pdf_parser import load_pdf_report


def load_report(file_obj):
    suffix = Path(file_obj.name).suffix.lower()

    if suffix == ".csv":
        return load_csv_report(file_obj)

    if suffix in {".xlsx", ".xls"}:
        return load_csv_report(file_obj)

    if suffix == ".pdf":
        return load_pdf_report(file_obj)

    raise ValueError(f"Unsupported file format: {suffix}")