import streamlit as st
import pandas as pd
import json
from pathlib import Path
from dataclasses import asdict, is_dataclass
from workflow.health_workflow import run_health_workflow


def make_json_safe(obj):
    if is_dataclass(obj):
        return asdict(obj)

    if hasattr(obj, "to_dict"):
        try:
            return obj.to_dict(orient="records")
        except Exception:
            return obj.to_dict()

    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [make_json_safe(v) for v in obj]

    return obj

# =====================================================================
# PAGE CONFIG
# =====================================================================
st.set_page_config(
    page_title="Health Analysis AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================================
# STYLES  (mobile-first, responsive, single cohesive theme)
# =====================================================================
st.markdown(
    """
    <style>
        :root{
            --bg-1:#0a0f1f;
            --bg-2:#0f1729;
            --bg-3:#111a2e;
            --surface:#131c33;
            --surface-2:#0d1526;
            --border:rgba(148,163,184,0.14);
            --border-strong:rgba(148,163,184,0.26);
            --text:#eef2f8;
            --muted:#94a3b8;
            --accent:#22c55e;
            --accent-2:#38bdf8;
            --accent-3:#a78bfa;
            --danger:#f87171;
            --warn:#fbbf24;
        }

        html, body, .stApp{
            background:
                radial-gradient(1100px 500px at 12% -8%, rgba(56,189,248,0.10), transparent 55%),
                radial-gradient(900px 480px at 100% 0%, rgba(34,197,94,0.10), transparent 55%),
                linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 45%, var(--bg-3) 100%);
            color: var(--text);
        }

        h1,h2,h3,h4,h5,h6,p,label,span,div{ color: var(--text); }
        ::selection{ background: rgba(34,197,94,0.35); }

        .block-container{
            padding-top: 1.1rem;
            padding-bottom: 4rem;
            max-width: 1180px;
        }

        /* ---------------- Hero ---------------- */
        .hero{
            position: relative;
            overflow: hidden;
            border-radius: 24px;
            padding: 30px 28px;
            background: linear-gradient(135deg, rgba(34,197,94,0.16), rgba(56,189,248,0.10));
            border: 1px solid var(--border-strong);
            box-shadow: 0 18px 40px rgba(0,0,0,0.30);
            margin-bottom: 22px;
        }
        .hero-badge{
            display:inline-flex; align-items:center; gap:6px;
            font-size:0.72rem; font-weight:700; letter-spacing:0.06em;
            text-transform:uppercase; color:#bbf7d0;
            background: rgba(34,197,94,0.14);
            border:1px solid rgba(34,197,94,0.35);
            padding:5px 12px; border-radius:999px; margin-bottom:12px;
        }
        .hero h1{ font-size:2.05rem; margin:0 0 8px 0; line-height:1.2; }
        .hero p{ color: var(--muted) !important; font-size:1.02rem; max-width:640px; margin:0; }

        /* ---------------- Cards ---------------- */
        .card{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 20px 20px 14px 20px;
            box-shadow: 0 10px 26px rgba(0,0,0,0.20);
            height: 100%;
        }
        .card h3, .card h4{ margin-top:0; }
        .card-title-row{
            display:flex; align-items:center; gap:10px; margin-bottom:4px;
        }
        .card-icon{
            width:34px; height:34px; border-radius:10px;
            display:flex; align-items:center; justify-content:center;
            background: rgba(56,189,248,0.14); font-size:1.05rem; flex-shrink:0;
        }

        /* ---------------- Step pills ---------------- */
        .step-row{ display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; }
        .step-pill{
            display:flex; align-items:center; gap:8px;
            background: var(--surface-2);
            border:1px solid var(--border);
            border-radius:12px; padding:8px 12px; font-size:0.86rem;
            color: var(--muted) !important; flex:1 1 210px;
        }
        .step-num{
            width:20px; height:20px; border-radius:50%;
            background: linear-gradient(135deg, var(--accent), var(--accent-2));
            color:#04220f !important; font-weight:800; font-size:0.72rem;
            display:flex; align-items:center; justify-content:center; flex-shrink:0;
        }

        /* ---------------- Metric strip ---------------- */
        .metric-card{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 14px 12px;
            text-align: center;
            height:100%;
        }
        .metric-icon{ font-size:1.3rem; margin-bottom:2px; }
        .metric-value{ font-size:1.05rem; font-weight:700; margin:0; color:#f8fafc !important; }
        .metric-label{ margin:2px 0 0 0; color: var(--muted) !important; font-size:0.78rem; }

        /* ---------------- Status chip ---------------- */
        .status-chip{
            display:inline-flex; align-items:center; gap:8px;
            border-radius:12px; padding:10px 14px; font-size:0.9rem;
            border:1px solid var(--border); background: var(--surface-2); width:100%;
            box-sizing:border-box;
        }
        .status-ok{ border-color: rgba(34,197,94,0.4); color:#bbf7d0 !important; }
        .status-idle{ border-color: rgba(148,163,184,0.3); color: var(--muted) !important; }

        /* ---------------- Sidebar ---------------- */
        section[data-testid="stSidebar"]{
            background: rgba(4,8,20,0.97);
            border-right: 1px solid var(--border);
        }
        section[data-testid="stSidebar"] .stMarkdown p{ color: var(--muted) !important; }
        .sidebar-title{
            font-size:1.05rem; font-weight:800; margin-bottom:2px;
        }
        .sidebar-sub{ color: var(--muted) !important; font-size:0.82rem; margin-bottom:10px; }

        /* ---------------- Buttons ---------------- */
        .stButton button{
            border-radius: 12px;
            padding: 0.65rem 1.1rem;
            background: linear-gradient(135deg, #16a34a, #0ea5e9);
            color: white;
            border: none;
            font-weight: 700;
            letter-spacing: 0.01em;
            transition: opacity 0.15s ease, transform 0.15s ease;
            width: 100%;
        }
        .stButton button:hover{ opacity:0.92; transform: translateY(-1px); }

        .stDownloadButton button{
            border-radius: 12px;
            border: 1px solid var(--border-strong) !important;
            background: var(--surface-2) !important;
            color: var(--text) !important;
            font-weight: 600;
            width: 100%;
        }

        /* ---------------- File uploader ---------------- */
        [data-testid="stFileUploaderDropzone"]{
            background: var(--surface-2) !important;
            border: 1.5px dashed var(--border-strong) !important;
            border-radius: 16px !important;
        }

        /* ---------------- Tabs ---------------- */
        .stTabs [data-baseweb="tab-list"]{
            gap: 4px;
            background: var(--surface-2);
            padding: 6px;
            border-radius: 14px;
            border: 1px solid var(--border);
            flex-wrap: wrap;
        }
        .stTabs [data-baseweb="tab"]{
            border-radius: 10px;
            padding: 8px 14px;
            font-weight: 600;
            color: var(--muted) !important;
        }
        .stTabs [aria-selected="true"]{
            background: linear-gradient(135deg, rgba(34,197,94,0.22), rgba(56,189,248,0.18)) !important;
            color: var(--text) !important;
        }

        /* ---------------- Divider spacing ---------------- */
        hr{ border-color: var(--border) !important; }

        /* ---------------- Footer credit ---------------- */
        .footer-credit{
            position: fixed;
            right: 14px;
            bottom: 12px;
            z-index: 9999;
            background: rgba(4,8,20,0.92);
            border: 1px solid var(--border-strong);
            border-radius: 12px;
            padding: 8px 12px;
            font-size: 0.72rem;
            color: var(--muted) !important;
            max-width: 260px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        }

        .small-muted{ color: var(--muted) !important; font-size:0.88rem; }

        /* =============== MOBILE RESPONSIVENESS =============== */
        @media (max-width: 640px){
            .block-container{ padding-left:0.8rem; padding-right:0.8rem; padding-top:0.6rem; }
            .hero{ padding:20px 18px; border-radius:18px; }
            .hero h1{ font-size:1.5rem; }
            .hero p{ font-size:0.92rem; }
            .card{ padding:16px 14px 10px 14px; border-radius:16px; }
            .metric-value{ font-size:0.92rem; }
            .footer-credit{
                left: 12px; right:12px; bottom:8px; max-width:none;
                text-align:center; font-size:0.68rem;
            }
            .stTabs [data-baseweb="tab"]{ padding:7px 10px; font-size:0.85rem; }
        }
    </style>
    <div class="footer-credit">All credit goes to &quot;Shrila Prabhupada Ji&quot; and Guru Maharaj &quot;H.H BPBM Ji&quot;</div>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# HERO
# =====================================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">🩺 AI Health Assistant</div>
        <h1>Health Analysis AI</h1>
        <p>Upload a blood test report, get an instant readable summary, and receive a
        personalized diet, exercise, and daily routine plan — built by AI agents.</p>
        <div class="step-row">
            <div class="step-pill"><span class="step-num">1</span> Upload report</div>
            <div class="step-pill"><span class="step-num">2</span> AI analyzes values</div>
            <div class="step-pill"><span class="step-num">3</span> Get your full plan</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# SIDEBAR — Patient Profile
# =====================================================================
if "final_report" not in st.session_state:
    st.session_state.final_report = None
final_report = st.session_state.final_report

with st.sidebar:
    st.markdown('<div class="sidebar-title">🧑‍⚕️ Patient Profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Fill this in before analyzing your report</div>', unsafe_allow_html=True)

    with st.expander("📥 Need a sample file?", expanded=False):
        sample_csv = Path("sample_data/blood_report.csv")
        if sample_csv.exists():
            with open(sample_csv, "rb") as sample_file:
                sample_bytes = sample_file.read()
            st.download_button(
                label="📥 Download Sample CSV",
                data=sample_bytes,
                file_name="blood_report.csv",
                mime="text/csv",
                use_container_width=True,
            )
        else:
            st.warning("Sample CSV not found.")

    st.markdown("#### Basic Details")
    c1, c2 = st.columns(2)
    with c1:
        age = st.number_input("Age", min_value=0, max_value=120, value=25)
    with c2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    c3, c4 = st.columns(2)
    with c3:
        height = st.number_input("Height (cm)", min_value=0.0, value=170.0, step=0.1)
    with c4:
        weight = st.number_input("Weight (kg)", min_value=0.0, value=65.0, step=0.1)

    st.markdown("#### Lifestyle")
    diet_pref = st.selectbox("Diet Preference", ["Vegetarian", "Eggitarian", "Non-Vegetarian", "Vegan"])
    activity_level = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active"])
    sleep_time = st.selectbox("Preferred Sleep Time", ["9 PM", "10 PM", "11 PM", "12 AM"])

    st.markdown("#### Health Context")
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

# =====================================================================
# QUICK METRIC STRIP
# =====================================================================
m1, m2, m3, m4 = st.columns(4)
metrics = [
    ("📤", "Upload", "CSV / Excel / PDF"),
    ("🤖", "3 AI Agents", "Diet · Exercise · Routine"),
    ("📊", "Smart Summary", "Low / High flags"),
    ("✨", "Powered by", "Gemini AI"),
]
for col, (icon, value, label) in zip((m1, m2, m3, m4), metrics):
    with col:
        st.markdown(
            f"""<div class="metric-card">
                    <div class="metric-icon">{icon}</div>
                    <p class="metric-value">{value}</p>
                    <p class="metric-label">{label}</p>
                </div>""",
            unsafe_allow_html=True,
        )

st.write("")

# =====================================================================
# UPLOAD + PROJECT PLAN
# =====================================================================
left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        """<div class="card-title-row">
                <div class="card-icon">📄</div>
                <h3 style="margin:0;">Upload & Analyze Report</h3>
            </div>""",
        unsafe_allow_html=True,
    )
    st.markdown('<p class="small-muted">Supported formats: CSV, XLSX, XLS, PDF</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Blood Report",
        type=["csv", "xlsx", "xls", "pdf"],
        label_visibility="collapsed",
    )
    if uploaded_file is not None:
        if st.session_state.get("last_uploaded") != uploaded_file.name:
            st.session_state.final_report = None
            st.session_state.last_uploaded = uploaded_file.name

    if uploaded_file is not None:
        st.markdown(
            f'<div class="status-chip status-ok">✅ Loaded: <b>{uploaded_file.name}</b></div>',
            unsafe_allow_html=True,
        )

        st.caption(f"📦 File Size: {uploaded_file.size / 1024:.1f} KB")

    else:
        st.markdown(
            '<div class="status-chip status-idle">📎 No file uploaded yet</div>',
            unsafe_allow_html=True,
        )
    st.write("")
    analyze = st.button("🔍 Analyze Report", use_container_width=True)

    if analyze:
        if uploaded_file is None:
            st.error("Please upload a blood report before analyzing.")
        else:
            st.session_state.final_report = None
            progress = st.progress(0)
            status = st.empty()
            try:
                with st.spinner("🤖 AI is analyzing your report..."):
                    st.session_state.final_report = run_health_workflow(
                        uploaded_file,
                        patient_data,
                        progress,
                        status,
                    )
                
            except Exception as e:
                status.error(str(e))

    final_report = st.session_state.final_report

    if final_report:
        st.write("")
        safe_report = make_json_safe(final_report)

        st.download_button(
            label="📥 Download Full Report (JSON)",
            data=json.dumps(safe_report, indent=4, default=str),
            file_name="Health_Report.json",
            mime="application/json",
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        """<div class="card-title-row">
                <div class="card-icon">🗺️</div>
                <h3 style="margin:0;">How It Works</h3>
            </div>""",
        unsafe_allow_html=True,
    )
    steps = [
        "Upload your CSV / Excel / PDF report",
        "AI reads and previews the data",
        "Test names get normalized",
        "Low / high values are detected",
        "A personalized diet plan is generated",
        "An exercise plan is generated",
        "A daily routine plan is generated",
    ]
    for i, s in enumerate(steps, start=1):
        st.markdown(
            f"""<div class="step-pill" style="margin-bottom:6px; flex:none;">
                    <span class="step-num">{i}</span> {s}
                </div>""",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# =====================================================================
# RESULTS TABS
# =====================================================================
summary_tab, diet_tab, exercise_tab, routine_tab = st.tabs(
    ["🩸 Blood Summary", "🥗 Diet Plan", "🏃 Exercise Plan", "📅 Daily Routine"]
)

final_report = st.session_state.final_report

with summary_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧑 Patient Profile")

    if final_report:
        profile = final_report["patient_profile"]

        profile_df = pd.DataFrame({
            "Field": [
                "Age",
                "Gender",
                "Height",
                "Weight",
                "Diet Preference",
                "Activity Level",
                "Sleep Time",
                "Known Condition",
                "Medications",
                "Allergies"
            ],
            "Value": [
                profile["age"],
                profile["gender"],
                f"{profile['height_cm']} cm",
                f"{profile['weight_kg']} kg",
                profile["diet_preference"],
                profile["activity_level"],
                profile["sleep_time"],
                profile["known_condition"] or "None",
                profile["medications"] or "None",
                profile["allergies"] or "None",
            ]
        })

        st.table(profile_df)
        st.divider()
        st.subheader("🩸 Blood Test Summary")
        st.dataframe(final_report["blood_report_summary"], use_container_width=True)
    else:
        st.info("Click **Analyze Report** to generate results.")
    st.markdown("</div>", unsafe_allow_html=True)

with diet_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🥗 Personalized Diet Plan")

    if final_report:
        st.markdown(final_report["diet_plan"], unsafe_allow_html=False)
    else:
        st.info("No diet plan generated yet.")
    st.markdown("</div>", unsafe_allow_html=True)

with exercise_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏃 Exercise Plan")

    if final_report:
        st.markdown(final_report["exercise_plan"], unsafe_allow_html=False)
    else:
        st.info("No exercise plan generated yet.")
    st.markdown("</div>", unsafe_allow_html=True)

with routine_tab:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📅 Daily Routine")

    if final_report:
        st.markdown(final_report["daily_routine"])
        st.divider()
        st.warning(final_report["medical_disclaimer"])
    else:
        st.info("No routine generated yet.")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# =====================================================================
# NEXT STEP NOTE
# =====================================================================
st.markdown(
    """
    <div class="card">
        <div class="card-title-row">
            <div class="card-icon">🛠️</div>
            <h4 style="margin:0;">Next Build Step</h4>
        </div>
        <p class="small-muted">After this UI works, connect a CSV parser, then normalization and abnormal-value analysis.</p>
    </div>
    """,
    unsafe_allow_html=True,
)