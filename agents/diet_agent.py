
from typing import Dict, Any
from llm.gemini import llm



def build_diet_prompt(report_summary: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """
    Build a prompt for the diet agent using blood report summary and patient profile.
    """
    return f"""
You are a diet planning agent for a health analysis application.

Patient Profile:
{profile}

Blood Report Summary:
{report_summary}

Task:
Create a practical, personalized diet plan.
Focus on:
- foods to eat
- foods to avoid
- breakfast, lunch, dinner, and snack suggestions
- hydration guidance
- meal timing

Rules:
- Do not diagnose disease.
- Keep the advice safe and general.
- Base the plan on the abnormal findings and the patient's lifestyle.
- If data is missing, make reasonable general suggestions.
- Return the answer in Markdown format.
- Use proper headings and bullet points.
- Do NOT return JSON.
- Do NOT return Python dictionaries.
- Do NOT include the prompt in the response.
""".strip()


def generate_diet_plan(report_summary: Dict[str, Any], profile: Dict[str, Any]) -> str:
    """
    Placeholder diet-agent output.
    Replace this with an LLM call later.
    """
    
    prompt = build_diet_prompt(report_summary, profile)

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
