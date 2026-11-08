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
</style>
""", unsafe_allow_html=True)

if not MODIFIED.exists():
    st.error("Missing program_ratings_modified.csv in the GitHub repository.")
    st.stop()

try:
    ratings, hours = load_ratings(MODIFIED)
except Exception as exc:
    st.error(f"Could not load modified ratings: {exc}")
    st.stop()

if "trials" not in st.session_state:
    st.session_state.trials = []

with st.sidebar:
    st.markdown("### GA Control Panel")
    co_r = st.slider("Crossover Rate (CO_R)", min_value=0.0, max_value=0.95, value=0.80, step=0.01)
    mut_r = st.number_input("Mutation Rate (MUT_R)", min_value=0.0, max_value=1.0, value=0.20, step=0.01, format="%.2f")
    st.divider()
    generations = st.number_input("Generations", min_value=1, max_value=2000, value=100, step=1)
    population_size = st.number_input("Population Size", min_value=4, max_value=1000, value=50, step=1)
    seed = st.number_input("Random Seed", min_value=0, max_value=1000000, value=42, step=1)
    run = st.button("▶ Run Genetic Algorithm", type="primary", use_container_width=True)
    st.divider()
    st.metric("Saved Trials", len(st.session_state.trials))

st.markdown("""
<div class="hero">
  <div class="eyebrow">JIE42903 · EVOLUTIONARY COMPUTING</div>
  <h1>📺 TV Scheduling Optimizer</h1>
  <p>Intelligent Program Scheduling with Genetic Algorithm</p>
