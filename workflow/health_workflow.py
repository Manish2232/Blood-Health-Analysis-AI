from parser.csv_parser import load_report
from preprocessing.normalizer import normalize_report
from analysis.blood_analyzer import analyze_report
from patient.profile import create_profile
from agents.diet_agent import generate_diet_plan
from agents.exercise_agent import generate_exercise_plan
from agents.routine_agent import generate_routine_plan
from report.report_generator import generate_final_report


def run_health_workflow(uploaded_file, patient_data):

    # Step 1: Read uploaded file
    report = load_report(uploaded_file)

    # Step 2: Normalize report
    normalized_report = normalize_report(report)

    # Step 3: Analyze report
    analyzed_report = analyze_report(normalized_report)

    # Step 4: Create patient profile
    profile = create_profile(**patient_data)

    # Step 5: Generate diet plan
    diet = generate_diet_plan(analyzed_report, profile)

    # Step 6: Generate exercise plan
    exercise = generate_exercise_plan(analyzed_report, profile)

    # Step 7: Generate daily routine
    routine = generate_routine_plan(
        analyzed_report,
        profile,
        diet,
        exercise
    )

    # Step 8: Generate final report
    final_report = generate_final_report(
        profile,
        analyzed_report,
        diet,
        exercise,
        routine
    )

    return final_report