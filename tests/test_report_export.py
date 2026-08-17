from pypdf import PdfReader

from report.exporter import build_report_pdf, format_report_text


def test_format_report_text_contains_sections():
    report = {
        "generated_at": "17-08-2026 10:00:00",
        "patient_profile": {
            "name": "Asha Sharma",
            "age": 32,
            "gender": "female",
        },
        "blood_report_summary": {"Hemoglobin": "12.5 g/dL"},
        "diet_plan": "Eat more greens.",
        "exercise_plan": "Walk 30 minutes daily.",
        "daily_routine": "Sleep by 11 PM.",
        "medical_disclaimer": "Educational use only.",
    }

    text = format_report_text(report)

    assert "HEALTH ANALYSIS REPORT" in text
    assert "Asha Sharma" in text
    assert "Hemoglobin" in text
    assert "Eat more greens." in text


def test_build_report_pdf_returns_pdf_bytes():
    report = {
        "generated_at": "17-08-2026 10:00:00",
        "patient_profile": {"name": "Asha Sharma"},
        "blood_report_summary": {"Hemoglobin": "12.5 g/dL"},
        "diet_plan": "Eat more greens.",
        "exercise_plan": "Walk 30 minutes daily.",
        "daily_routine": "Sleep by 11 PM.",
        "medical_disclaimer": "Educational use only.",
    }

    pdf_bytes = build_report_pdf(report)

    assert pdf_bytes.startswith(b"%PDF")

    reader = PdfReader(__import__("io").BytesIO(pdf_bytes))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert "Asha Sharma" in text
    assert "HEALTH ANALYSIS REPORT" in text


def test_build_profile_table_normalizes_mixed_value_types():
    from app import build_profile_table

    profile = {
        "name": "Asha Sharma",
        "age": 32,
        "gender": "Female",
        "height_cm": 165.0,
        "weight_kg": 62.0,
        "diet_preference": "Vegetarian",
    }

    profile_df = build_profile_table(profile)

    assert list(profile_df.columns) == ["Field", "Value"]
    assert profile_df["Value"].map(type).nunique() == 1
    assert profile_df.loc[profile_df["Field"] == "Gender", "Value"].iat[0] == "Female"
