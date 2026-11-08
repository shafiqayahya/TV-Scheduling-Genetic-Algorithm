
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

from ga_engine import (
    load_ratings,
    genetic_algorithm,
    create_schedule,
    calculate_upper_bound,
)

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="TV Scheduling Optimizer",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# ROSE & BURGUNDY DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #FFF8FA;
    color: #491528;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

.hero {
    background: linear-gradient(120deg, #65112E, #9F3659);
    padding: 34px;
    border-radius: 20px;
    color: white;
    margin-bottom: 24px;
}

.hero h1 {
    color: white;
    font-size: 2.5rem;
    margin-bottom: 10px;
}

.hero p {
    color: #FFE5ED;
    font-size: 1rem;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #F0CED9;
    box-shadow: 0 3px 12px rgba(101,17,46,0.06);
    margin-bottom: 12px;
}

.metric-label {
    color: #94526B;
    font-size: 0.9rem;
}

.metric-value {
    color: #65112E;
    font-size: 1.8rem;
    font-weight: 750;
}

.section-heading {
    color: #65112E;
    font-size: 1.35rem;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 12px;
}

.stButton > button[kind="primary"] {
    background: #9F3659;
    border: 1px solid #9F3659;
    color: white;
    border-radius: 10px;
    font-weight: 650;
}

.stButton > button[kind="primary"]:hover {
    background: #65112E;
    border-color: #65112E;
    color: white;
}

div[data-testid="stTabs"] button {
    font-weight: 600;
}

div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# DATA LOADING
# ==========================================

@st.cache_data
def get_data():
    return load_ratings("program_ratings_modified.csv")


try:
    programs, hours, ratings = get_data()
except Exception as error:
    st.error(f"Unable to load modified CSV: {error}")
    st.stop()

upper_bound = calculate_upper_bound(ratings)

if "trials" not in st.session_state:
    st.session_state.trials = []

if "current_result" not in st.session_state:
    st.session_state.current_result = None


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_schedule(schedule):
    st.dataframe(
        schedule,
        use_container_width=True,
        hide_index=True,
    )


def show_result(result):
    fitness = result["fitness"]
    efficiency = (
        fitness / upper_bound * 100
        if upper_bound > 0 else 0
    )

    a, b, c = st.columns(3)

    with a:
        metric_card("Best Fitness", f"{fitness:.2f}")

    with b:
        metric_card("Upper Bound", f"{upper_bound:.2f}")

    with c:
        metric_card("Upper Bound Achieved", f"{efficiency:.1f}%")

    st.markdown(
        '<div class="section-heading">Generated TV Schedule</div>',
        unsafe_allow_html=True,
    )

    show_schedule(result["schedule"])

    st.download_button(
        "📥 Download Schedule CSV",
        data=result["schedule"].to_csv(index=False),
        file_name="tv_schedule.csv",
        mime="text/csv",
        key="download_current",
    )

    st.markdown(
        '<div class="section-heading">Fitness Convergence</div>',
        unsafe_allow_html=True,
    )

    history = pd.DataFrame({
        "Generation": range(len(result["history"])),
        "Best Fitness": result["history"],
    })

    st.line_chart(
        history.set_index("Generation"),
        color="#A33B5D",
    )


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.title("⚙️ GA Configuration")

    st.caption("Configure the genetic algorithm.")

    co_r = st.slider(
        "Crossover Rate (CO_R)",
        min_value=0.0,
        max_value=0.95,
        value=0.80,
        step=0.01,
    )

    mut_r = st.number_input(
        "Mutation Rate (MUT_R)",
        min_value=0.0,
        max_value=1.0,
        value=0.20,
        step=0.01,
        format="%.2f",
    )

    if not 0.01 <= mut_r <= 0.05:
        st.warning(
            "The assignment specifies default MUT_R = 0.20, "
            "but an experimental range of 0.01–0.05. "
            "Please confirm this inconsistency with the lecturer."
        )

    st.markdown("#### Experimental Settings")

    pop_size = st.number_input(
        "Population Size",
        min_value=2,
        max_value=500,
        value=50,
        step=10,
    )

    generations = st.number_input(
        "Generations",
        min_value=1,
        max_value=2000,
        value=100,
        step=10,
    )

    seed = st.number_input(
        "Random Seed",
        min_value=0,
        value=42,
        step=1,
    )

    run_ga = st.button(
        "▶ Run Genetic Algorithm",
        type="primary",
        use_container_width=True,
    )

    st.divider()

    st.caption(
        "JIE42903 | Evolutionary Computing"
    )


# ==========================================
# RUN GENETIC ALGORITHM
# ==========================================

if run_ga:
    with st.spinner("Optimizing TV schedule..."):
        chromosome, fitness, history = genetic_algorithm(
            ratings=ratings,
            pop_size=int(pop_size),
            generations=int(generations),
            crossover_rate=float(co_r),
            mutation_rate=float(mut_r),
            seed=int(seed),
        )

        schedule = create_schedule(
            chromosome, programs, hours, ratings
        )

        st.session_state.current_result = {
            "co_r": float(co_r),
            "mut_r": float(mut_r),
            "pop_size": int(pop_size),
            "generations": int(generations),
            "seed": int(seed),
            "fitness": fitness,
            "history": history,
            "schedule": schedule,
        }

    st.success("Genetic Algorithm completed successfully!")


# ==========================================
# HERO BANNER
# ==========================================

st.markdown("""
<div class="hero">
    <div style="font-size:12px; letter-spacing:2px;">
        JIE42903 · EVOLUTIONARY COMPUTING
    </div>
    <h1>📺 TV Scheduling Optimizer</h1>
    <p>
        Intelligent Program Scheduling using Genetic Algorithm
    </p>
    <div style="margin-top:18px; font-size:13px;">
        Genetic Optimization · Interactive Parameters ·
        Experimental Analysis
    </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# FIVE MAIN TABS
# ==========================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Overview",
    "🧬 GA Scheduler",
    "📊 Trial Comparison",
    "📁 Rating Changes",
    "📖 Methodology",
])


# ==========================================
# TAB 1: OVERVIEW
# ==========================================

with tab1:
    st.markdown("### Project Overview")

    st.write(
        "This application uses a Genetic Algorithm "
        "to generate TV program schedules based on "
        "program rating data."
    )

    a, b, c = st.columns(3)

    with a:
        metric_card("Available Programs", len(programs))

    with b:
        metric_card("Scheduling Time Slots", len(hours))

    with c:
        metric_card("Rating Upper Bound", f"{upper_bound:.2f}")

    st.markdown("### How to Use")

    st.markdown("""
    1. Configure the GA parameters in the sidebar.
    2. Open the **GA Scheduler** tab.
    3. Click **Run Genetic Algorithm**.
    4. Review the schedule and fitness score.
    5. Save the trial for comparison.
    6. Repeat with different CO_R and MUT_R values.
    7. Compare the three trials.
    """)

    st.info(
        "The objective is to maximize the total "
        "program rating across the scheduling slots."
    )

    if st.session_state.current_result is not None:
        st.markdown("### Latest Optimization")

        result = st.session_state.current_result

        a, b = st.columns(2)

        with a:
            metric_card(
                "Latest Fitness",
                f"{result['fitness']:.2f}"
            )

        with b:
            metric_card(
                "Saved Trials",
                len(st.session_state.trials)
            )


# ==========================================
# TAB 2: GA SCHEDULER
# ==========================================

with tab2:
    st.markdown("### Genetic Algorithm Scheduler")

    st.write(
        "Adjust the parameters in the sidebar "
        "and run the Genetic Algorithm."
    )

    result = st.session_state.current_result

    if result is None:
        st.info(
            "No schedule generated yet. "
            "Click Run Genetic Algorithm in the sidebar."
        )
    else:
        st.caption(
            f"CO_R = {result['co_r']:.2f} | "
            f"MUT_R = {result['mut_r']:.2f} | "
            f"Population = {result['pop_size']} | "
            f"Generations = {result['generations']} | "
            f"Seed = {result['seed']}"
        )

        show_result(result)

        st.markdown("### Save Experiment")

        if len(st.session_state.trials) < 3:
            if st.button(
                "💾 Save This Trial for Comparison",
                type="primary",
            ):
                trial = result.copy()
                trial["trial_name"] = (
                    f"Trial {len(st.session_state.trials) + 1}"
                )

                st.session_state.trials.append(trial)

                st.success(
                    f"{trial['trial_name']} saved successfully."
                )
        else:
            st.warning(
                "Three trials have already been saved. "
                "Clear saved trials to start a new comparison."
            )


# ==========================================
# TAB 3: TRIAL COMPARISON
# ==========================================

with tab3:
    st.markdown("### Experimental Trial Comparison")

    trials = st.session_state.trials

    st.write(
        f"Saved trials: {len(trials)} / 3"
    )

    if len(trials) == 0:
        st.info(
            "Run the GA and save your first trial."
        )

    else:
        summary = []

        for trial in trials:
            efficiency = (
                trial["fitness"] / upper_bound * 100
                if upper_bound > 0 else 0
            )

            summary.append({
                "Trial": trial["trial_name"],
                "CO_R": trial["co_r"],
                "MUT_R": trial["mut_r"],
                "Population": trial["pop_size"],
                "Generations": trial["generations"],
                "Seed": trial["seed"],
                "Fitness": trial["fitness"],
                "Upper Bound Achieved (%)": round(
                    efficiency, 2
                ),
            })

        comparison_df = pd.DataFrame(summary)

        st.markdown("#### Parameter and Fitness Summary")

        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "📥 Download Trial Comparison",
            data=comparison_df.to_csv(index=False),
            file_name="ga_trial_comparison.csv",
            mime="text/csv",
        )

        st.markdown("#### Fitness Comparison")

        st.bar_chart(
            comparison_df.set_index("Trial")[["Fitness"]],
            color="#A33B5D",
        )

        best_trial = max(
            trials,
            key=lambda trial: trial["fitness"]
        )

        st.success(
            f"Highest observed fitness: "
            f"{best_trial['trial_name']} "
            f"({best_trial['fitness']:.2f})"
        )

        st.caption(
            "The highest fitness identifies the best "
            "observed schedule among the saved trials, "
            "not necessarily the best parameter setting "
            "across repeated runs."
        )

        st.markdown("### Full Schedule for Each Trial")

        for trial in trials:
            with st.expander(
                f"{trial['trial_name']} — "
                f"Fitness {trial['fitness']:.2f}",
                expanded=True,
            ):
                st.write(
                    f"CO_R: {trial['co_r']:.2f} | "
                    f"MUT_R: {trial['mut_r']:.2f}"
                )

                show_schedule(trial["schedule"])

                st.download_button(
                    "Download Schedule",
                    data=trial["schedule"].to_csv(index=False),
                    file_name=(
                        f"{trial['trial_name'].replace(' ', '_')}"
                        "_schedule.csv"
                    ),
                    mime="text/csv",
                    key=f"download_{trial['trial_name']}",
                )

        st.markdown("### Reset Experiments")

        if st.button("🗑️ Clear Saved Trials"):
            st.session_state.trials = []
            st.rerun()


# ==========================================
# TAB 4: RATING CHANGES
# ==========================================

with tab4:
    st.markdown("### Program Rating Data")

    modified_df = pd.read_csv(
        "program_ratings_modified.csv"
    )

    st.markdown("#### Modified Rating Dataset")

    st.dataframe(
        modified_df,
        use_container_width=True,
        hide_index=True,
    )

    original_path = Path(
        "program_ratings_original.csv"
    )

    if original_path.exists():
        original_df = pd.read_csv(original_path)

        st.markdown("#### Original vs Modified Ratings")

        if (
            original_df.shape == modified_df.shape
            and original_df.columns.equals(
                modified_df.columns
            )
            and original_df.iloc[:, 0].equals(
                modified_df.iloc[:, 0]
            )
        ):
            changes = []

            for row in range(len(original_df)):
                for col in original_df.columns[1:]:
                    old = original_df.loc[row, col]
                    new = modified_df.loc[row, col]

                    if str(old) != str(new):
                        changes.append({
                            "Program": original_df.iloc[row, 0],
                            "Time Slot": col,
                            "Original Rating": old,
                            "Modified Rating": new,
                        })

            if changes:
                st.dataframe(
                    pd.DataFrame(changes),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("No rating changes detected.")
        else:
            st.warning(
                "Original and modified CSV structures "
                "do not match. Check row order and columns."
            )
    else:
        st.warning(
            "Original CSV not found. Upload "
            "program_ratings_original.csv to GitHub "
            "to display the rating changes."
        )

    st.caption(
        "Modified ratings represent assumptions "
        "for the scheduling experiment."
    )


# ==========================================
# TAB 5: METHODOLOGY
# ==========================================

with tab5:
    st.markdown("### Genetic Algorithm Methodology")

    st.markdown("""
    **1. Population Initialization**

    Generate random chromosomes representing
    TV program assignments for each time slot.

    **2. Fitness Evaluation**

    Calculate the total rating of all scheduled
    programs.

    **3. Tournament Selection**

    Select better-performing chromosomes
    as parents.

    **4. Single-Point Crossover**

    Exchange chromosome segments between
    two parents based on CO_R.

    **5. Mutation**

    Randomly change program assignments
    based on MUT_R.

    **6. Elitism**

    Preserve the best chromosome in each
    generation.

    **7. Final Schedule**

    Return the chromosome with the highest
    fitness in the final population.
    """)

    st.markdown("### Fitness Function")

    st.latex(
        r"F(C)=\\sum_{t=1}^{T} R_{C_t,t}"
    )

    st.write(
        "Where C is a chromosome, T is the number "
        "of time slots, and R is the rating of the "
        "selected program at each time slot."
    )

    st.markdown("### Experimental Controls")

    st.write(
        "For fair comparison, use the same dataset, "
        "population size, generation count and seed "
        "while changing crossover and mutation rates."
    )

    st.warning(
        "This implementation permits repeated programs "
        "across time slots. Additional scheduling "
        "constraints must be implemented if required "
        "by the original Week 4 tutorial."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "TV Scheduling Optimizer | "
    "JIE42903 Evolutionary Computing | "
    "Genetic Algorithm Dashboard"
)
