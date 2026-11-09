
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

/* SIDEBAR TEXT — WHITE */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #FFFFFF !important;
}

/* SIDEBAR SLIDER */
section[data-testid="stSidebar"] [data-testid="stSlider"] {
    accent-color: #FFF4F7;
}

/* SIDEBAR NUMBER INPUT */
section[data-testid="stSidebar"] input {
    background-color: #FFF4F7 !important;
    color: #64152D !important;
    -webkit-text-fill-color: #64152D !important;
}

/* SIDEBAR NUMBER INPUT BUTTONS */
section[data-testid="stSidebar"] [data-testid="stNumberInput"] button {
    background: #FFE5EC !important;
    color: #64152D !important;
}

/* SIDEBAR RUN BUTTON */
section[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background:#F9A8C0 !important;
    border: 1px solid #F6B3C6 !important;
    color: #FFFFFF !important;
    border-radius: 12px;
    font-weight: 700;
}

section[data-testid="stSidebar"] .stButton button[kind="primary"]:hover {
    background: #A7234A !important;
    border-color: #FFE0E9 !important;
}

/* ORIGINAL MAIN BUTTON STYLE */
.stButton button[kind="primary"] {
    background:#A7234A;
    border-color:#A7234A;
    color:white;
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
    mut_r = st.number_input('Mutation Rate (MUT_R)', min_value=0.0, max_value=1.0, value=0.20, step=0.01, format='%.2f')
    st.caption('Check the lecturer’s permitted mutation range before final trials.')
    generations = st.number_input('Generations', 1, 2000, 100)
    population_size = st.number_input('Population Size', 4, 1000, 50)
    seed = st.number_input('Random Seed', 0, 1000000, 42)
    run = st.button('▶ Run Genetic Algorithm', type='primary', width='stretch')
    st.metric('Saved Trials', len(st.session_state.trials))

if run:
    try:
        with st.spinner('Optimizing schedule...'):
            rows, score, upper, history = run_ga(
                ratings, hours, crossover_rate=co_r, mutation_rate=mut_r,
                generations=int(generations), population_size=int(population_size),
                seed=int(seed))
        st.session_state.current = dict(rows=rows, score=score, upper=upper, history=history,
                                        co_r=co_r, mut_r=mut_r, generations=int(generations),
                                        population_size=int(population_size), seed=int(seed))
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
        st.info('Set parameters in the sidebar and click Run Genetic Algorithm.')
    else:
        st.caption(f"CO_R={current['co_r']:.2f} · MUT_R={current['mut_r']:.2f} · Generations={current['generations']} · Population={current['population_size']} · Seed={current['seed']}")
        schedule_df = pd.DataFrame(current['rows'])
        st.dataframe(schedule_df, width='stretch', hide_index=True)
        st.subheader('Fitness Convergence')
        st.line_chart(pd.DataFrame(current['history']).set_index('Generation'), width='stretch')
        left,right = st.columns(2)
        with left:
            st.download_button('⬇ Download Schedule CSV', schedule_df.to_csv(index=False), 'generated_schedule.csv', 'text/csv', width='stretch')
        with right:
            if st.button('💾 Save Trial for Comparison', width='stretch'):
                if len(st.session_state.trials) >= 3:
                    st.warning('Three trials already saved. Clear trials to start again.')
                else:
                    st.session_state.trials.append({**current, 'trial':len(st.session_state.trials)+1})
                    st.rerun()

with comparison:
    st.subheader('Three-Trial Experiment Comparison')
    trials = st.session_state.trials
    if not trials:
        st.info(
            'Run GA and save up to three trials '
            'in the GA Scheduler tab.'
        )
