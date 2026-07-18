import json
import pandas as pd
from llm.gemini import llm
from utils.llm_helper import get_llm_text


def parse_pdf_text(text):

    prompt = f"""
You are an expert pathology report parser.

Extract every blood test from the report.

Return ONLY valid JSON.

Format:

[
  {{
    "TestName": "",
    "Result": "",
    "Unit": "",
    "ReferenceRange": ""
  }}
]

Report:

{text}
"""

    response = llm.invoke(prompt)

    answer = get_llm_text(response)

    # Remove markdown if Gemini returns ```json
    answer = answer.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(answer)
    except json.JSONDecodeError:
        raise ValueError(f"Gemini returned invalid JSON:\n\n{answer}")

    df = pd.DataFrame(data)

    return df