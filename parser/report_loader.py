from pathlib import Path

from parser.csv_parser import load_csv_report
from parser.pdf_parser import load_pdf_report
from parser.text_parser import parse_pdf_text


def load_report(uploaded_file):

    suffix = Path(uploaded_file.name).suffix.lower()

    if suffix in [".csv", ".xlsx", ".xls"]:
        return load_csv_report(uploaded_file)

    elif suffix == ".pdf":

        text = load_pdf_report(uploaded_file)

        df = parse_pdf_text(text)

        return df

    else:
        raise ValueError("Unsupported file format")