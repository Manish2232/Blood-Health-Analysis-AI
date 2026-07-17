from typing import Dict, Any
from llm.gemini import llm


def build_routine_prompt(report_summary: Dict[str, Any], profile: Dict[str, Any], diet_plan: Dict[str, Any], exercise_plan: Dict[str, Any]) -> str:
    """
    Build a prompt for the routine agent using blood report summary, patient profile,
    diet plan, and exercise plan.
    """
    return f"""
You are a daily routine planning agent for a health analysis application.

Patient Profile:
{profile}

Blood Report Summary:
{report_summary}

Diet Plan:
{diet_plan}

Exercise Plan:
{exercise_plan}

Task:
Create a practical full-day routine.
Focus on:
- wake-up time
- sleep time
- meal timing
- exercise timing
- work/study blocks
- rest and hydration
- recovery guidance

Rules:
- Do not diagnose disease.
- Keep the advice safe and general.
- Make the routine compatible with the diet and exercise plan.
- If data is missing, make reasonable general suggestions.
- Return your response using exactly this format:

Wake-up Time:
...

Morning Routine:
...

Breakfast:
...

Work / Study Schedule:
...

Lunch:
...

Evening Exercise:
...

Dinner:
...

Sleep Time:
...

Additional Recommendations:
...
""".strip()


def generate_routine_plan(
    report_summary: Dict[str, Any],
    profile: Dict[str, Any],
    diet_plan: Dict[str, Any],
    exercise_plan: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Placeholder daily-routine agent output.
    Replace this with an LLM call later.
    """
    prompt = build_routine_prompt(report_summary, profile, diet_plan, exercise_plan)
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