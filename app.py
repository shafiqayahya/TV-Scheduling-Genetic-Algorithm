
from pathlib import Path
from html import escape

import pandas as pd
import streamlit as st

from ga_engine import load_ratings, run_ga


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TV Scheduling | Genetic Algorithm",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT = Path(__file__).resolve().parent
MODIFIED = ROOT / "program_ratings_modified.csv"
ORIGINAL = ROOT / "program_ratings_original.csv"


# ============================================================
# CUSTOM CSS - BURGUNDY ROSE THEME
# ============================================================

st.markdown("""
<style>

/* MAIN PAGE */

.block-container {
    padding-top: 1.5rem;
    max-width: 1250px;
}

/* MAIN BANNER */

.hero {
    background: linear-gradient(
        110deg,
        #64152D,
        #881337,
        #BE365A
    );
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

/* SIDEBAR THEME */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        155deg,
        #64152D 0%,
        #881337 56%,
        #BE365A 100%
    ) !important;
    border-right: 1px solid #A72B50;
}

/* STATIC SIDEBAR */

@media (min-width: 768px) {
    section[data-testid="stSidebar"] {
        min-width: 320px !important;
        width: 320px !important;
        flex-shrink: 0 !important;
        transform: translateX(0) !important;
        visibility: visible !important;
    }
}

/* HIDE SIDEBAR CONTROLS */

[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarNavCollapseButton"],
section[data-testid="stSidebar"]
[data-testid="stSidebarHeader"] button,
button[aria-label="Close sidebar"],
button[aria-label="Open sidebar"] {
    display: none !important;
}

/* REMOVE SIDEBAR HEADER SPACE */

section[data-testid="stSidebar"]
[data-testid="stSidebarHeader"] {
    min-height: 0 !important;
    height: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
}

/* SIDEBAR PADDING */

section[data-testid="stSidebar"]
[data-testid="stSidebarUserContent"] {
    padding: 2rem 1.35rem 2rem 1.35rem !important;
    box-sizing: border-box !important;
}

section[data-testid="stSidebar"]
[data-testid="stSidebarContent"] {
    padding-top: 0 !important;
}

/* SIDEBAR HEADING */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
    text-align: center !important;
    font-size: 1.28rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px;
    padding-bottom: 14px !important;
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    border-bottom: 1px solid rgba(255,255,255,0.25);
}

/* SIDEBAR TEXT */

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"]
[data-testid="stWidgetLabel"] p {
    color: white !important;
}

/* SIDEBAR SPACING */

section[data-testid="stSidebar"]
[data-testid="stVerticalBlock"] {
    gap: 1.5rem !important;
}

/* BALANCED SIDEBAR DISTRIBUTION */

@media (min-width: 768px) and (min-height: 650px) {

    section[data-testid="stSidebar"]
    [data-testid="stSidebarUserContent"] {
        min-height: 100dvh !important;
        display: flex !important;
        flex-direction: column !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stSidebarUserContent"]
    > [data-testid="stVerticalBlock"] {
        flex: 1 1 auto !important;
        min-height: 0 !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        gap: 1.5rem !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stSidebarUserContent"]
    > div > [data-testid="stVerticalBlock"] {
        flex: 1 1 auto !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        gap: 1.5rem !important;
    }
}

/* SMALL SCREEN SPACING */

@media (max-width: 767px), (max-height: 649px) {

    section[data-testid="stSidebar"]
    [data-testid="stSidebarUserContent"] {
        min-height: auto !important;
        padding: 1.5rem 1.35rem 1.75rem 1.35rem !important;
    }

    section[data-testid="stSidebar"]
    [data-testid="stVerticalBlock"] {
        gap: 1.2rem !important;
    }
}

/* INPUT LABELS */

section[data-testid="stSidebar"]
[data-testid="stWidgetLabel"] {
    margin-bottom: 8px !important;
}

section[data-testid="stSidebar"]
[data-testid="stWidgetLabel"] p {
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    line-height: 1.35 !important;
}

/* ============================================================
   SIDEBAR SLIDERS - BURGUNDY ROSE
   Applies to both CO_R and MUT_R
   ============================================================ */

section[data-testid="stSidebar"]
[data-testid="stSlider"] {
    accent-color: #BE365A !important;
    padding-bottom: 0 !important;
}

section[data-testid="stSidebar"]
[data-testid="stSlider"]
[data-baseweb="slider"] {
    --slider-color: #BE365A;
}

/* Slider track */

section[data-testid="stSidebar"]
[data-testid="stSlider"]
[data-testid="stSliderTrack"] {
    background: #D77A96 !important;
}

/* Selected slider track */

section[data-testid="stSidebar"]
[data-testid="stSlider"]
[data-testid="stSliderTrackFill"] {
    background: #BE365A !important;
}

/* Burgundy Rose circular handle */

section[data-testid="stSidebar"]
[data-testid="stSlider"]
[role="slider"] {
    background: #881337 !important;
    border: 2px solid #BE365A !important;
    box-shadow: 0 0 0 1px #F4C7D4 !important;
}

/* Slider labels and values */

section[data-testid="stSidebar"]
[data-testid="stSlider"] p,
section[data-testid="stSidebar"]
[data-testid="stSlider"] span,
section[data-testid="stSidebar"]
[data-testid="stSlider"]
[data-testid="stTickBar"] {
    color: #FFF4F7 !important;
    -webkit-text-fill-color: #FFF4F7 !important;
}

/* RUN GA BUTTON */

section[data-testid="stSidebar"]
.stButton button[kind="primary"] {
    background: #FFF4F7 !important;
    border: 1px solid #FFF4F7 !important;
    color: #64152D !important;
    border-radius: 11px !important;
    font-weight: 700 !important;
    width: 100% !important;
    min-height: 52px !important;
    font-size: 0.91rem !important;
    margin-top: 0 !important;
}

section[data-testid="stSidebar"]
.stButton button[kind="primary"] p,
section[data-testid="stSidebar"]
.stButton button[kind="primary"] span {
    color: #64152D !important;
    -webkit-text-fill-color: #64152D !important;
}

section[data-testid="stSidebar"]
.stButton button[kind="primary"] svg {
    color: #64152D !important;
    fill: #64152D !important;
}

section[data-testid="stSidebar"]
.stButton button[kind="primary"]:hover {
    background: #FFE5EC !important;
    border-color: #F4C7D4 !important;
}

/* SIDEBAR METRIC */

section[data-testid="stSidebar"]
[data-testid="stMetric"] {
    background: #FFF4F7 !important;
    border: 1px solid #F4C7D4 !important;
    padding: 20px 17px !important;
    border-radius: 12px !important;
    min-height: 110px !important;
}

section[data-testid="stSidebar"]
[data-testid="stMetricLabel"] p,
section[data-testid="stSidebar"]
[data-testid="stMetricValue"],
section[data-testid="stSidebar"]
[data-testid="stMetricValue"] > div {
    color: #64152D !important;
    -webkit-text-fill-color: #64152D !important;
}

section[data-testid="stSidebar"]
[data-testid="stMetricLabel"] {
    margin-bottom: 5px !important;
}

section[data-testid="stSidebar"]
[data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 600 !important;
}

/* INFORMATION BOX */

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
    color: white !important;
    font-size: 16px;
    line-height: 1.5;
}

.burgundy-info p,
.burgundy-info span {
    color: white !important;
    -webkit-text-fill-color: white !important;
    margin: 0 !important;
}

/* DATAFRAME */

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* EXPANDERS */

[data-testid="stExpander"] {
    border: 1px solid #F4D8E0 !important;
    border-radius: 12px !important;
}

/* MAIN PRIMARY BUTTON */

.stButton button[kind="primary"] {
    background: #A7234A;
    border-color: #A7234A;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="hero">'
    '<h1>📺 TV Scheduling Optimizer</h1>'
    '<p>JIE42903 · Evolutionary Computing · Genetic Algorithm</p>'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# LOAD MODIFIED DATASET
# ============================================================

if not MODIFIED.is_file():
    st.error(
        "Missing program_ratings_modified.csv. "
        "Add this file to the same folder as app.py."
    )
    st.stop()

try:
    ratings, hours = load_ratings(MODIFIED)
except Exception as exc:
    st.error(f"Could not load ratings CSV: {exc}")
    st.stop()


# ============================================================
# EXPERIMENT CONFIGURATION
# ============================================================

DEFAULT_CO_R = 0.80
DEFAULT_MUT_R = 0.20

EXPERIMENT_ORDER = [
    "Default",
    "Trial 1",
    "Trial 2",
    "Trial 3"
]

TRIAL_NAMES = [
    "Trial 1",
    "Trial 2",
    "Trial 3"
]

GENERATIONS = 100
POPULATION_SIZE = 50
SEED = 42


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def is_default_parameters(co_r, mut_r):
    return (
        abs(float(co_r) - DEFAULT_CO_R) < 1e-9
        and
        abs(float(mut_r) - DEFAULT_MUT_R) < 1e-9
    )


def get_next_experiment(saved_experiments):
    for name in EXPERIMENT_ORDER:
        if name not in saved_experiments:
            return name
    return None


def get_parameter_table(saved_experiments):
    table_rows = []

    for name in EXPERIMENT_ORDER:

        if name == "Default":
            crossover_rate = DEFAULT_CO_R
            mutation_rate = DEFAULT_MUT_R

        elif name in saved_experiments:
            crossover_rate = saved_experiments[name]["co_r"]
            mutation_rate = saved_experiments[name]["mut_r"]

        else:
            crossover_rate = None
            mutation_rate = None

        table_rows.append({
            "Experiment": name,
            "Crossover Rate (CO_R)": crossover_rate,
            "Mutation Rate (MUT_R)": mutation_rate,
            "Status": (
                "Saved"
                if name in saved_experiments
                else "Not Saved"
            )
        })

    return pd.DataFrame(table_rows)


def build_performance_summary(saved_experiments):
    """
    Default is the baseline only.
    Best trial is selected from Trial 1-3.
    """

    baseline_score = float(
        saved_experiments["Default"]["score"]
    )

    best_trial_score = max(
        float(saved_experiments[name]["score"])
        for name in TRIAL_NAMES
    )

    best_trials = [
        name
        for name in TRIAL_NAMES
        if abs(
            float(saved_experiments[name]["score"])
            - best_trial_score
        ) < 1e-9
    ]

    if len(best_trials) == 1:
        trial_description = (
            f"{best_trials[0]} achieved the highest fitness "
            f"among the experimental trials "
            f"({best_trial_score:.2f})"
        )
    else:
        trial_description = (
            f"{', '.join(best_trials)} achieved the same "
            f"highest fitness among the experimental trials "
            f"({best_trial_score:.2f})"
        )

    if abs(best_trial_score - baseline_score) < 1e-9:
        performance_description = (
            "matching the baseline performance."
        )

    elif best_trial_score < baseline_score:
        difference = baseline_score - best_trial_score
        performance_description = (
            f"which is {difference:.2f} below "
            "the baseline fitness."
        )

    else:
        difference = best_trial_score - baseline_score
        performance_description = (
            f"which is {difference:.2f} above "
            "the baseline fitness."
        )

    return (
        "All four experiments completed. "
        f"The Default configuration achieved a baseline "
        f"fitness of {baseline_score:.2f}. "
        f"{trial_description}, {performance_description}"
    )


# ============================================================
# SESSION STATE
# ============================================================

if "experiments" not in st.session_state:
    st.session_state.experiments = {}

if "current" not in st.session_state:
    st.session_state.current = None

if "co_r_input" not in st.session_state:
    st.session_state.co_r_input = DEFAULT_CO_R

if "mut_r_input" not in st.session_state:
    st.session_state.mut_r_input = DEFAULT_MUT_R

if "run_counter" not in st.session_state:
    st.session_state.run_counter = 0


# ============================================================
# SESSION STATE COMPATIBILITY
# ============================================================

if st.session_state.current is not None:

    if isinstance(st.session_state.current, dict):

        st.session_state.current.setdefault(
            "experiment", None
        )

        st.session_state.current.setdefault(
            "generations", GENERATIONS
        )

        st.session_state.current.setdefault(
            "population_size", POPULATION_SIZE
        )

        st.session_state.current.setdefault(
            "seed", SEED
        )

        st.session_state.current.setdefault(
            "run_id", None
        )

    else:
        st.session_state.current = None


# ============================================================
# SIDEBAR - GA CONTROL PANEL
# ============================================================

with st.sidebar:

    st.header("GA Control Panel")

    # --------------------------------------------------------
    # CROSSOVER RATE SLIDER
    # --------------------------------------------------------

    co_r = st.slider(
        "Crossover Rate (CO_R)",
        min_value=0.00,
        max_value=0.95,
        step=0.01,
        key="co_r_input",
        format="%.2f"
    )

    # --------------------------------------------------------
    # MUTATION RATE SLIDER
    # --------------------------------------------------------

    mut_r = st.slider(
        "Mutation Rate (MUT_R)",
        min_value=0.00,
        max_value=1.00,
        step=0.01,
        key="mut_r_input",
        format="%.2f",
        help=(
            "Default MUT_R is 0.20. "
            "For Trial 1-3, the assignment specifies "
            "mutation rates between 0.01 and 0.05."
        )
    )

    # --------------------------------------------------------
    # RUN GA BUTTON
    # --------------------------------------------------------

    run = st.button(
        "Run Genetic Algorithm",
        icon=":material/play_arrow:",
        type="primary",
        width="stretch"
    )

    # --------------------------------------------------------
    # SAVED EXPERIMENTS
    # --------------------------------------------------------

    st.metric(
        "Saved Experiments",
        f"{len(st.session_state.experiments)} / 4"
    )


# ============================================================
# RUN GENETIC ALGORITHM
# ============================================================

if run:

    try:

        with st.spinner("Optimizing schedule..."):

            rows, score, upper, history = run_ga(
                ratings,
                hours,
                crossover_rate=co_r,
                mutation_rate=mut_r,
                generations=GENERATIONS,
                population_size=POPULATION_SIZE,
                seed=SEED
            )

        st.session_state.run_counter += 1

        st.session_state.current = {
            "experiment": None,
            "rows": rows,
            "score": score,
            "upper": upper,
            "history": history,
            "co_r": co_r,
            "mut_r": mut_r,
            "generations": GENERATIONS,
            "population_size": POPULATION_SIZE,
            "seed": SEED,
            "run_id": st.session_state.run_counter
        }

        st.success(
            "Schedule generated successfully."
        )

    except Exception as exc:
        st.error(f"GA execution failed: {exc}")


# ============================================================
# MAIN METRICS
# ============================================================

current = st.session_state.current

if current is not None:

    a, b, c = st.columns(3)

    a.metric(
        "Best Fitness",
        f"{current['score']:.2f}"
    )

    b.metric(
        "Upper Bound",
        f"{current['upper']:.2f}"
    )

    c.metric(
        "Fitness / Upper Bound",
        (
            f"{100 * current['score'] / current['upper']:.1f}%"
            if current["upper"]
            else "N/A"
        )
    )

else:

    a, b, c = st.columns(3)

    a.metric("Time Slots", len(hours))

    b.metric("Program Categories", len(ratings))

    c.metric(
        "Saved Experiments",
        f"{len(st.session_state.experiments)} / 4"
    )


# ============================================================
# MAIN TABS
# ============================================================

scheduler, comparison, changes = st.tabs([
    "GA Scheduler",
    "Trial Comparison",
    "Rating Changes"
])


# ============================================================
# TAB 1 - GA SCHEDULER
# ============================================================

with scheduler:

    st.subheader("Generated TV Schedule")

    if current is None:

        st.markdown(
            '<div class="burgundy-info">'
            'Start with Default (CO_R=0.80, MUT_R=0.20). '
            'Then choose your own crossover and mutation '
            'rates for Trial 1, Trial 2 and Trial 3.'
            '</div>',
            unsafe_allow_html=True
        )

    else:

        # ====================================================
        # CURRENT PARAMETERS
        # ====================================================

        if is_default_parameters(
            current["co_r"],
            current["mut_r"]
        ):
            parameter_type = "Default Parameters"
        else:
            parameter_type = "Custom Parameters"

        st.caption(
            f"Parameter Type={parameter_type} · "
            f"CO_R={current['co_r']:.2f} · "
            f"MUT_R={current['mut_r']:.2f} · "
            f"Generations={current['generations']} · "
            f"Population={current['population_size']} · "
            f"Seed={current['seed']}"
        )

        # ====================================================
        # GENERATED SCHEDULE
        # ====================================================

        schedule_df = pd.DataFrame(
            current["rows"]
        )

        st.dataframe(
            schedule_df,
            width="stretch",
            hide_index=True
        )

        # ====================================================
        # FITNESS CONVERGENCE
        # ====================================================

        st.subheader("Fitness Convergence")

        history_df = pd.DataFrame(
            current["history"]
        )

        if (
            not history_df.empty
            and "Generation" in history_df.columns
        ):

            st.line_chart(
                history_df.set_index("Generation"),
                width="stretch"
            )

        else:

            st.info(
                "Fitness convergence history "
                "is not available."
            )

        # ====================================================
        # DOWNLOAD AND SAVE BUTTONS
        # ====================================================

        left, right = st.columns(2)

        with left:

            st.download_button(
                "⬇ Download Schedule CSV",
                data=schedule_df.to_csv(index=False),
                file_name="generated_schedule.csv",
                mime="text/csv",
                width="stretch"
            )

        with right:

            save_clicked = st.button(
                "💾 Save Experiment",
                width="stretch"
            )

        # ====================================================
        # AUTOMATIC EXPERIMENT SAVING
        # ====================================================

        if save_clicked:

            saved_experiments = (
                st.session_state.experiments
            )

            next_experiment = get_next_experiment(
                saved_experiments
            )

            # Check sidebar parameters against
            # the generated schedule.

            parameters_match = (
                abs(
                    float(current["co_r"])
                    - float(co_r)
                ) < 1e-9
                and
                abs(
                    float(current["mut_r"])
                    - float(mut_r)
                ) < 1e-9
            )

            # Prevent saving the same GA run twice.

            run_id = current.get("run_id")

            already_saved = (
                run_id is not None
                and any(
                    experiment.get("run_id") == run_id
                    for experiment
                    in saved_experiments.values()
                )
            )

            # Prevent duplicate parameter combinations.

            duplicate_parameters = any(
                (
                    abs(
                        float(experiment["co_r"])
                        - float(current["co_r"])
                    ) < 1e-9
                )
                and
                (
                    abs(
                        float(experiment["mut_r"])
                        - float(current["mut_r"])
                    ) < 1e-9
                )
                for experiment
                in saved_experiments.values()
            )

            if next_experiment is None:

                st.warning(
                    "All four experiments have already "
                    "been saved. Open Trial Comparison "
                    "to view the results."
                )

            elif not parameters_match:

                st.warning(
                    "The sidebar parameters have changed "
                    "since the current schedule was generated. "
                    "Please click Run Genetic Algorithm "
                    "again before saving."
                )

            elif already_saved:

                st.warning(
                    "This GA run has already been saved. "
                    "Change the parameters and run the "
                    "Genetic Algorithm again for "
                    "the next trial."
                )

            elif (
                next_experiment == "Default"
                and not is_default_parameters(
                    current["co_r"],
                    current["mut_r"]
                )
            ):

                st.warning(
                    "Default must use CO_R=0.80 "
                    "and MUT_R=0.20. "
                    "Please run the Genetic Algorithm "
                    "using these parameters first."
                )

            elif (
                next_experiment != "Default"
                and is_default_parameters(
                    current["co_r"],
                    current["mut_r"]
                )
            ):

                st.warning(
                    "Default has already been saved. "
                    "Please change CO_R or MUT_R "
                    "and run the GA again for "
                    "the next trial."
                )

            elif duplicate_parameters:

                st.warning(
                    "These crossover and mutation rates "
                    "have already been used in a saved "
                    "experiment. Please choose a different "
                    "parameter combination."
                )

            else:

                st.session_state.experiments[
                    next_experiment
                ] = {
                    **current,
                    "experiment": next_experiment
                }

                st.rerun()

    # ========================================================
    # EXPERIMENT PARAMETERS
    # ========================================================

    st.subheader("Experiment Parameters")

    parameter_df = get_parameter_table(
        st.session_state.experiments
    )

    st.dataframe(
        parameter_df,
        width="stretch",
        hide_index=True,
        column_config={
            "Crossover Rate (CO_R)":
                st.column_config.NumberColumn(
                    format="%.2f"
                ),
            "Mutation Rate (MUT_R)":
                st.column_config.NumberColumn(
                    format="%.2f"
                )
        }
    )

    st.caption(
        "Default uses fixed parameters (0.80, 0.20). "
        "Trial 1, Trial 2 and Trial 3 use parameters "
        "selected by the user. "
        "All experiments use the modified CSV dataset, "
        "100 generations, population size 50 "
        "and random seed 42."
    )


# ============================================================
# TAB 2 - TRIAL COMPARISON
# ============================================================

with comparison:

    st.subheader(
        "Default and Three-Trial Experiment Comparison"
    )

    saved_experiments = st.session_state.experiments

    if not saved_experiments:

        st.markdown(
            '<div class="burgundy-info">'
            'Run and save the Default experiment first. '
            'Then generate and save Trial 1, Trial 2 '
            'and Trial 3 using your own parameters.'
            '</div>',
            unsafe_allow_html=True
        )

    else:

        st.caption(
            f"{len(saved_experiments)} "
            "of 4 experiments saved."
        )

        # ====================================================
        # EXPERIMENT RESULTS SUMMARY
        # ====================================================

        comparison_rows = []

        for name in EXPERIMENT_ORDER:

            if name not in saved_experiments:
                continue

            experiment = saved_experiments[name]

            comparison_rows.append({
                "Experiment": name,
                "Crossover Rate (CO_R)":
                    experiment["co_r"],
                "Mutation Rate (MUT_R)":
                    experiment["mut_r"],
                "Generations":
                    experiment["generations"],
                "Population Size":
                    experiment["population_size"],
                "Random Seed":
                    experiment["seed"],
                "Best Fitness":
                    experiment["score"],
                "Upper Bound":
                    experiment["upper"],
                "Fitness (%)": (
                    100
                    * experiment["score"]
                    / experiment["upper"]
                    if experiment["upper"]
                    else 0
                )
            })

        comparison_df = pd.DataFrame(
            comparison_rows
        )

        st.subheader("Experiment Results Summary")

        st.dataframe(
            comparison_df,
            width="stretch",
            hide_index=True,
            column_config={
                "Crossover Rate (CO_R)":
                    st.column_config.NumberColumn(
                        format="%.2f"
                    ),
                "Mutation Rate (MUT_R)":
                    st.column_config.NumberColumn(
                        format="%.2f"
                    ),
                "Best Fitness":
                    st.column_config.NumberColumn(
                        format="%.2f"
                    ),
                "Upper Bound":
                    st.column_config.NumberColumn(
                        format="%.2f"
                    ),
                "Fitness (%)":
                    st.column_config.NumberColumn(
                        format="%.1f%%"
                    )
            }
        )

        # ====================================================
        # FITNESS COMPARISON
        # ====================================================

        st.subheader("Fitness Comparison")

        fitness_df = comparison_df[
            ["Experiment", "Best Fitness"]
        ].set_index("Experiment")

        st.bar_chart(
            fitness_df,
            width="stretch",
            color="#A7234A"
        )

        # ====================================================
        # FITNESS CONVERGENCE COMPARISON
        # ====================================================

        st.subheader(
            "Fitness Convergence Comparison"
        )

        convergence_frames = []

        for name in EXPERIMENT_ORDER:

            if name not in saved_experiments:
                continue

            experiment = saved_experiments[name]

            trial_history = pd.DataFrame(
                experiment["history"]
            ).copy()

            if "Generation" not in trial_history.columns:
                continue

            fitness_columns = [
                col
                for col in trial_history.columns
                if (
                    col != "Generation"
                    and pd.api.types.is_numeric_dtype(
                        trial_history[col]
                    )
                )
            ]

            if fitness_columns:

                fitness_column = fitness_columns[0]

                trial_history = trial_history[
                    ["Generation", fitness_column]
                ].rename(
                    columns={
                        fitness_column: name
                    }
                )

                trial_history = trial_history.set_index(
                    "Generation"
                )

                convergence_frames.append(
                    trial_history
                )

        if convergence_frames:

            convergence_df = pd.concat(
                convergence_frames,
                axis=1
            )

            st.line_chart(
                convergence_df,
                width="stretch"
            )

        else:

            st.info(
                "Fitness convergence history is "
                "not available for saved experiments."
            )

        # ====================================================
        # GENERATED SCHEDULE FOR EACH EXPERIMENT
        # ====================================================

        st.subheader(
            "Generated Schedule for Each Experiment"
        )

        for name in EXPERIMENT_ORDER:

            if name not in saved_experiments:
                continue

            experiment = saved_experiments[name]

            with st.expander(
                f"{name} - Generated TV Schedule"
            ):

                st.caption(
                    f"CO_R={experiment['co_r']:.2f} · "
                    f"MUT_R={experiment['mut_r']:.2f} · "
                    f"Generations={experiment['generations']} · "
                    f"Population={experiment['population_size']} · "
                    f"Seed={experiment['seed']}"
                )

                st.metric(
                    "Best Fitness",
                    f"{experiment['score']:.2f}"
                )

                experiment_schedule_df = pd.DataFrame(
                    experiment["rows"]
                )

                st.dataframe(
                    experiment_schedule_df,
                    width="stretch",
                    hide_index=True
                )

                st.download_button(
                    f"⬇ Download {name} Schedule",
                    data=experiment_schedule_df.to_csv(
                        index=False
                    ),
                    file_name=(
                        name.lower().replace(" ", "_")
                        + "_schedule.csv"
                    ),
                    mime="text/csv",
                    width="stretch",
                    key=(
                        f"download_"
                        f"{name.replace(' ', '_')}"
                    )
                )

        # ====================================================
        # EXPERIMENT PERFORMANCE SUMMARY
        # ====================================================

        if all(
            name in saved_experiments
            for name in EXPERIMENT_ORDER
        ):

            result_message = build_performance_summary(
                saved_experiments
            )

            st.markdown(
                '<div class="burgundy-info">'
                + escape(result_message)
                + '</div>',
                unsafe_allow_html=True
            )

        # ====================================================
        # CLEAR SAVED EXPERIMENTS
        # ====================================================

        if st.button(
            "Clear Saved Experiments",
            width="stretch"
        ):

            st.session_state.experiments = {}

            st.rerun()


# ============================================================
# TAB 3 - RATING CHANGES
# ============================================================

with changes:

    st.subheader("Rating Changes")

    if not ORIGINAL.is_file():

        st.markdown(
            '<div class="burgundy-info">'
            'Original ratings CSV is not available. '
            'Add program_ratings_original.csv '
            'to compare rating changes.'
            '</div>',
            unsafe_allow_html=True
        )

    else:

        try:

            original_df = pd.read_csv(
                ORIGINAL
            )

            modified_df = pd.read_csv(
                MODIFIED
            )

            # =================================================
            # VALIDATE DATASET STRUCTURE
            # =================================================

            same_structure = (
                original_df.columns.tolist()
                == modified_df.columns.tolist()
                and len(original_df) == len(modified_df)
            )

            if same_structure:

                program_column = original_df.columns[0]

                hour_columns = [
                    col
                    for col in original_df.columns
                    if str(col).strip().lower().startswith(
                        "hour"
                    )
                ]

                if not hour_columns:

                    st.warning(
                        "No hourly rating columns were found."
                    )

                else:

                    same_program_order = (
                        original_df[program_column]
                        .reset_index(drop=True)
                        .equals(
                            modified_df[program_column]
                            .reset_index(drop=True)
                        )
                    )

                    if not same_program_order:

                        st.warning(
                            "Program order differs between "
                            "the original and modified CSV files."
                        )

                    else:

                        # =====================================
                        # FIND MODIFIED RATINGS
                        # =====================================

                        rating_changes = []
                        changed_row_indices = set()

                        for row_index in range(
                            len(original_df)
                        ):

                            program_name = original_df.iloc[
                                row_index
                            ][program_column]

                            for hour in hour_columns:

                                original_rate = original_df.at[
                                    row_index,
                                    hour
                                ]

                                modified_rate = modified_df.at[
                                    row_index,
                                    hour
                                ]

                                both_missing = (
                                    pd.isna(original_rate)
                                    and pd.isna(modified_rate)
                                )

                                if both_missing:
                                    continue

                                if (
                                    pd.isna(original_rate)
                                    or pd.isna(modified_rate)
                                ):
                                    is_changed = True
                                else:
                                    is_changed = (
                                        original_rate
                                        != modified_rate
                                    )

                                if is_changed:

                                    changed_row_indices.add(
                                        row_index
                                    )

                                    rating_changes.append({
                                        "Type of Program":
                                            program_name,
                                        "Hour":
                                            hour,
                                        "Original Rates":
                                            original_rate,
                                        "Modified Rates":
                                            modified_rate
                                    })

                        changes_df = pd.DataFrame(
                            rating_changes,
                            columns=[
                                "Type of Program",
                                "Hour",
                                "Original Rates",
                                "Modified Rates"
                            ]
                        )

                        # =====================================
                        # 1. SUMMARY METRICS
                        # =====================================

                        summary_left, summary_right = (
                            st.columns(2)
                        )

                        with summary_left:

                            st.metric(
                                "Total Records",
                                len(modified_df)
                            )

                        with summary_right:

                            st.metric(
                                "Rows with Changes",
                                len(changed_row_indices)
                            )

                        # =====================================
                        # 2. RATING CHANGES COMPARISON
                        # =====================================

                        st.subheader(
                            "Rating Changes Comparison"
                        )

                        if changes_df.empty:

                            st.markdown(
                                '<div class="burgundy-info">'
                                'No rating changes were detected '
                                'between the original and modified '
                                'datasets.'
                                '</div>',
                                unsafe_allow_html=True
                            )

                        else:

                            st.dataframe(
                                changes_df,
                                width="stretch",
                                hide_index=True,
                                column_config={
                                    "Type of Program":
                                        st.column_config.TextColumn(
                                            "Type of Program"
                                        ),
                                    "Hour":
                                        st.column_config.TextColumn(
                                            "Hour"
                                        ),
                                    "Original Rates":
                                        st.column_config.NumberColumn(
                                            "Original Rates",
                                            format="%.2f"
                                        ),
                                    "Modified Rates":
                                        st.column_config.NumberColumn(
                                            "Modified Rates",
                                            format="%.2f"
                                        )
                                }
                            )

                            st.caption(
                                "Only modified ratings are shown. "
                                "Each row represents a program "
                                "and hour with a changed rating."
                            )

                        # =====================================
                        # 3. ORIGINAL PROGRAM RATINGS
                        # =====================================

                        st.subheader(
                            "Original Program Ratings"
                        )

                        st.dataframe(
                            original_df,
                            width="stretch",
                            hide_index=True
                        )

                        # =====================================
                        # 4. MODIFIED PROGRAM RATINGS
                        # =====================================

                        st.subheader(
                            "Modified Program Ratings"
                        )

                        st.dataframe(
                            modified_df,
                            width="stretch",
                            hide_index=True
                        )

            else:

                st.warning(
                    "Original and modified CSV files have "
                    "different columns or row counts."
                )

                st.subheader(
                    "Original Program Ratings"
                )

                st.dataframe(
                    original_df,
                    width="stretch",
                    hide_index=True
                )

                st.subheader(
                    "Modified Program Ratings"
                )

                st.dataframe(
                    modified_df,
                    width="stretch",
                    hide_index=True
                )

        except Exception as exc:

            st.error(
                f"Could not compare rating CSV files: {exc}"
            )
