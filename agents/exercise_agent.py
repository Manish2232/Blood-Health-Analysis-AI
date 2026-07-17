from typing import Dict, Any
from llm.gemini import llm


def build_exercise_prompt(report_summary: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """
    Build a prompt for the exercise agent using blood report summary and patient profile.
    """
    return f"""
You are an exercise planning agent for a health analysis application.

Patient Profile:
{profile}

Blood Report Summary:
{report_summary}

Task:
Create a safe, personalized exercise plan.
Focus on:
- suitable exercise types
- duration
- intensity
- frequency
- precautions
- exercises to avoid

Rules:
- Do not diagnose disease.
- Keep the advice safe and general.
- Base the plan on the abnormal findings and the patient's lifestyle.
- If data is missing, make reasonable general suggestions.
- Return the answer in clear sections.
""".strip()


def generate_exercise_plan(report_summary: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """
    Placeholder exercise-agent output.
    Replace this with an LLM call later.
    """
    prompt = build_exercise_prompt(report_summary, profile)
    # response = llm.invoke(prompt)

    # Temporary static output for development/testing.
    # Later you will send 'prompt' to Gemini/Grok and parse the result.
    # return response.content
    response = llm.invoke(prompt)

    answer = ""

    for item in response.content:
        if item["type"] == "text":
         answer = item["text"]

    return answer
