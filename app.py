import streamlit as st
from workflow.health_workflow import run_health_workflow
from pathlib import Path

st.set_page_config(
    page_title="Health Analysis AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styles ----------
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #0b1020 0%, #0f172a 45%, #111827 100%);
            color: #e5e7eb;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 5rem;
            max-width: 1200px;
        }

        h1, h2, h3, h4, h5, h6, p, label, div {
            color: #e5e7eb !important;
        }

        .hero {
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.18), rgba(16, 185, 129, 0.12));
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 22px;
            padding: 26px 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
            margin-bottom: 18px;
        }

        .card {
            background: rgba(15, 23, 42, 0.88);
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 20px;
            padding: 18px 18px 8px 18px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
            min-height: 170px;
        }

        .metric-card {
            background: rgba(17, 24, 39, 0.92);
            border: 1px solid rgba(96, 165, 250, 0.2);
            border-radius: 18px;
            padding: 14px 16px;
            text-align: center;
        }

        .metric-value {
            font-size: 1.7rem;
            font-weight: 700;
            margin: 0;
            color: #f8fafc;
        }

        .metric-label {
            margin: 0;
            color: #94a3b8 !important;
            font-size: 0.9rem;
        }

        .footer-credit {
            position: fixed;
            right: 16px;
            bottom: 16px;
            z-index: 9999;
            background: rgba(17, 24, 39, 0.92);
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 14px;
            padding: 10px 12px;
            font-size: 0.78rem;
            color: #e5e7eb;
            max-width: 280px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
        }

        .small-muted {
            color: #94a3b8 !important;
            font-size: 0.9rem;
        }

        .stButton button {
            border-radius: 12px;
            padding: 0.6rem 1rem;
            background: linear-gradient(135deg, #2563eb, #10b981);
            color: white;
            border: none;
            font-weight: 600;
        }

        .stButton button:hover {
            border: none;
            opacity: 0.95;
        }

        section[data-testid="stSidebar"] {
            background: rgba(2, 6, 23, 0.95);
            border-right: 1px solid rgba(148, 163, 184, 0.12);
        }
        
        .loader-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 14px;
            padding: 28px 18px;
            border-radius: 18px;
            background: rgba(15, 23, 42, 0.92);
            border: 1px solid rgba(148, 163, 184, 0.22);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
            margin-top: 12px;
        }

        .loader-ring {
            width: 54px;
            height: 54px;
            border: 5px solid rgba(148, 163, 184, 0.22);
            border-top: 5px solid #10b981;
            border-right: 5px solid #2563eb;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        .loader-text {
            font-size: 1rem;
            font-weight: 600;
            color: #e5e7eb;
            text-align: center;
        }

        .loader-subtext {
            font-size: 0.85rem;
            color: #94a3b8;
            text-align: center;
        }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    </style>
    <div class="footer-credit">All credit goes to &quot;Shrila Prabhupada Ji&quot; and Guru Maharaj &quot;H.H BPBM Ji&quot;</div>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown(
    """
    <div class="hero">
        <h1>🩺 Health Analysis AI</h1>
        <p>Upload a blood test report, preview the data, and prepare it for AI-based diet, exercise, and daily routine generation.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## Patient Profile")
    uploaded_file = st.file_uploader(
        "Upload Blood Report",
        type=["csv", "xlsx", "xls"],
        help="Start with CSV or Excel for the first version.",
    )
    st.markdown("---")
    st.markdown("### Sample Blood Report")

    sample_csv = Path("sample_data/blood_report.csv")

    if sample_csv.exists():
        with open(sample_csv, "rb") as file:
            st.download_button(
                label="📥 Download Sample CSV",
                data=file,
                file_name="blood_report.csv",
                mime="text/csv",
            )
    else:
        st.warning("Sample CSV not found.")

    st.markdown("### Basic Details")
    age = st.number_input("Age", min_value=0, max_value=120, value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    height = st.number_input("Height (cm)", min_value=0.0, value=170.0, step=0.1)
    weight = st.number_input("Weight (kg)", min_value=0.0, value=65.0, step=0.1)

    st.markdown("### Lifestyle")
    diet_pref = st.selectbox("Diet Preference", ["Vegetarian", "Eggitarian", "Non-Vegetarian", "Vegan"])
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active"])
    sleep_time = st.selectbox("Preferred Sleep Time", ["9 PM", "10 PM", "11 PM", "12 AM"])

    st.markdown("### Health Context")
    condition = st.text_input("Known Condition / Concern", placeholder="e.g. diabetes, anemia, thyroid")
    medications = st.text_input("Current Medication", placeholder="Optional")
    allergies = st.text_input("Food Allergies", placeholder="Optional")
    patient_data = {
        "age": age,
        "gender": gender,
        "height_cm": height,
        "weight_kg": weight,
        "diet_preference": diet_pref,
        "activity_level": activity_level,
        "sleep_time": sleep_time,
        "known_condition": condition,
        "medications": medications,
        "allergies": allergies,
}





# ---------- Main Area ----------
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        '<div class="metric-card"><p class="metric-value">1</p><p class="metric-label">Upload Step</p></div>',
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        '<div class="metric-card"><p class="metric-value">3</p><p class="metric-label">AI Agents Later</p></div>',
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        '<div class="metric-card"><p class="metric-value">Dark</p><p class="metric-label">Modern Theme</p></div>',
        unsafe_allow_html=True,
    )
with col4:
    st.markdown(
        '<div class="metric-card"><p class="metric-value">CSV</p><p class="metric-label">First Version</p></div>',
        unsafe_allow_html=True,
    )

st.write("")

left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Upload & Analyze Blood Report")
    st.write("Upload the blood report here.")

    if "final_report" not in st.session_state:
        st.session_state.final_report = None

    if uploaded_file is not None:
        st.success(f"Loaded file: {uploaded_file.name}")
    else:
        st.info("No file uploaded yet.")

    analyze = st.button("Analyze Report")

    if analyze:

        if uploaded_file is None:
            st.error("Please upload a blood report.")

        else:
            loader = st.empty()
            loader.markdown(
                """
                <div class="loader-box">
                    <div class="loader-ring"></div>
                    <div class="loader-text">Analyzing blood report...</div>
                    <div class="loader-subtext">Reading file, normalizing values, and generating diet, exercise, and routine plans.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            try:
                st.session_state.final_report = run_health_workflow(
                    uploaded_file,
                    patient_data
                )

                st.success("Health report generated successfully.")

            except Exception as e:
                st.error(str(e))

            finally:
                loader.empty()

    final_report = st.session_state.final_report

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 2) Project Plan")
    st.markdown(
        """
        - Step 1: Upload CSV or Excel
        - Step 2: Read and preview data
        - Step 3: Normalize test names
        - Step 4: Detect low/high values
        - Step 5: Generate diet plan
        - Step 6: Generate exercise plan
        - Step 7: Generate routine plan
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

summary_tab, diet_tab, exercise_tab, routine_tab = st.tabs(
    ["Blood Summary", "Diet Plan", "Exercise Plan", "Daily Routine"]
)

with summary_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### Blood Test Summary")

    if final_report:
        st.dataframe(final_report["blood_report_summary"], use_container_width=True)
    else:
        st.info("Click 'Analyze Report' to generate results.")

    st.markdown("</div>", unsafe_allow_html=True)

with diet_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🥗 Personalized Diet Plan")

    if final_report:
        st.markdown(final_report["diet_plan"], unsafe_allow_html=False)
    else:
        st.info("No diet plan generated.")

    st.markdown("</div>", unsafe_allow_html=True)

with exercise_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏃 Exercise Plan")

    if final_report:
        st.markdown(final_report["exercise_plan"], unsafe_allow_html=False)
    else:
        st.info("No exercise plan generated.")

    st.markdown("</div>", unsafe_allow_html=True)

with routine_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📅 Daily Routine")

    if final_report:
        st.markdown(final_report["daily_routine"], unsafe_allow_html=False)
    else:
        st.info("No routine generated.")

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.markdown(
    """
    <div class="card">
        <h4>Next Build Step</h4>
        <p class="small-muted">After this UI works, connect a CSV parser, then normalization and abnormal-value analysis.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
