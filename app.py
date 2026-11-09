
from pathlib import Path
import pandas as pd
import streamlit as st
from ga_engine import load_ratings, run_ga

st.set_page_config(page_title='TV Scheduling | Genetic Algorithm', page_icon='📺', layout='wide', initial_sidebar_state='expanded')

ROOT = Path(__file__).resolve().parent
MODIFIED = ROOT / 'program_ratings_modified.csv'
ORIGINAL = ROOT / 'program_ratings_original.csv'

st.markdown('''<style>

/* MAIN PAGE */
.block-container {
    padding-top: 1.5rem;
    max-width: 1250px;
}

/* MAIN BANNER */
.hero {
    background: linear-gradient(110deg,#64152D,#881337,#BE365A);
    padding: 30px;
    border-radius: 16px;
    color: white;
    margin-bottom: 20px;
}

.hero h1 {
    color: white !important;
    margin: 0;
    font-size: 2.2rem;
}

.hero p {
    color: #FFE8EE;
    margin: 8px 0 0;
}

/* MAIN METRIC CARDS */
[data-testid="stMetric"] {
    background: #FFF4F6;
    border: 1px solid #F4D8E0;
    padding: 14px;
    border-radius: 12px;
}

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
        min-width: 320px !important;
        width: 320px !important;
        flex-shrink: 0 !important;
        transform: translateX(0) !important;
        visibility: visible !important;
    }
}

/* HIDE SIDEBAR OPEN & CLOSE BUTTONS */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarNavCollapseButton"],
section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] button,
button[aria-label="Close sidebar"],
button[aria-label="Open sidebar"] {
    display: none !important;
}

/* REMOVE SIDEBAR HEADER EMPTY SPACE */
section[data-testid="stSidebar"] [data-testid="stSidebarHeader"] {
    min-height: 0 !important;
    height: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
}

/* SIDEBAR CONTENT ALIGNMENT */
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    padding: 1.15rem 1.35rem 1.25rem 1.35rem !important;
}

/* MOVE SIDEBAR CONTENT UP */
section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    padding-top: 0 !important;
}

/* SIDEBAR HEADING — CENTER */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
    text-align: center !important;
    font-size: 1.28rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px;
    padding-bottom: 12px !important;
    margin-top: 0 !important;
    margin-bottom: 16px !important;
    border-bottom: 1px solid rgba(255,255,255,0.25);
}

/* SIDEBAR TEXT — WHITE */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #FFFFFF !important;
}

/* CONSISTENT SIDEBAR WIDGET SPACING */
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 0.9rem !important;
}

/* INPUT LABEL ALIGNMENT */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    margin-bottom: 6px !important;
}

section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    line-height: 1.35 !important;
}

/* SIDEBAR SLIDER */
section[data-testid="stSidebar"] [data-testid="stSlider"] {
    accent-color: #FFF4F7 !important;
    padding-bottom: 0 !important;
}

section[data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] {
    --slider-color: #FFF4F7;
}

section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stSliderTrack"] {
    background: #FFF4F7 !important;
}

section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stSliderTrackFill"] {
    background: #FFF4F7 !important;
}

section[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
    background: #FFF4F7 !important;
    border: 2px solid #FFF4F7 !important;
    box-shadow: 0 0 0 1px #F4C7D4 !important;
}

/* CROSSOVER RATE — HIDE BUILT-IN END LABELS */
section[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stTickBar"] {
    display: none !important;
}

/* CROSSOVER RATE — PERMANENT MIN & MAX VALUES */
.crossover-range {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-top: -8px;
    margin-bottom: 4px;
    padding: 0 5px;
    box-sizing: border-box;
}

.crossover-range span {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-size: 0.85rem;
    font-weight: 500;
    line-height: 1.3;
}

/* SIDEBAR NUMBER INPUT */
section[data-testid="stSidebar"] input {
    background-color: #FFF4F7 !important;
    color: #64152D !important;
    -webkit-text-fill-color: #64152D !important;
}

/* NUMBER INPUT — CONSISTENT HEIGHT */
section[data-testid="stSidebar"] [data-testid="stNumberInput"] [data-baseweb="input"] {
    min-height: 42px !important;
    border-radius: 10px !important;
    overflow: hidden;
}

/* SIDEBAR NUMBER INPUT BUTTONS */
section[data-testid="stSidebar"] [data-testid="stNumberInput"] button {
    background: #FFE5EC !important;
    color: #64152D !important;
}

/* RUN GENETIC ALGORITHM BUTTON */
section[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: #FFF4F7 !important;
    border: 1px solid #FFF4F7 !important;
    color: #64152D !important;
    border-radius: 11px !important;
    font-weight: 700 !important;
    width: 100% !important;
    min-height: 45px !important;
    font-size: 0.91rem !important;
    margin-top: 4px !important;
}

section[data-testid="stSidebar"] .stButton button[kind="primary"] p,
section[data-testid="stSidebar"] .stButton button[kind="primary"] span {
    color: #64152D !important;
    -webkit-text-fill-color: #64152D !important;
}

section[data-testid="stSidebar"] .stButton button[kind="primary"] svg {
    color: #64152D !important;
    fill: #64152D !important;
}

section[data-testid="stSidebar"] .stButton button[kind="primary"]:hover {
    background: #FFE5EC !important;
    border-color: #F4C7D4 !important;
    color: #64152D !important;
}

/* SIDEBAR SAVED TRIALS CARD */
section[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: #FFF4F7 !important;
    border: 1px solid #F4C7D4 !important;
    padding: 14px 17px !important;
    border-radius: 12px !important;
    min-height: 92px !important;
}

/* SIDEBAR SAVED TRIALS TEXT AND NUMBER */
section[data-testid="stSidebar"] [data-testid="stMetricLabel"] p,
section[data-testid="stSidebar"] [data-testid="stMetricValue"],
section[data-testid="stSidebar"] [data-testid="stMetricValue"] > div {
    color: #64152D !important;
    -webkit-text-fill-color: #64152D !important;
}

section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    margin-bottom: 5px !important;
}

section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 600 !important;
}

/* MAIN INFORMATION BOX — BURGUNDY GRADIENT */
.burgundy-info {
    background: linear-gradient(
        110deg,
        #64152D 0%,
        #881337 58%,
        #BE365A 100%
    ) !important;
    border: 1px solid #881337 !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin-top: 12px;
    margin-bottom: 16px;
    color: #FFFFFF !important;
    font-size: 16px;
    line-height: 1.5;
}

.burgundy-info p,
.burgundy-info span {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    margin: 0 !important;
}

/* ORIGINAL MAIN BUTTON STYLE */
.stButton button[kind="primary"] {
    background: #A7234A;
    border-color: #A7234A;
    color: white;
}

</style>''', unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>📺 TV Scheduling Optimizer</h1><p>JIE42903 · Evolutionary Computing · Genetic Algorithm</p></div>', unsafe_allow_html=True)

if not MODIFIED.is_file():
    st.error('Missing program_ratings_modified.csv. Add this file to the same GitHub folder as app.py.')
    st.stop()

try:
    ratings, hours = load_ratings(MODIFIED)
except Exception as exc:
    st.error(f'Could not load ratings CSV: {exc}')
    st.stop()

if 'trials' not in st.session_state:
    st.session_state.trials = []

with st.sidebar:
    st.header('GA Control Panel')

    co_r = st.slider('Crossover Rate (CO_R)', 0.0, 0.95, 0.80, 0.01)

    st.markdown(
        '<div class="crossover-range">'
        '<span>0.00</span>'
        '<span>0.95</span>'
        '</div>',
        unsafe_allow_html=True
    )

    mut_r = st.number_input('Mutation Rate (MUT_R)', min_value=0.0, max_value=1.0, value=0.20, step=0.01, format='%.2f')

    generations = st.number_input('Generations', 1, 2000, 100)

    population_size = st.number_input('Population Size', 4, 1000, 50)

    seed = st.number_input('Random Seed', 0, 1000000, 42)

    run = st.button('Run Genetic Algorithm', icon=':material/play_arrow:', type='primary', width='stretch')

    st.metric('Saved Trials', len(st.session_state.trials))

if run:
    try:
        with st.spinner('Optimizing schedule...'):
            rows, score, upper, history = run_ga(
                ratings, hours, crossover_rate=co_r, mutation_rate=mut_r,
                generations=int(generations), population_size=int(population_size),
                seed=int(seed))

        st.session_state.current = dict(
            rows=rows,
            score=score,
            upper=upper,
            history=history,
            co_r=co_r,
            mut_r=mut_r,
            generations=int(generations),
            population_size=int(population_size),
            seed=int(seed)
        )

        st.success('Schedule generated successfully.')

    except Exception as exc:
        st.error(f'GA execution failed: {exc}')

current = st.session_state.get('current')

if current:
    a,b,c = st.columns(3)
    a.metric('Best Fitness', f"{current['score']:.2f}")
    b.metric('Upper Bound', f"{current['upper']:.2f}")
    c.metric('Fitness / Upper Bound', f"{100*current['score']/current['upper']:.1f}%" if current['upper'] else 'N/A')

else:
    a,b,c = st.columns(3)
    a.metric('Time Slots', len(hours))
    b.metric('Program Categories', len(ratings))
    c.metric('Saved Trials', len(st.session_state.trials))

scheduler, comparison, changes = st.tabs(['GA Scheduler', 'Trial Comparison', 'Rating Changes'])

with scheduler:
    st.subheader('Generated TV Schedule')

    if current is None:
        st.markdown(
            '<div class="burgundy-info">'
            'Set parameters in the sidebar and click Run Genetic Algorithm.'
            '</div>',
            unsafe_allow_html=True
        )

    else:
        st.caption(f"CO_R={current['co_r']:.2f} · MUT_R={current['mut_r']:.2f} · Generations={current['generations']} · Population={current['population_size']} · Seed={current['seed']}")

        schedule_df = pd.DataFrame(current['rows'])

        st.dataframe(schedule_df, width='stretch', hide_index=True)

        st.subheader('Fitness Convergence')

        st.line_chart(pd.DataFrame(current['history']).set_index('Generation'), width='stretch')

        left,right = st.columns(2)

        with left:
            st.download_button(
                '⬇ Download Schedule CSV',
                schedule_df.to_csv(index=False),
                'generated_schedule.csv',
                'text/csv',
                width='stretch'
            )

        with right:
            if st.button('💾 Save Trial for Comparison', width='stretch'):
                if len(st.session_state.trials) >= 3:
                    st.warning('Three trials already saved. Clear trials to start again.')
                else:
                    st.session_state.trials.append({
                        **current,
                        'trial': len(st.session_state.trials) + 1
                    })
                    st.rerun()

with comparison:
    st.subheader('Three-Trial Experiment Comparison')

    trials = st.session_state.trials

    if not trials:
        st.markdown(
            '<div class="burgundy-info">'
            'Run GA and save up to three trials in the GA Scheduler tab.'
            '</div>',
            unsafe_allow_html=True
        )
