import pandas as pd

import workflow.health_workflow as workflow


def test_run_health_workflow_avoids_artificial_sleep(monkeypatch):
    def fail_sleep(*args, **kwargs):
        raise AssertionError("Artificial delay should not be used in workflow")

    monkeypatch.setattr(workflow.time, "sleep", fail_sleep)
    monkeypatch.setattr(workflow, "load_report", lambda uploaded_file: pd.DataFrame({"test": [1, 2]}))
    monkeypatch.setattr(workflow, "normalize_report", lambda report: {"normalized": True})
    monkeypatch.setattr(workflow, "analyze_report", lambda normalized_report: {"analyzed": True})
    monkeypatch.setattr(workflow, "create_profile", lambda **kwargs: {"name": "Asha"})
    monkeypatch.setattr(workflow, "generate_diet_plan", lambda analyzed_report, profile: "diet plan")
    monkeypatch.setattr(workflow, "generate_exercise_plan", lambda analyzed_report, profile: "exercise plan")
    monkeypatch.setattr(workflow, "generate_routine_plan", lambda analyzed_report, profile, diet, exercise: "routine plan")
    monkeypatch.setattr(
        workflow,
        "generate_final_report",
        lambda profile, analyzed_report, diet, exercise, routine: {"ok": True, "diet": diet, "exercise": exercise, "routine": routine},
    )

    result = workflow.run_health_workflow(None, {"name": "Asha"})

    assert result["ok"] is True
    assert result["diet"] == "diet plan"
    assert result["exercise"] == "exercise plan"
