import pdfplumber
import pandas as pd


def load_pdf_report(uploaded_file):
    rows = []

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                rows.extend(table)

    if not rows:
        raise ValueError("No table found in PDF report.")

    df = pd.DataFrame(rows[1:], columns=rows[0])

    # Clean column names
    df.columns = [str(col).strip().lower() for col in df.columns]

    return df