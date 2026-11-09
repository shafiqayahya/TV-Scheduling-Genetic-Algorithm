
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
    background: linear-gradient(
        155deg,
        #64152D 0%,
        #881337 56%,
        #BE365A 100%
    ) !important;
    border-right: 1px solid #A72B50;
}

/* SIDEBAR — ALWAYS VISIBLE & STATIC */
@media (min-width: 768px) {
    section[data-testid="stSidebar"] {
        min-width: 330px !important;
        width: 330px !important;
        flex-shrink: 0 !important;
        transform: translateX(0) !important;
        visibility: visible !important;
    }
}

/* HIDE SIDEBAR OPEN & CLOSE BUTTONS */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarNavCollapseButton"],
button[aria-label="Close sidebar"],
button[aria-label="Open sidebar"] {
    display: none !important;
}

/* SIDEBAR CONTENT ALIGNMENT — COMPACT & BALANCED */
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    padding: 0.5rem 1.4rem 1.5rem 1.4rem !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    padding-top: 0 !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* SIDEBAR HEADING */
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-size: 1.30rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.2px;
    padding-bottom: 12px !important;
    margin-top: 0 !important;
    margin-bottom: 2px !important;
    border-bottom: 1px solid rgba(255,255,255,0.25);
}

/* SIDEBAR TEXT — WHITE */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #FFFFFF !important;
}

/* CONSISTENT WIDGET SPACING */
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.85rem !important;
}

section[data-testid="stSidebar"] [data-testid="stElementContainer"] {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
}

/* INPUT LABEL ALIGNMENT */
