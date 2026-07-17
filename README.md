# Health Analysis AI

Health Analysis AI is a Streamlit-based multi-agent application that analyzes blood test reports and generates personalized diet, exercise, and daily routine suggestions.

## Features

- Upload blood test report in CSV or Excel format
- Read and normalize report data
- Detect low, normal, and high values
- Collect patient profile details
- Generate:
  - Diet plan
  - Exercise plan
  - Daily routine
- Dark themed responsive Streamlit UI
- Supports Google Gemini and Groq integration

## Project Structure

```text
health_analysis_ai/
├── app.py
├── workflow/
├── parser/
├── preprocessing/
├── analysis/
├── patient/
├── agents/
├── llm/
├── report/
├── .env
└── README.md