</div>
""", unsafe_allow_html=True)

if run:
    try:
        with st.spinner("Optimizing the TV schedule..."):
            rows, score, upper, history = run_ga(
                ratings, hours, co_r, mut_r,
                int(generations), int(population_size), seed=int(seed)
            )
        st.session_state.current = {
            "rows": rows,
            "score": float(score),
            "upper": float(upper),
            "history": history,
            "co_r": float(co_r),
            "mut_r": float(mut_r),
            "seed": int(seed),
            "generations": int(generations),
            "population_size": int(population_size),
        }
        st.success("Schedule generated successfully!")
    except Exception as exc:
        st.error(f"The GA could not run: {exc}")

current = st.session_state.get("current")
if current is not None:
    a, b, c, d = st.columns(4)
    a.metric("Best Fitness", f"{current['score']:.2f}")

    b.metric("Upper Bound", f"{current['upper']:.2f}")
    c.metric(
        "Fitness / Upper Bound",
        f"{100 * current['score'] / current['upper']:.1f}%"
        if current["upper"] else "N/A"
    )
    d.metric("Saved Trials", len(st.session_state.trials))
else:
    a, b, c = st.columns(3)
    a.metric("Time Slots", len(hours))
    b.metric("Program Categories", len(ratings))
    c.metric("Saved Trials", len(st.session_state.trials))


# ==================================================
# THREE MAIN TABS
# ==================================================

scheduler, comparison, changes = st.tabs([
    "GA Scheduler",
    "Trial Comparison",
    "Rating Changes"
])


# ==================================================
# TAB 1: GA SCHEDULER
# ==================================================

with scheduler:
    st.subheader("Generated TV Schedule")

    if current is None:
        st.info(
            "Configure the GA parameters in the sidebar "
            "and click Run Genetic Algorithm."
        )
    else:
        st.caption(
            f"CO_R = {current['co_r']:.2f} | "
            f"MUT_R = {current['mut_r']:.2f} | "
            f"Generations = {current['generations']} | "
            f"Population = {current['population_size']} | "
            f"Seed = {current['seed']}"
        )

        schedule_df = pd.DataFrame(current["rows"])

        st.dataframe(
            schedule_df,
            use_container_width=True,
            hide_index=True,
            height=650
        )

        st.subheader("Fitness Convergence")

        history_df = pd.DataFrame(current["history"])

        st.line_chart(
            history_df.set_index("Generation"),
            use_container_width=True
        )

        left, right = st.columns(2)

        with left:
            st.download_button(
                "⬇ Download Schedule CSV",
                data=schedule_df.to_csv(index=False),
                file_name="generated_schedule.csv",
                mime="text/csv",
                use_container_width=True
            )

        with right:
            if st.button(
                "💾 Save Trial for Comparison",
                use_container_width=True
            ):
                if len(st.session_state.trials) >= 3:
                    st.warning(
                        "Three trials have already been saved."
                    )
                else:
                    number = len(st.session_state.trials) + 1

                    st.session_state.trials.append({
                        **current,
                        "trial": number
                    })

                    st.toast(
                        f"Trial {number} saved successfully!",
                        icon="✅"
                    )

                    st.rerun()


# ==================================================
# TAB 2: TRIAL COMPARISON
# ==================================================

with comparison:
    st.subheader("Three-Trial Experiment Comparison")

    trials = st.session_state.trials

    if not trials:
        st.info(
            "No trials saved yet. Generate a schedule "
            "and save it from the GA Scheduler tab."
        )

    else:
        records = []

        for trial in trials:
            records.append({
                "Trial": trial["trial"],
                "CO_R": trial["co_r"],
                "MUT_R": trial["mut_r"],
                "Generations": trial["generations"],
                "Population": trial["population_size"],
                "Seed": trial["seed"],
                "Fitness": round(trial["score"], 4),
                "Fitness / Upper Bound (%)": (
                    round(
                        100 * trial["score"] / trial["upper"],
                        2
                    )
                    if trial["upper"] else None
                )
            })

        summary = pd.DataFrame(records)

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Fitness Comparison")

        st.bar_chart(
            summary.set_index("Trial")[["Fitness"]],
            use_container_width=True
        )

        best = max(
            trials,
            key=lambda trial: trial["score"]
        )

        st.success(
            f"Highest observed fitness: Trial {best['trial']} "
            f"({best['score']:.2f}) | "
            f"CO_R = {best['co_r']:.2f} | "
            f"MUT_R = {best['mut_r']:.2f}"
        )

        st.download_button(
            "⬇ Download Trial Comparison CSV",
            data=summary.to_csv(index=False),
            file_name="trial_comparison.csv",
            mime="text/csv"
        )

        st.subheader("Full Schedule for Each Trial")

        for trial in trials:
            with st.expander(
                f"Trial {trial['trial']} | "
                f"Fitness = {trial['score']:.2f}"
            ):
                trial_df = pd.DataFrame(trial["rows"])

                st.dataframe(
                    trial_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.download_button(
                    f"⬇ Download Trial {trial['trial']} CSV",
                    data=trial_df.to_csv(index=False),
                    file_name=f"trial_{trial['trial']}.csv",
                    mime="text/csv",
                    key=f"download_{trial['trial']}"
                )

        if st.button("🗑 Clear Saved Trials"):
            st.session_state.trials = []
            st.rerun()


# ==================================================
# TAB 3: RATING CHANGES
# ==================================================

with changes:
    st.subheader("CSV Rating Modifications")

    modified = pd.read_csv(MODIFIED)

    if ORIGINAL.exists():
        original = pd.read_csv(ORIGINAL)

        old = original.set_index("Type of Program")
        new = modified.set_index("Type of Program")

        changed = []

        for program in new.index:
            for column in new.columns:
                original_value = float(
                    old.loc[program, column]
                )

                modified_value = float(
                    new.loc[program, column]
                )

                if original_value != modified_value:
                    changed.append({
                        "Program": program,
                        "Time": column.replace("Hour ", "") + ":00",
                        "Original Rating": original_value,
                        "Modified Rating": modified_value,
                        "Difference": round(
                            modified_value - original_value,
                            3
                        )
                    })

        st.metric(
            "Changed Rating Values",
            len(changed)
        )

        if changed:
            st.dataframe(
                pd.DataFrame(changed),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info(
                "No rating differences were detected."
            )

    else:
        st.warning(
            "Original CSV not found. "
            "Upload program_ratings_original.csv."
        )

    with st.expander("View Full Modified Dataset"):
        st.dataframe(
            modified,
            use_container_width=True,
            hide_index=True
        )
