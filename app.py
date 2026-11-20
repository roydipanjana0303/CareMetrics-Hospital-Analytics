import hashlib
from io import BytesIO

import pandas as pd
import streamlit as st

from data_processor import (
    clean_dataset,
    compute_analytics,
    demonstrate_indexing_and_slicing,
    inspect_raw_data,
)
from visualizer import (
    plot_admission_line,
    plot_age_histogram,
    plot_cost_boxplot,
    plot_gender_pie,
    plot_hospital_bar,
)

DATA_PROCESSING_VERSION = 3


st.set_page_config(
    page_title="CareMetrics | Hospital Analytics",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
    :root {
        --ink: #21134f;
        --muted: #625e79;
        --purple: #7045dc;
        --lavender: #f0eaff;
        --line: #e9e3f7;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp {
        color: var(--ink);
        background:
            radial-gradient(ellipse at 86% 28%, rgba(208, 187, 255, .30), transparent 34%),
            radial-gradient(ellipse at 7% 72%, rgba(233, 221, 255, .35), transparent 30%),
            linear-gradient(135deg, #fcfaff 0%, #f7f3ff 48%, #fbfaff 100%);
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"] { visibility: hidden; }
    .block-container { max-width: 1440px; padding: .8rem 3.5rem 2.5rem; }
    [data-testid="stSidebar"] { background: #fff; border-right: 1px solid var(--line); }
    [data-testid="stMetric"] {
        background: #fff; border: 1px solid var(--line); border-radius: 16px;
        padding: 17px 19px; box-shadow: 0 8px 26px rgba(49, 31, 100, .055);
    }
    [data-testid="stMetricLabel"] { color: #77718d; font-size: 12px; font-weight: 600; }
    [data-testid="stMetricValue"] { color: var(--ink); font-size: 25px; font-weight: 700; }
    h1, h2, h3 { color: var(--ink); letter-spacing: -.035em; }
    .st-key-site-header {
        min-height: 64px; padding: 0 18px; margin: 0 0 18px;
        background: rgba(255,255,255,.82); border: 1px solid rgba(226,217,246,.9);
        border-radius: 16px; box-shadow: 0 8px 28px rgba(53,34,106,.055);
        backdrop-filter: blur(12px);
    }
    .st-key-site-header [data-testid="stHorizontalBlock"] {
        align-items:center; flex-wrap:nowrap !important; gap:12px;
    }
    .st-key-site-header [data-testid="stColumn"]:first-child {
        flex:0 0 170px !important; width:170px !important; min-width:145px !important;
    }
    .st-key-site-header [data-testid="stColumn"]:last-child {
        flex:1 1 auto !important; width:auto !important; min-width:0 !important;
    }
    .logo { display:flex; align-items:center; gap:10px; color:#2b145d; font-size:20px; font-weight:800; white-space:nowrap; }
    .logo-icon {
        display:grid; place-items:center; width:38px; height:38px;
        color:white; border-radius:13px;
        background:linear-gradient(140deg,#9b61ef,#6738d5);
        box-shadow:0 6px 14px rgba(112,69,220,.25); font-size:19px;
    }
    .st-key-hero { min-height:365px; padding:10px 24px 12px; }
    .st-key-hero [data-testid="stHorizontalBlock"] { align-items:center; gap:24px; }
    .eyebrow {
        display:inline-flex; align-items:center; gap:8px; padding:7px 12px;
        color:#6840cb; background:#f0e9ff; border:1px solid #e6dcff;
        border-radius:30px; font-size:12px; font-weight:700; letter-spacing:.03em;
    }
    .hero-title { margin:14px 0 6px; color:#29145f; font-size:clamp(42px,4.6vw,61px); font-weight:800; line-height:1.02; letter-spacing:-.055em; }
    .hero-subtitle { margin:0 0 14px; color:#2e2354; font-size:clamp(20px,2vw,27px); font-weight:700; line-height:1.2; letter-spacing:-.035em; }
    .hero-copy { max-width:560px; margin:0; color:#625e79; font-size:15px; line-height:1.65; }
    .hero-art {
        width:100%; min-height:320px; display:flex; align-items:center; justify-content:center;
        overflow:hidden; border-radius:30px;
        background:radial-gradient(ellipse at 48% 55%,#e6d9ff 0%,#f2ebff 46%,rgba(248,244,255,.1) 75%);
    }
    .st-key-hero-actions { margin-top:20px; }
    .feature-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:15px; margin:25px 0 12px; }
    .feature-card {
        display:flex; align-items:flex-start; gap:13px; min-height:108px; padding:17px;
        background:rgba(255,255,255,.72); border:1px solid rgba(255,255,255,.95);
        border-radius:18px; box-shadow:0 10px 28px rgba(63,43,122,.055);
    }
    .feature-icon {
        display:grid; place-items:center; flex:0 0 48px; height:48px;
        background:#f0eaff; border-radius:15px; font-size:23px;
    }
    .feature-title { margin:2px 0 5px; color:#2c195e; font-weight:700; font-size:14px; }
    .feature-copy { color:#716b87; font-size:12px; line-height:1.45; }
    .section-heading { margin:12px 0 3px; font-size:27px; font-weight:800; }
    .section-subtitle { margin:0 0 20px; color:#77718d; font-size:14px; }
    .stButton > button {
        min-height:44px; border-radius:12px; border:1px solid #d5c7f5;
        color:#4d2aa4; background:rgba(255,255,255,.8); font-weight:700;
        transition:all .18s ease;
    }
    .stButton > button:hover { border-color:#7045dc; color:#4b25a1; transform:translateY(-1px); }
    .st-key-explore-action .stButton > button {
        color:white; border:0; background:linear-gradient(135deg,#8a52e5,#6334ce);
        box-shadow:0 8px 20px rgba(112,69,220,.24);
    }
    .st-key-explore-action .stButton > button:hover { color:white; border:0; background:#5e31c4; }
    .st-key-upload-action [data-testid="stFileUploaderDropzone"] {
        min-height:44px; padding:4px 8px; border:0; border-radius:12px;
        background:linear-gradient(135deg,#8a52e5,#6334ce);
    }
    .st-key-upload-action [data-testid="stFileUploaderDropzone"] > div {
        min-height:36px; flex-direction:row; justify-content:center; gap:8px;
    }
    .st-key-upload-action [data-testid="stFileUploaderDropzone"] button {
        min-height:34px; padding:4px 12px; border:0; color:#fff;
        background:transparent; font-size:14px; font-weight:700;
    }
    .st-key-upload-action [data-testid="stFileUploaderDropzone"] button:hover {
        color:#fff; border:0; background:rgba(255,255,255,.12);
    }
    .stTabs [data-baseweb="tab-list"] { gap:8px; }
    .stTabs [data-baseweb="tab"] { background:#fff; border:1px solid var(--line); border-radius:10px; padding:0 15px; }
    div[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; }
    .st-key-nav-menu button {
        min-height:38px; padding:8px 7px; border-radius:24px;
        color:#38285f; font-size:12px; font-weight:600; white-space:nowrap;
        text-decoration:none;
    }
    .st-key-nav-menu button:hover { color:#4f2ba6; background:#f2edff; }
    .st-key-nav-menu button[kind="primary"] {
        color:#4f2ba6; background:#e9e0ff; font-weight:700;
    }
    .st-key-upload-action [data-testid="stFileUploaderDropzone"] small,
    .st-key-upload-action [data-testid="stFileUploaderDropzone"] [data-testid="stFileUploaderDropzoneInstructions"] {
        display:none;
    }
    .st-key-hero-actions [data-testid="stHorizontalBlock"] {
        flex-wrap:nowrap !important; gap:10px;
    }
    .st-key-hero-actions [data-testid="stColumn"] {
        flex:1 1 50% !important; width:50% !important; min-width:0 !important;
    }
    @media (max-width: 900px) {
        .block-container { padding: .8rem 1rem 2rem; }
        .st-key-hero { padding:16px 8px; }
        .st-key-site-header { padding:8px 12px; }
        .st-key-site-header [data-testid="stHorizontalBlock"] {
            flex-direction:column !important; align-items:stretch !important; gap:7px;
        }
        .st-key-site-header [data-testid="stColumn"]:first-child,
        .st-key-site-header [data-testid="stColumn"]:last-child {
            flex:1 1 100% !important; width:100% !important; min-width:0 !important;
        }
        .hero-art { min-height:220px; }
        .feature-grid { grid-template-columns:repeat(2,1fr); }
    }
    @media (max-width: 560px) {
        .feature-grid { grid-template-columns:1fr; }
        .hero-title { font-size:43px; }
        .hero-copy { font-size:14px; }
        .st-key-site-header [data-testid="stColumn"]:first-child { flex-basis:128px !important; width:128px !important; min-width:128px !important; }
        .st-key-nav-menu button { padding:6px 3px; font-size:10px; }
        .st-key-hero-actions [data-testid="stHorizontalBlock"] { flex-wrap:wrap !important; }
        .st-key-hero-actions [data-testid="stColumn"] { flex-basis:100% !important; width:100% !important; }
    }
    
    /* CareMetrics professional navigation */
    .st-key-site-header {
        padding: 12px 18px !important;
        border-radius: 18px !important;
    }

    .st-key-nav-menu [data-testid="stHorizontalBlock"] {
        gap: 6px !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
    }

    .st-key-nav-menu [data-testid="stColumn"] {
        min-width: 0 !important;
    }

    .st-key-nav-menu .stButton > button {
        width: 100% !important;
        min-height: 40px !important;
        padding: 8px 5px !important;
        border-radius: 9px !important;
        border: 1px solid transparent !important;
        background: transparent !important;
        color: #51446e !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        white-space: nowrap !important;
        box-shadow: none !important;
        transform: none !important;
    }

    .st-key-nav-menu .stButton > button:hover {
        background: #f1ebff !important;
        color: #6334ce !important;
    }

    .st-key-nav-menu .stButton > button[kind="primary"] {
        background: #eee6ff !important;
        color: #6334ce !important;
        font-weight: 700 !important;
    }

    @media (max-width: 1100px) {
        .st-key-nav-menu {
            overflow-x: auto;
        }
    }

</style>
    """,
    unsafe_allow_html=True,
)


def store_dataset(raw_df, source_name):
    st.session_state["raw_df"] = raw_df
    st.session_state["source_name"] = source_name
    st.session_state["raw_report"] = inspect_raw_data(raw_df)
    st.session_state["cleaned_df"] = clean_dataset(raw_df)
    st.session_state["processing_version"] = DATA_PROCESSING_VERSION


def load_sample_data():
    store_dataset(pd.read_csv("sample_hospital_data.csv"), "Sample hospital dataset")
    st.session_state["upload_signature"] = None


def open_dashboard_with_sample():
    if st.session_state["raw_df"] is None:
        load_sample_data()
    st.session_state["active_page"] = "Dashboard"


def page_heading(title, subtitle):
    st.markdown(
        f'<div class="section-heading">{title}</div><div class="section-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )


def render_hospital_art():
    st.markdown(
        """
        <div class="hero-art">
        <svg viewBox="0 0 640 390" width="100%" role="img" aria-label="Illustration of a hospital and patient analytics">
          <defs>
            <linearGradient id="building" x1="0" x2="1" y1="0" y2="1">
              <stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#e4dcff"/>
            </linearGradient>
            <linearGradient id="purple" x1="0" x2="1" y1="0" y2="1">
              <stop offset="0" stop-color="#a56cf1"/><stop offset="1" stop-color="#6235ce"/>
            </linearGradient>
            <filter id="shadow" x="-30%" y="-30%" width="160%" height="170%">
              <feDropShadow dx="0" dy="12" stdDeviation="12" flood-color="#6849b5" flood-opacity=".20"/>
            </filter>
          </defs>
          <circle cx="320" cy="197" r="155" fill="#e7dcff" opacity=".8"/>
          <circle cx="320" cy="197" r="126" fill="#f3edff"/>
          <path d="M66 321h505" stroke="#bca9ed" stroke-width="4" stroke-linecap="round"/>
          <g filter="url(#shadow)">
            <path d="M166 135h219v183H166z" fill="url(#building)" stroke="#d7ccf2" stroke-width="3"/>
            <path d="M191 108h169v37H191z" fill="#fff" stroke="#ddd3f3" stroke-width="3"/>
            <path d="M215 79h122v34H215z" fill="url(#purple)"/>
            <rect x="266" y="46" width="20" height="62" rx="5" fill="#fff"/>
            <rect x="245" y="67" width="62" height="20" rx="5" fill="#fff"/>
            <rect x="187" y="161" width="37" height="40" rx="4" fill="#b9ddf8"/>
            <rect x="241" y="161" width="37" height="40" rx="4" fill="#b9ddf8"/>
            <rect x="295" y="161" width="37" height="40" rx="4" fill="#b9ddf8"/>
            <rect x="349" y="161" width="22" height="40" rx="4" fill="#b9ddf8"/>
            <rect x="187" y="218" width="37" height="40" rx="4" fill="#b9ddf8"/>
            <rect x="241" y="218" width="37" height="40" rx="4" fill="#b9ddf8"/>
            <rect x="295" y="218" width="37" height="40" rx="4" fill="#b9ddf8"/>
            <path d="M347 318v-52a22 22 0 0 1 44 0v52" fill="#7e56d8"/>
            <path d="M349 318v-51a20 20 0 0 1 40 0v51" fill="#ddd1ff"/>
            <path d="M146 145h20v173h-20zM385 164h81v154h-81z" fill="#f7f3ff" stroke="#d7ccf2" stroke-width="3"/>
            <path d="M397 187h24v30h-24zM432 187h23v30h-23zM397 232h24v30h-24zM432 232h23v30h-23z" fill="#bbdef7"/>
          </g>
          <g filter="url(#shadow)" transform="rotate(8 476 254)">
            <rect x="439" y="172" width="124" height="151" rx="14" fill="#fff" stroke="#d8cdf4" stroke-width="4"/>
            <rect x="466" y="159" width="71" height="23" rx="8" fill="url(#purple)"/>
            <circle cx="477" cy="215" r="13" fill="#dfd5fa"/>
            <path d="M458 249c3-16 34-16 38 0" fill="#b9a2f1"/>
            <rect x="504" y="203" width="43" height="8" rx="4" fill="#c6b5f2"/>
            <rect x="504" y="219" width="32" height="6" rx="3" fill="#e4ddf4"/>
            <path d="M456 280h21l8-14 11 26 9-16 8 4h39" fill="none" stroke="#8458df" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
          </g>
          <g transform="translate(475 80)">
            <path d="M0 68 33 42l23 13 34-42" fill="none" stroke="#9c7beb" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="m81 14 10-1-2 10" fill="none" stroke="#9c7beb" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
            <rect x="2" y="78" width="17" height="30" rx="4" fill="#c9b8f5"/>
            <rect x="29" y="65" width="17" height="43" rx="4" fill="#b9a0f1"/>
            <rect x="56" y="47" width="17" height="61" rx="4" fill="#a88beb"/>
            <rect x="83" y="28" width="17" height="80" rx="4" fill="#9875e5"/>
          </g>
          <g fill="#72bd7b">
            <circle cx="119" cy="286" r="17"/><circle cx="139" cy="279" r="20"/><circle cx="157" cy="290" r="15"/>
            <circle cx="400" cy="296" r="16"/><circle cx="420" cy="286" r="21"/><circle cx="440" cy="297" r="15"/>
          </g>
          <g fill="#6ba66a"><path d="M137 316v-34h5v34zM417 316v-32h5v32z"/></g>
        </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )


page_names = ["Home", "Dashboard", "Preprocessing", "Analysis", "Visualisations", "Dataset"]


if st.session_state.get("active_page") not in page_names:
    st.session_state["active_page"] = "Home"


def navigate_to(destination):
    st.session_state["active_page"] = destination


page = st.session_state["active_page"]

with st.container(key="site-header"):
    header_left, header_nav = st.columns([0.85, 3.15], vertical_alignment="center")
    with header_left:
        st.markdown(
            '<div class="logo"><span class="logo-icon">✚</span>CareMetrics</div>',
            unsafe_allow_html=True,
        )
    with header_nav:
        with st.container(key="nav-menu"):
            nav_columns = st.columns(len(page_names), gap="small")
            for page_name, nav_column in zip(page_names, nav_columns):
                with nav_column:
                    st.button(
                        page_name,
                        key=f"nav_{page_name.lower()}",
                        use_container_width=True,
                        type="primary" if page == page_name else "secondary",
                        on_click=navigate_to,
                        args=(page_name,),
                    )

if "raw_df" not in st.session_state:
    st.session_state["raw_df"] = None

if page == "Home":
    with st.container(key="hero"):
        hero_copy, hero_art = st.columns([1.02, 0.98], vertical_alignment="center")
        with hero_copy:
            st.markdown(
                """
                <span class="eyebrow">✦ &nbsp; HOSPITAL DATA, MADE CLEAR</span>
                <div class="hero-title">CareMetrics</div>
                <div class="hero-subtitle">Hospital Patient Data Analytics &amp; Visualisation</div>
                <p class="hero-copy">
                  Upload hospital patient records, prepare your data, and explore
                  clear insights into admissions, demographics, conditions, and treatment costs.
                  Everything you need to understand your hospital data—in one place.
                </p>
                """,
                unsafe_allow_html=True,
            )
            with st.container(key="hero-actions"):
                action_upload, action_explore = st.columns([1, 1])
                with action_upload:
                    with st.container(key="upload-action"):
                        upload = st.file_uploader(
                            "Upload Dataset",
                            type=["csv"],
                            label_visibility="collapsed",
                            key="home_upload",
                        )
                with action_explore:
                    with st.container(key="explore-action"):
                        st.button(
                            "▮  Explore Dashboard",
                            use_container_width=True,
                            on_click=open_dashboard_with_sample,
                        )
                st.caption("CSV format · Your data stays in this session")
        with hero_art:
            render_hospital_art()

    if upload is not None:
        try:
            upload_bytes = upload.getvalue()
            signature = hashlib.sha256(upload_bytes).hexdigest()
            if st.session_state.get("upload_signature") != signature:
                store_dataset(pd.read_csv(BytesIO(upload_bytes)), upload.name)
                st.session_state["upload_signature"] = signature
            st.success(f"{upload.name} is ready. Choose a section from the navigation.")
        except (pd.errors.ParserError, UnicodeDecodeError, ValueError) as error:
            st.error(f"Could not read this CSV file: {error}")

    st.markdown(
        """
        <div class="feature-grid">
          <div class="feature-card"><div class="feature-icon">▤</div><div><div class="feature-title">Data preprocessing</div><div class="feature-copy">Clean and prepare patient records with a clear quality report.</div></div></div>
          <div class="feature-card"><div class="feature-icon">▥</div><div><div class="feature-title">Data analysis</div><div class="feature-copy">Summarise patient volumes, treatment costs, and hospital trends.</div></div></div>
          <div class="feature-card"><div class="feature-icon">◔</div><div><div class="feature-title">Visualisations</div><div class="feature-copy">Explore trends through concise, easy-to-read charts.</div></div></div>
          <div class="feature-card"><div class="feature-icon">♧</div><div><div class="feature-title">Patient insights</div><div class="feature-copy">Understand demographics, conditions, admissions, and care costs.</div></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


if st.session_state["raw_df"] is None:
    empty_pages = {
        "Dashboard": ("Hospital dashboard", "Upload hospital records to see patient KPIs and trends."),
        "Preprocessing": ("Data preprocessing", "Upload a CSV to inspect missing values, duplicates, and cleaned records."),
        "Analysis": ("Patient data analysis", "Upload a CSV to explore statistical and hospital-level summaries."),
        "Visualisations": ("Visualisations", "Upload a CSV to view admissions, demographics, and cost charts."),
        "Dataset": ("Patient dataset", "Upload a CSV to browse and export patient records."),
    }
    title, subtitle = empty_pages.get(page, ("Hospital analytics", "Upload a patient CSV to get started."))
    page_heading(title, subtitle)
    st.info("No dataset is loaded yet. Upload a CSV from Home or load the sample dataset.")
    if st.button("Load sample dataset", key="load_sample_dataset"):
        load_sample_data()
        st.rerun()
    st.stop()

raw_df = st.session_state["raw_df"]
source_name = st.session_state.get("source_name", "Hospital patient dataset")
raw_report = st.session_state.get("raw_report")
cleaned_df = st.session_state.get("cleaned_df")
if (
    raw_report is None
    or cleaned_df is None
    or st.session_state.get("processing_version") != DATA_PROCESSING_VERSION
):
    store_dataset(raw_df, source_name)
    raw_report = st.session_state["raw_report"]
    cleaned_df = st.session_state["cleaned_df"]

with st.sidebar:
    st.markdown("### Dashboard filters")
    st.caption(f"Data source: {source_name}")
    if st.button("Load sample data", key="load_sample_sidebar", use_container_width=True):
        load_sample_data()
        st.rerun()
    st.divider()
    hospitals = ["All"] + sorted(cleaned_df["Hospital_Name"].dropna().unique().tolist())
    hospital = st.selectbox("Hospital", hospitals)
    conditions = sorted(cleaned_df["Medical_Condition"].dropna().unique().tolist())
    selected_conditions = st.multiselect("Medical condition", conditions, default=conditions)
    ages = pd.to_numeric(cleaned_df["Age"], errors="coerce").dropna() if "Age" in cleaned_df else pd.Series(dtype=float)
    if not ages.empty:
        low_age, high_age = int(ages.min()), int(ages.max())
        age_range = st.slider("Patient age", low_age, high_age, (low_age, high_age))
    else:
        age_range = (0, 120)

age_values = pd.to_numeric(cleaned_df["Age"], errors="coerce") if "Age" in cleaned_df else pd.Series(0, index=cleaned_df.index)
filtered_df = cleaned_df[
    cleaned_df["Medical_Condition"].isin(selected_conditions)
    & age_values.ge(age_range[0])
    & age_values.le(age_range[1])
].copy()
if hospital != "All":
    filtered_df = filtered_df[filtered_df["Hospital_Name"] == hospital]


if page == "Dashboard":
    page_heading("Hospital dashboard", "A live overview of the records in your selected dataset.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total patients", f"{len(filtered_df):,}")
    c2.metric("Hospitals", f"{filtered_df['Hospital_Name'].nunique():,}")
    c3.metric("Average treatment cost", f"₹{filtered_df['Treatment_Cost'].mean():,.0f}" if len(filtered_df) and "Treatment_Cost" in filtered_df else "₹0")
    c4.metric("Average hospital stay", f"{filtered_df['Stay_Days'].mean():.1f} days" if len(filtered_df) and "Stay_Days" in filtered_df else "—")

    row1_left, row1_right = st.columns([1.8, 1], gap="medium")
    with row1_left:
        with st.container(border=True):
            st.markdown("#### Hospital volume")
            if len(filtered_df):
                st.pyplot(plot_hospital_bar(filtered_df), use_container_width=True, clear_figure=True)
            else:
                st.warning("No records match the selected filters.")
    with row1_right:
        with st.container(border=True):
            st.markdown("#### Patient demographics")
            if len(filtered_df):
                st.pyplot(plot_gender_pie(filtered_df), use_container_width=True, clear_figure=True)
            else:
                st.info("No patient records for this selection.")
    row2_left, row2_middle, row2_right = st.columns([1.5, 1, 1], gap="medium")
    with row2_left:
        with st.container(border=True):
            st.markdown("#### Monthly admissions")
            if len(filtered_df):
                st.pyplot(plot_admission_line(filtered_df), use_container_width=True, clear_figure=True)
    with row2_middle:
        with st.container(border=True):
            st.markdown("#### Patient age")
            if len(filtered_df):
                st.pyplot(plot_age_histogram(filtered_df), use_container_width=True, clear_figure=True)
    with row2_right:
        with st.container(border=True):
            st.markdown("#### Treatment costs")
            if len(filtered_df):
                st.pyplot(plot_cost_boxplot(filtered_df), use_container_width=True, clear_figure=True)

elif page == "Preprocessing":
    page_heading("Data preprocessing", "Review data quality and inspect the cleaned patient records.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Raw records", f"{raw_report['rows']:,}")
    c2.metric("Missing values", f"{raw_report['total_missing']:,}")
    c3.metric("Duplicate records", f"{raw_report['duplicates']:,}")
    c4.metric("Clean records", f"{len(cleaned_df):,}")
    st.markdown("#### Missing values by column")
    st.dataframe(pd.Series(raw_report["missing_by_col"], name="Missing values"), use_container_width=True)
    st.markdown("#### Cleaned data preview")
    st.dataframe(cleaned_df.head(100), use_container_width=True)
    st.download_button("Download cleaned CSV", cleaned_df.to_csv(index=False).encode("utf-8"), "caremetrics_cleaned_data.csv", "text/csv")

elif page == "Analysis":
    page_heading("Patient data analysis", "Statistical summaries and hospital-level comparisons.")
    if filtered_df.empty:
        st.warning("No records match the selected filters.")
    else:
        summary, hospital_summary, condition_counts = compute_analytics(filtered_df)
        stat_col, group_col = st.columns(2, gap="large")
        with stat_col:
            st.markdown("#### Descriptive statistics")
            st.dataframe(summary, use_container_width=True)
        with group_col:
            st.markdown("#### Hospital summary")
            st.dataframe(hospital_summary, use_container_width=True)
        st.markdown("#### Patients by medical condition")
        st.dataframe(condition_counts, use_container_width=True)
        _, high_cost = demonstrate_indexing_and_slicing(filtered_df)
        st.markdown("#### Highest treatment cost cases")
        st.dataframe(high_cost, use_container_width=True)

elif page == "Visualisations":
    page_heading("Visualisations", "Explore patient demographics, admission volume, and care costs.")
    if filtered_df.empty:
        st.warning("No records match the selected filters.")
    else:
        left, right = st.columns(2, gap="large")
        with left:
            with st.container(border=True):
                st.pyplot(plot_hospital_bar(filtered_df), use_container_width=True, clear_figure=True)
            with st.container(border=True):
                st.pyplot(plot_age_histogram(filtered_df), use_container_width=True, clear_figure=True)
        with right:
            with st.container(border=True):
                st.pyplot(plot_gender_pie(filtered_df), use_container_width=True, clear_figure=True)
            with st.container(border=True):
                st.pyplot(plot_cost_boxplot(filtered_df), use_container_width=True, clear_figure=True)
        with st.container(border=True):
            st.pyplot(plot_admission_line(filtered_df), use_container_width=True, clear_figure=True)

elif page == "Dataset":
    page_heading("Patient dataset", f"{len(filtered_df):,} records · {source_name}")
    st.dataframe(filtered_df, use_container_width=True, height=540)
    st.download_button("Download filtered records", filtered_df.to_csv(index=False).encode("utf-8"), "caremetrics_filtered_patients.csv", "text/csv")
