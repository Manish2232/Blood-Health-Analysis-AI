from datetime import datetime
from typing import Dict, Any
from dataclasses import asdict, is_dataclass    

def generate_final_report(
    patient_profile: Dict[str, Any],
    blood_summary: Dict[str, Any],
    diet_plan: Dict[str, Any],
    exercise_plan: Dict[str, Any],
    routine_plan: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Merge all agent outputs into one final report.
    """

    report = {
        "generated_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),

        "patient_profile": asdict(patient_profile) if is_dataclass(patient_profile) else patient_profile,

        "blood_report_summary": blood_summary,

        "diet_plan": diet_plan,

        "exercise_plan": exercise_plan,

        "daily_routine": routine_plan,

        "medical_disclaimer":
        (
            "This report is AI-generated for educational purposes only. "
            "It is not a medical diagnosis or prescription. "
            "Consult a qualified healthcare professional before making "
            "medical decisions."
        )
    }

    return report


def print_report(report: Dict[str, Any]):

    print("=" * 80)
    print("HEALTH ANALYSIS REPORT")
    print("=" * 80)

    print("\nGenerated At:")
    print(report["generated_at"])

    print("\nPATIENT PROFILE")
    print("-" * 80)
    print(report["patient_profile"])

    print("\nBLOOD REPORT SUMMARY")
    print("-" * 80)
    print(report["blood_report_summary"])

    print("\nDIET PLAN")
    print("-" * 80)
    print(report["diet_plan"])

    print("\nEXERCISE PLAN")
    print("-" * 80)
    print(report["exercise_plan"])

    print("\nDAILY ROUTINE")
    print("-" * 80)
    print(report["daily_routine"])

    print("\nDISCLAIMER")
    print("-" * 80)
    print(report["medical_disclaimer"])