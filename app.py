from pathlib import Path
import pandas as pd
import streamlit as st
from ga_engine import load_ratings, run_ga

st.set_page_config(page_title='TV Scheduling | Genetic Algorithm', page_icon='📺', layout='wide', initial_sidebar_state='expanded')
ROOT = Path(__file__).resolve().parent
MODIFIED = ROOT / 'program_ratings_modified.csv'
ORIGINAL = ROOT / 'program_ratings_original.csv'

st.markdown('''<style>
.block-container {padding-top:1.5rem;max-width:1250px;}
.hero {background:linear-gradient(110deg,#64152D,#881337,#BE365A);padding:30px;border-radius:16px;color:white;margin-bottom:20px;}
.hero h1 {color:white!important;margin:0;font-size:2.2rem;}
.hero p {color:#FFE8EE;margin:8px 0 0;}
[data-testid="stMetric"] {background:#FFF4F6;border:1px solid #F4D8E0;padding:14px;border-radius:12px;}

/* SIDEBAR — BURGUNDY & ROSE THEME */
section[data-testid="stSidebar"] {
    background:linear-gradient(155deg,#64152D 0%,#881337 56%,#BE365A 100%) !important;
    border-right:1px solid #A72B50;
}

/* SIDEBAR — COMPACT TOP ALIGNMENT */
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    padding:0.65rem 1.35rem 1.4rem !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div {
    padding-top:0 !important;
    margin-top:0 !important;
}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap:0.85rem !important;
}
section[data-testid="stSidebar"] [data-testid="stElementContainer"] {
    margin-bottom:0 !important;
}

/* SIDEBAR HEADING */
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-size:1.25rem !important;
    font-weight:700 !important;
    margin:0 !important;
    padding:0 0 0.7rem !important;
    border-bottom:1px solid rgba(255,244,247,.35);
}

/* SIDEBAR TEXT — WHITE */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color:#FFFFFF !important;
}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    margin-bottom:0.25rem !important;
}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    font-size:0.89rem !important;
    font-weight:600 !important;
}

/* SIDEBAR SLIDER — LIGHT ROSE */
section[data-testid="stSidebar"] [data-testid="stSlider"] {
    accent-color:#FFF4F7 !important;
}
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] {
    --slider-color:#FFF4F7;
}
section[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background:#FFF4F7 !important;
    border:2px solid #F4C7D4 !important;
}
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stSliderTrack"],
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stSliderTrackFill"] {
    background:#FFF4F7 !important;
}

/* SIDEBAR NUMBER INPUT */
section[data-testid="stSidebar"] input {
    background-color:#FFF4F7 !important;
    color:#64152D !important;
    -webkit-text-fill-color:#64152D !important;
}
section[data-testid="stSidebar"] [data-testid="stNumberInput"] [data-baseweb="input"] {
    min-height:43px !important;
    border-radius:10px !important;
    overflow:hidden;
}
section[data-testid="stSidebar"] [data-testid="stNumberInput"] button {
    background:#FFE5EC !important;
    color:#64152D !important;
}
