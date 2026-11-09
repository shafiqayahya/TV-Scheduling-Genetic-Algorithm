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

/* TRIAL COMPARISON TABLE */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* TRIAL EXPANDER */
[data-testid="stExpander"] {
    border: 1px solid #F4D8E0 !important;
    border-radius: 12px !important;
}

/* MAIN BUTTON STYLE */
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

# FIXED GA PARAMETERS
generations = 100
population_size = 50
seed = 42

with st.sidebar:
    st.header('GA Control Panel')

    co_r = st.slider('Crossover Rate (CO_R)', 0.0, 0.95, 0.80, 0.01)

    mut_r = st.number_input('Mutation Rate (MUT_R)', min_value=0.0, max_value=1.0, value=0.2, step=0.01, format='%.2f')

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

    else:
        st.caption(f"{len(trials)} of 3 trials saved for comparison.")

        comparison_df = pd.DataFrame([
            {
                'Trial': f"Trial {t['trial']}",
                'Crossover Rate (CO_R)': t['co_r'],
                'Mutation Rate (MUT_R)': t['mut_r'],
                'Generations': t['generations'],
                'Population Size': t['population_size'],
                'Random Seed': t['seed'],
                'Best Fitness': t['score'],
                'Upper Bound': t['upper'],
                'Fitness (%)': (
                    100 * t['score'] / t['upper']
                    if t['upper'] else 0
                )
            }
            for t in trials
        ])

        st.subheader('Trial Results Summary')

        st.dataframe(
            comparison_df,
            width='stretch',
            hide_index=True,
            column_config={
                'Crossover Rate (CO_R)': st.column_config.NumberColumn(format='%.2f'),
                'Mutation Rate (MUT_R)': st.column_config.NumberColumn(format='%.2f'),
                'Best Fitness': st.column_config.NumberColumn(format='%.2f'),
                'Upper Bound': st.column_config.NumberColumn(format='%.2f'),
                'Fitness (%)': st.column_config.NumberColumn(format='%.1f%%')
            }
        )

        st.subheader('Fitness Comparison')

        fitness_df = comparison_df[
            ['Trial', 'Best Fitness']
        ].set_index('Trial')

        st.bar_chart(
            fitness_df,
            width='stretch',
            color='#A7234A'
        )

        st.subheader('Generated Schedule for Each Trial')

        for t in trials:
            with st.expander(f"Trial {t['trial']} - Generated TV Schedule"):

                st.caption(
                    f"CO_R={t['co_r']:.2f} · "
                    f"MUT_R={t['mut_r']:.2f} · "
                    f"Generations={t['generations']} · "
                    f"Population={t['population_size']} · "
                    f"Seed={t['seed']}"
                )

                st.metric(
                    'Best Fitness',
                    f"{t['score']:.2f}"
                )

                trial_schedule_df = pd.DataFrame(t['rows'])

                st.dataframe(
                    trial_schedule_df,
                    width='stretch',
                    hide_index=True
                )

                st.download_button(
                    f"⬇ Download Trial {t['trial']} Schedule",
                    trial_schedule_df.to_csv(index=False),
                    f"trial_{t['trial']}_schedule.csv",
                    'text/csv',
                    width='stretch',
                    key=f"download_trial_{t['trial']}"
                )

        if len(trials) == 3:
            best_trial = max(trials, key=lambda t: t['score'])

            st.markdown(
                '<div class="burgundy-info">'
                f"All three trials completed. "
                f"Trial {best_trial['trial']} achieved the highest fitness "
                f"of {best_trial['score']:.2f}."
                '</div>',
                unsafe_allow_html=True
            )

        if st.button('Clear Saved Trials', width='stretch'):
            st.session_state.trials = []
            st.rerun()

with changes:
    st.subheader('Rating Changes')

    if not ORIGINAL.is_file():
        st.markdown(
            '<div class="burgundy-info">'
            'Original ratings CSV is not available. '
            'Add program_ratings_original.csv to compare rating changes.'
            '</div>',
            unsafe_allow_html=True
        )

    else:
        try:
            original_df = pd.read_csv(ORIGINAL)
            modified_df = pd.read_csv(MODIFIED)

            st.subheader('Original Program Ratings')

            st.dataframe(
                original_df,
                width='stretch',
                hide_index=True
            )

            st.subheader('Modified Program Ratings')

            st.dataframe(
                modified_df,
                width='stretch',
                hide_index=True
            )

            st.subheader('Rating Changes Comparison')

            if (
                original_df.columns.tolist() == modified_df.columns.tolist()
                and len(original_df) == len(modified_df)
            ):
                original_numeric = original_df.select_dtypes(
                    include='number'
                ).columns.tolist()

                modified_numeric = modified_df.select_dtypes(
                    include='number'
                ).columns.tolist()

                numeric_columns = [
                    col for col in original_numeric
                    if col in modified_numeric
                ]

                if numeric_columns:
                    comparison_changes = modified_df.copy()

                    for col in numeric_columns:
                        comparison_changes[f'{col} Change'] = (
                            modified_df[col] - original_df[col]
                        )

                    st.dataframe(
                        comparison_changes,
                        width='stretch',
                        hide_index=True
                    )

                    changed_cells = (
                        original_df.ne(modified_df)
                        & original_df.notna().combine(
                            modified_df.notna(),
                            lambda a, b: a or b
                        )
                    )

                    changed_rows = changed_cells.any(axis=1).sum()

                    a,b = st.columns(2)

                    a.metric(
                        'Total Records',
                        len(modified_df)
                    )

                    b.metric(
                        'Rows with Changes',
                        int(changed_rows)
                    )

                    st.caption(
                        'Rating differences are calculated as '
                        'Modified Rating - Original Rating. '
                        'Rows are compared in their existing order.'
                    )

                else:
                    st.info(
                        'No matching numeric rating columns were found '
                        'for calculating rating differences.'
                    )

            else:
                st.warning(
                    'Original and modified CSV files have different '
                    'columns or row counts. Both datasets are displayed '
                    'above, but automatic row-by-row comparison is not available.'
                )

        except Exception as exc:
            st.error(f'Could not compare rating CSV files: {exc}')
