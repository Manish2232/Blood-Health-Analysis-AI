import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

load_dotenv()

try:
    google_api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    google_api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemma-4-31b-it",
    google_api_key=google_api_key,
    temperature=0
)