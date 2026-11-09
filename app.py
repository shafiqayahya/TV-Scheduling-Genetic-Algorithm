from pathlib import Path
import pandas as pd
import streamlit as st
from ga_engine import load_ratings, run_ga

st.set_page_config(
    page_title="TV Scheduling | Genetic Algorithm",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).parent
MODIFIED = ROOT / "program_ratings_modified.csv"
ORIGINAL = ROOT / "program_ratings_original.csv"

st.markdown("""
<style>
:root {--rose:#BE365A;--burgundy:#881337;--wine:#64152D;--blush:#FFF1F4;}
.block-container {padding-top:1.6rem;padding-bottom:3rem;max-width:1250px;}
.hero {background:linear-gradient(115deg,#64152D 0%,#881337 58%,#BE365A 100%);padding:32px 34px;border-radius:19px;color:white;margin-bottom:20px;box-shadow:0 12px 30px rgba(100,21,45,.15);}
.hero .eyebrow {color:#FFDCE5;font-size:12px;letter-spacing:1.4px;font-weight:700;}
.hero h1 {color:#FFFFFF !important;margin:8px 0;font-size:2.35rem;line-height:1.2;}
.hero p {color:#FFE8EE;margin:0;font-size:15px;}
[data-testid="stMetric"] {background:#FFF4F6;border:1px solid #F4D8E0;padding:17px;border-radius:14px;}
[data-testid="stMetricLabel"] {color:#75233F;}
[data-testid="stMetricValue"] {color:#881337;}
.stButton>button[kind="primary"] {background:#A7234A;border-color:#A7234A;color:white;border-radius:11px;font-weight:700;}
.stButton>button[kind="primary"]:hover {background:#881337;border-color:#881337;color:white;}
section[data-testid="stSidebar"] {background:#FFF4F6;border-right:1px solid #F4D8E0;}
[data-testid="stTabs"] button[aria-selected="true"] {color:#881337;}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {background:#BE365A;}
[data-testid="stDataFrame"] {border:1px solid #F0D6DF;border-radius:12px;overflow:hidden;}
a {color:#A7234A;}
/* Sidebar Rose & Burgundy theme — visual changes only */
section[data-testid="stSidebar"] {
    background: linear-gradient(155deg,#64152D 0%,#881337 56%,#BE365A 100%);
    border-right: 1px solid #A72B50;
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stTickBar"] {
    color: #FFE5ED;
}
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: #FFE0E9 !important;
    border-color: #FFE0E9 !important;
}
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] div[style*="background"] {
    accent-color: #F9A8C0;
}
section[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
    background: #FFF4F7 !important;
    color: #64152D !important;
    -webkit-text-fill-color: #64152D;
}
section[data-testid="stSidebar"] [data-testid="stNumberInput"] [data-baseweb="input"] {
    background: #FFF4F7;
    border-radius: 10px;
}
section[data-testid="stSidebar"] [data-testid="stNumberInput"] button {
    background: #FFE5EC !important;
    color: #64152D !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #E65A83 !important;
    border: 1px solid #F6B3C6 !important;
    color: #FFFFFF !important;
    border-radius: 12px;
    font-weight: 700;
    box-shadow: 0 5px 15px rgba(52,8,25,.2);
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: #A7234A !important;
    border-color: #FFE0E9 !important;
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: rgba(255,244,247,.97);
    border: 1px solid #F4C7D4;
}
section[data-testid="stSidebar"] [data-testid="stMetricLabel"] p,
section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: #881337 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,228,237,.38);
}
</style>
""", unsafe_allow_html=True)
