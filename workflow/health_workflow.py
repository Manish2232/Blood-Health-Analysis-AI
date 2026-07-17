import time
from parser.report_loader import load_report
from preprocessing.normalizer import normalize_report
from analysis.blood_analyzer import analyze_report
from patient.profile import create_profile
from agents.diet_agent import generate_diet_plan
from agents.exercise_agent import generate_exercise_plan
from agents.routine_agent import generate_routine_plan
from report.report_generator import generate_final_report


def run_health_workflow(
    uploaded_file,
    patient_data,
    progress=None,
    status=None
):

    # Step 1: Read uploaded file
    try:
    
        if status:
            status.info("📂 Reading Blood Report...")

        report = load_report(uploaded_file)
        print(report.head())
        print(report.columns)


        if progress:
            progress.progress(15)
            time.sleep(0.5)

    # Step 2: Normalize report

        if status:
            status.info("🧹 Normalizing Blood Report...")

        normalized_report = normalize_report(report)
    
        if progress:
            progress.progress(30)
            time.sleep(0.5)

    # Step 3: Analyze report

        if status:
            status.info("🩸 Analyzing Blood Report...")

        analyzed_report = analyze_report(normalized_report)
    
        if progress:
            progress.progress(45)
            time.sleep(0.5)

    # Step 4: Create patient profile

        if status:
            status.info("👤 Creating Patient Profile...")

        profile = create_profile(**patient_data)

        if progress:
            progress.progress(55)
            time.sleep(0.5)

    # Step 5: Generate diet plan

        if status:
            status.info("🥗 Generating Diet Plan...")

        diet = generate_diet_plan(analyzed_report, profile)

        if progress:
            progress.progress(70)
            time.sleep(0.5)

    # Step 6: Generate exercise plan

        if status:
            status.info("🏃 Generating Exercise Plan...")

        exercise = generate_exercise_plan(analyzed_report, profile)

        if progress:
            progress.progress(85)
            time.sleep(0.5)

    # Step 7: Generate daily routine

        if status:
            status.info("📅 Generating Daily Routine...")

        routine = generate_routine_plan(
            analyzed_report,
            profile,
        diet,
            exercise
        )

        if progress:
            progress.progress(95)
            time.sleep(0.5)

    # Step 8: Generate final report

        if status:
            status.info("📑 Preparing Final Report...")

        final_report = generate_final_report(
            profile,
            analyzed_report,
            diet,
            exercise,
            routine
        )

        if progress:
            progress.progress(100)
            time.sleep(0.5)

        if status:
            status.success("✅ Report Generated Successfully!")

        time.sleep(1)

        if progress:
            progress.empty()

        if status:
            status.empty()
    
    
        # All workflow steps
        return final_report

    except Exception as e:
        if status:
            status.error(f"❌ {str(e)}")
        raise

    finally:
        if progress:
            progress.empty()

    if status:
        status.empty()