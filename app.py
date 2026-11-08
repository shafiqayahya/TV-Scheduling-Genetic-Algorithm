from pathlib import Path
import pandas as pd
import streamlit as st
from ga_engine import load_ratings, run_ga

st.set_page_config(page_title='TV Scheduling GA', page_icon='📺', layout='wide')
st.title('📺 TV Scheduling Using Genetic Algorithm')
st.caption('JIE42903 – Evolutionary Computing | Scheduling with modified program ratings')

ratings, hours = load_ratings(Path(__file__).with_name('program_ratings_modified.csv'))
st.info('The assignment specifies default MUT_R = 0.20 but also lists an experimental range of 0.01–0.05. The default is preserved here; confirm the intended range with the lecturer.')

with st.sidebar:
    st.header('GA Parameters')
    co_r = st.slider('Crossover Rate (CO_R)', min_value=0.0, max_value=0.95, value=0.8, step=0.01)
    mut_r = st.number_input('Mutation Rate (MUT_R)', min_value=0.0, max_value=1.0, value=0.20, step=0.01, format='%.2f', help='For the three assignment trials, test values between 0.01 and 0.05 unless lecturer clarifies otherwise.')
    generations = st.number_input('Generations', min_value=1, max_value=2000, value=100)
    population_size = st.number_input('Population Size', min_value=4, max_value=1000, value=50)
    seed = st.number_input('Random Seed', min_value=0, max_value=1000000, value=42)
    run = st.button('▶ Run Genetic Algorithm', type='primary', use_container_width=True)

st.subheader('Modified Program Ratings')
with st.expander('View input CSV data'):
    st.dataframe(pd.read_csv(Path(__file__).with_name('program_ratings_modified.csv')), use_container_width=True)

if 'results' not in st.session_state:
    st.session_state.results = []
if run:
    rows, score, upper, history = run_ga(ratings, hours, co_r, mut_r, int(generations), int(population_size), seed=int(seed))
    st.session_state.current = {'rows': rows, 'score': score, 'upper': upper, 'history': history,
                                'co_r': co_r, 'mut_r': mut_r, 'seed': seed}

if 'current' in st.session_state:
    result = st.session_state.current
    st.subheader('Generated TV Schedule')
    a, b, c = st.columns(3)
    a.metric('Total Fitness (Rating)', f"{result['score']:.2f}")
    b.metric('Maximum Possible Rating*', f"{result['upper']:.2f}")
    c.metric('Fitness / Upper Bound', f"{result['score']/result['upper']:.1%}" if result['upper'] else 'N/A')
    st.dataframe(pd.DataFrame(result['rows']), use_container_width=True, hide_index=True)
    st.caption('*Upper bound assumes any program may be repeated in different slots and ignores additional scheduling restrictions.')
    st.subheader('Best Fitness by Generation')
    st.line_chart(pd.DataFrame(result['history']).set_index('Generation'))
    st.download_button('Download Schedule CSV', pd.DataFrame(result['rows']).to_csv(index=False), 'generated_schedule.csv', 'text/csv')
    if st.button('Save this trial for comparison'):
        st.session_state.results.append({'Trial': len(st.session_state.results)+1,
                                         'CO_R': result['co_r'], 'MUT_R': result['mut_r'],
                                         'Seed': result['seed'], 'Fitness': round(result['score'], 4),
                                         'Schedule': ' | '.join(r['Program'] for r in result['rows'])})
        st.success('Trial saved in this session.')

st.subheader('Trial Comparison')
if st.session_state.results:
    comparison = pd.DataFrame(st.session_state.results)
    st.dataframe(comparison, use_container_width=True, hide_index=True)
    st.download_button('Download Trial Comparison CSV', comparison.to_csv(index=False), 'trial_comparison.csv', 'text/csv')
    if st.button('Clear saved trials'):
        st.session_state.results = []
        st.rerun()
else:
    st.caption('Run GA and save each trial to compare parameter combinations.')
