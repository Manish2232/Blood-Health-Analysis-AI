import json
import re
from io import BytesIO
from typing import Any, Dict, List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def _escape_html(value: Any) -> str:
    text = str(value)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _clean_text(value: Any) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, (dict, list)):
        return json.dumps(value, indent=2, default=str)
    return str(value)


def format_report_text(report: Dict[str, Any]) -> str:
    profile = report.get("patient_profile", {})
    summary = report.get("blood_report_summary", {})
    diet = report.get("diet_plan", "")
    exercise = report.get("exercise_plan", "")
    routine = report.get("daily_routine", "")
    disclaimer = report.get("medical_disclaimer", "")

    lines = [
        "HEALTH ANALYSIS REPORT",
        f"Generated At: {report.get('generated_at', 'N/A')}",
        "",
        "PATIENT PROFILE",
        "-" * 80,
    ]

    if isinstance(profile, dict):
        for key, value in profile.items():
            lines.append(f"{key.replace('_', ' ').title()}: {_clean_text(value)}")
    else:
        lines.append(_clean_text(profile))

    lines.extend([
        "",
        "BLOOD REPORT SUMMARY",
        "-" * 80,
    ])

    if isinstance(summary, dict):
        for key, value in summary.items():
            lines.append(f"{key}: {_clean_text(value)}")
    else:
        lines.append(_clean_text(summary))

    lines.extend([
        "",
        "DIET PLAN",
        "-" * 80,
        _clean_text(diet),
        "",
        "EXERCISE PLAN",
        "-" * 80,
        _clean_text(exercise),
        "",
        "DAILY ROUTINE",
        "-" * 80,
        _clean_text(routine),
        "",
        "DISCLAIMER",
        "-" * 80,
        _clean_text(disclaimer),
    ])

    return "\n".join(lines)


def _as_bullet_lines(text: Any) -> List[str]:
    raw = _clean_text(text).strip()
    if not raw:
        return ["No details available."]

    lines = []
    for line in raw.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        cleaned = re.sub(r"^[-*•]\s*", "", cleaned)
        cleaned = re.sub(r"^\d+[.)]\s*", "", cleaned)
        lines.append(cleaned)

    if not lines:
        lines = [raw]
    return lines


def _add_section_heading(story, styles, title: str):
    story.append(Paragraph(f"<b>{_escape_html(title)}</b>", styles["Heading2"]))
    story.append(Spacer(1, 8))


def _add_key_value_block(story, styles, mapping: Dict[str, Any]):
    for key, value in mapping.items():
        story.append(
            Paragraph(
                f"<b>{_escape_html(key.replace('_', ' ').title())}:</b> {_escape_html(_clean_text(value))}",
                styles["BodyText"],
            )
        )
    story.append(Spacer(1, 10))


def _add_bullet_list(story, styles, items: List[str]):
    bullet_items = [
        ListItem(Paragraph(f"<bullet>&bull;</bullet> {_escape_html(item)}", styles["BodyText"]))
        for item in items
    ]
    story.append(ListFlowable(bullet_items, bulletType="bullet", bulletColor=colors.HexColor("#0F766E"), leftIndent=18, spaceBefore=4, spaceAfter=4))
    story.append(Spacer(1, 10))


def _normalize_table_value(value: Any) -> str:
    text = _clean_text(value)
    if len(text) > 180:
        text = text[:175].rstrip() + "..."
    return text


def _summary_to_rows(summary: Any) -> List[List[str]]:
    rows = [["Test", "Value"]]

    if isinstance(summary, dict):
        for key, value in summary.items():
            rows.append([_normalize_table_value(key), _normalize_table_value(value)])
        return rows

    if isinstance(summary, list):
        for item in summary:
            if isinstance(item, dict):
                for key, value in item.items():
                    rows.append([_normalize_table_value(key), _normalize_table_value(value)])
            else:
                rows.append(["Summary", _normalize_table_value(item)])
        return rows

    rows.append(["Summary", _normalize_table_value(summary)])
    return rows


def _add_table(story, styles, title: str, rows: List[List[str]], col_widths: List[int]):
    _add_section_heading(story, styles, title)
    table = Table(rows, colWidths=col_widths)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.8, colors.HexColor("#93C5FD")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EFF6FF")]),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 7),
                ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 14))


def _extract_routine_rows(text: Any) -> List[List[str]]:
    content = _clean_text(text)
    lines = [line.strip() for line in content.splitlines() if line.strip()]

    if not lines:
        return [["General", "No routine details available."]]

    rows = []
    seen_times = set()

    for line in lines:
        if ":" not in line:
            if rows and rows[-1][0] == "General":
                rows[-1][1] = f"{rows[-1][1]} {line}".strip()
            else:
                rows.append(["General", line])
            continue

        label, value = [part.strip() for part in line.split(":", 1)]
        if not label or not value:
            continue

        normalized_label = label.strip()
        if normalized_label.lower() in {"general", "note", "notes"}:
            if rows and rows[-1][0] == "General":
                rows[-1][1] = f"{rows[-1][1]} {value}".strip()
            else:
                rows.append(["General", value])
            continue

        if normalized_label not in seen_times:
            rows.append([normalized_label, value])
            seen_times.add(normalized_label)
        else:
            for row in rows:
                if row[0] == normalized_label:
                    row[1] = f"{row[1]} {value}".strip()
                    break

    if not rows:
        rows.append(["General", content])
    return rows


def build_report_pdf(report: Dict[str, Any]) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    story = []
    styles = getSampleStyleSheet()

    profile = report.get("patient_profile", {})
    patient_name = ""
    if isinstance(profile, dict):
        patient_name = str(profile.get("name") or profile.get("patient_name") or "Patient").strip()
    elif profile:
        patient_name = str(profile).strip()

    story.append(Paragraph("HEALTH ANALYSIS REPORT", styles["Title"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"<font color='#0F172A' size=18><b>{_escape_html(patient_name)}</b></font>", styles["Heading1"]))
    story.append(Paragraph(f"<b>Generated At:</b> {_escape_html(report.get('generated_at', 'N/A'))}", styles["BodyText"]))
    story.append(Spacer(1, 18))

    summary = report.get("blood_report_summary", {})

    _add_section_heading(story, styles, "Patient Profile")
    if isinstance(profile, dict):
        _add_key_value_block(story, styles, profile)
    else:
        story.append(Paragraph(_escape_html(_clean_text(profile)), styles["BodyText"]))
        story.append(Spacer(1, 10))

    summary_rows = _summary_to_rows(summary)
    _add_table(story, styles, "Blood Report Summary", summary_rows, [210, 290])

    _add_section_heading(story, styles, "Diet Plan")
    _add_bullet_list(story, styles, _as_bullet_lines(report.get("diet_plan", "")))

    _add_section_heading(story, styles, "Exercise Plan")
    _add_bullet_list(story, styles, _as_bullet_lines(report.get("exercise_plan", "")))

    _add_section_heading(story, styles, "Daily Routine")
    for slot, action in _extract_routine_rows(report.get("daily_routine", "")):
        story.append(Paragraph(f"<b>{_escape_html(slot)}</b>: {_escape_html(action)}", styles["BodyText"]))
        story.append(Spacer(1, 6))
    story.append(Spacer(1, 10))

    _add_section_heading(story, styles, "Disclaimer")
    story.append(Paragraph(_escape_html(_clean_text(report.get("medical_disclaimer", ""))), styles["BodyText"]))
    story.append(Spacer(1, 12))

    doc.build(story)
    return buffer.getvalue()
