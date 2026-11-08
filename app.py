from pathlib import Path
import pandas as pd
import streamlit as st
from ga_engine import load_ratings, run_ga

st.set_page_config(page_title="TV Scheduling | Genetic Algorithm", page_icon="📺", layout="wide", initial_sidebar_state="expanded")
ROOT = Path(__file__).parent
MODIFIED = ROOT / "program_ratings_modified.csv"
ORIGINAL = ROOT / "program_ratings_original.csv"

st.markdown("""<style>
:root {--rose:#BE365A;--burgundy:#881337;--wine:#64152D;--blush:#FFF1F4;}
.block-container {padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1250px;}
.hero {background:linear-gradient(115deg,#64152D 0%,#881337 58%,#BE365A 100%); padding:32px 34px; border-radius:19px; color:white; margin-bottom:20px; box-shadow:0 12px 30px rgba(100,21,45,.15);}
.hero .eyebrow {color:#FFDCE5; font-size:12px; letter-spacing:1.4px; font-weight:700;}
.hero h1 {color:#FFFFFF !important; margin:8px 0; font-size:2.35rem; line-height:1.2;}
.hero p {color:#FFE8EE; margin:0; font-size:15px;}
[data-testid="stMetric"] {background:#FFF4F6; border:1px solid #F4D8E0; padding:17px; border-radius:14px;}
[data-testid="stMetricLabel"] {color:#75233F;}
[data-testid="stMetricValue"] {color:#881337;}
.stButton>button[kind="primary"] {background:#A7234A; border-color:#A7234A; color:white; border-radius:11px; font-weight:700;}
.stButton>button[kind="primary"]:hover {background:#881337; border-color:#881337; color:white;}
section[data-testid="stSidebar"] {background:#FFF4F6; border-right:1px solid #F4D8E0;}
[data-testid="stTabs"] button[aria-selected="true"] {color:#881337;}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {background:#BE365A;}
a {color:#A7234A;}
</style>""", unsafe_allow_html=True)

ratings, hours = load_ratings(MODIFIED)
if "trials" not in st.session_state:
    st.session_state.trials = []

with st.sidebar:
    st.title("⚙️ GA Controls")
    st.caption("Configure one experiment at a time")
    co_r = st.slider("Crossover Rate (CO_R)", 0.0, 0.95, 0.80, 0.01)
    mut_r = st.number_input("Mutation Rate (MUT_R)", min_value=0.0, max_value=1.0, value=0.20, step=0.01, format="%.2f", help="Assignment default: 0.20. The stated experimental range is 0.01–0.05; clarify the contradiction with the lecturer.")
    if not 0.01 <= mut_r <= 0.05:
        st.warning("MUT_R is outside the stated trial range (0.01–0.05). The assignment also specifies a conflicting default of 0.20.")
    generations = st.number_input("Generations", min_value=1, max_value=2000, value=100, step=10)
    population_size = st.number_input("Population Size", min_value=4, max_value=1000, value=50, step=1)
    seed = st.number_input("Random Seed", min_value=0, max_value=1000000, value=42, step=1)
    run = st.button("▶ Run Genetic Algorithm", type="primary", use_container_width=True)
    st.divider()
    st.caption("Recommended fair comparison: keep generations, population size and seed unchanged across trials.")

st.markdown('''<div class="hero"><div class="eyebrow">JIE42903 · EVOLUTIONARY COMPUTING</div><h1>📺 TV Scheduling Optimizer</h1><p>Genetic Algorithm · Interactive Scheduling & Experiment Dashboard</p></div>''', unsafe_allow_html=True)
st.caption("18 hourly slots (06:00–23:00) · 10 program categories · Modified rating dataset")

if run:
    with st.spinner("Optimizing the TV schedule..."):
        rows, score, upper, history = run_ga(ratings, hours, co_r, mut_r, int(generations), int(population_size), seed=int(seed))
    st.session_state.current = {
        "rows": rows, "score": score, "upper": upper, "history": history,
        "co_r": co_r, "mut_r": mut_r, "seed": int(seed),
        "generations": int(generations), "population_size": int(population_size),
    }

overview, scheduler, comparison, changes, methodology = st.tabs([
    "🏠 Overview", "📅 GA Scheduler", "📊 Trial Comparison", "📝 Rating Changes", "📘 Methodology"
])

with overview:
    st.subheader("Project overview")
    st.write("The algorithm chooses a program for each hourly TV slot to maximize the sum of the corresponding viewer ratings. Programs may be repeated across different slots.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Time slots", len(hours))
    c2.metric("Available programs", len(ratings))
    c3.metric("Saved trials", len(st.session_state.trials))
    st.info("Assignment clarification needed: default MUT_R = 0.20 conflicts with the specified trial range 0.01–0.05. The app preserves the stated default and allows values in the trial range.")
    st.markdown("**Workflow:** Choose parameters in the sidebar → Run GA → Review the full schedule → Save trial → Repeat with new rates → Compare all three trials.")

with scheduler:
    if "current" not in st.session_state:
        st.info("Set parameters in the sidebar and click **Run Genetic Algorithm** to generate a schedule.")
    else:
        r = st.session_state.current
        st.subheader("Generated TV Schedule")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Fitness", f"{r['score']:.2f}")
        c2.metric("Theoretical Upper Bound*", f"{r['upper']:.2f}")
        c3.metric("Fitness / Upper Bound", f"{r['score']/r['upper']:.1%}" if r['upper'] else "N/A")
        st.caption(f"CO_R = {r['co_r']:.2f} · MUT_R = {r['mut_r']:.2f} · Generations = {r['generations']} · Population = {r['population_size']} · Seed = {r['seed']}")
        st.dataframe(pd.DataFrame(r["rows"]), use_container_width=True, hide_index=True, height=660)
        st.caption("*Upper bound is the sum of the best available rating per time slot, assuming repeated programs are allowed and no additional scheduling constraints apply.")
        st.subheader("Fitness convergence")
        st.line_chart(pd.DataFrame(r["history"]).set_index("Generation"), use_container_width=True)
        left, right = st.columns(2)
        with left:
            st.download_button("⬇ Download schedule CSV", pd.DataFrame(r["rows"]).to_csv(index=False), file_name="generated_schedule.csv", mime="text/csv", use_container_width=True)
        with right:
            if st.button("💾 Save this trial for comparison", use_container_width=True):
                st.session_state.trials.append({**r, "trial": len(st.session_state.trials) + 1})
                st.success(f"Trial {len(st.session_state.trials)} saved. Open the Trial Comparison tab.")

with comparison:
    st.subheader("Experiment comparison")
    trials = st.session_state.trials
    if not trials:
        st.info("No saved trials yet. Run GA and save each trial from the GA Scheduler tab.")
    else:
        records = [{"Trial": t["trial"], "CO_R": t["co_r"], "MUT_R": t["mut_r"], "Generations": t["generations"], "Population": t["population_size"], "Seed": t["seed"], "Fitness": round(t["score"], 4), "Fitness / Upper Bound (%)": round(100 * t["score"] / t["upper"], 2) if t["upper"] else None} for t in trials]
        summary = pd.DataFrame(records)
        st.dataframe(summary, use_container_width=True, hide_index=True)
        st.bar_chart(summary.set_index("Trial")[["Fitness"]])
        best = max(trials, key=lambda t: t["score"])
        st.success(f"Highest observed fitness: Trial {best['trial']} ({best['score']:.2f}), CO_R={best['co_r']:.2f}, MUT_R={best['mut_r']:.2f}. This is a result for the recorded runs, not proof of universal optimality.")
        st.download_button("⬇ Download trial comparison CSV", summary.to_csv(index=False), file_name="trial_comparison.csv", mime="text/csv")
        st.markdown("### Full schedule for each trial")
        for t in trials:
            with st.expander(f"Trial {t['trial']} · CO_R {t['co_r']:.2f} · MUT_R {t['mut_r']:.2f} · Fitness {t['score']:.2f}", expanded=len(trials) <= 3):
                st.dataframe(pd.DataFrame(t["rows"]), use_container_width=True, hide_index=True, height=470)
                st.download_button(f"⬇ Download Trial {t['trial']} schedule", pd.DataFrame(t["rows"]).to_csv(index=False), file_name=f"trial_{t['trial']}_schedule.csv", mime="text/csv", key=f"dl_{t['trial']}")
        st.markdown("### Discussion prompts")
        st.write("Compare the fitness values and scheduled programs, describe convergence trends, and explain which recorded combination performed best. Because GA is stochastic, repeat trials using multiple seeds before making broader claims.")
        if st.button("🗑 Clear saved trials"):
            st.session_state.trials = []
            st.rerun()

with changes:
    st.subheader("CSV rating modifications")
    modified = pd.read_csv(MODIFIED)
    st.write("The deployed algorithm uses the **modified** rating file.")
    if ORIGINAL.exists():
        original = pd.read_csv(ORIGINAL)
        old = original.set_index("Type of Program")
        new = modified.set_index("Type of Program")
        changes_rows = []
        for name in new.index:
            for col in new.columns:
                if float(old.loc[name, col]) != float(new.loc[name, col]):
                    changes_rows.append({"Program": name, "Time": col.replace("Hour ", "") + ":00", "Original Rating": float(old.loc[name, col]), "Modified Rating": float(new.loc[name, col]), "Difference": round(float(new.loc[name, col]) - float(old.loc[name, col]), 3)})
        st.metric("Modified rating cells", len(changes_rows))
        st.dataframe(pd.DataFrame(changes_rows), use_container_width=True, hide_index=True)
        st.caption("Rating changes are experimental assumptions, not verified audience measurements. Explain the rationale for each change in the written report.")
    else:
        st.warning("Original CSV not uploaded. Add program_ratings_original.csv to display the before/after comparison.")
    with st.expander("View full modified rating dataset"):
        st.dataframe(modified, use_container_width=True, hide_index=True)

with methodology:
    st.subheader("How the GA works")
    st.markdown("""1. **Encoding:** Each chromosome has 18 genes, one program per hourly slot. Programs can repeat.\n2. **Fitness:** Sum of the rating for the selected program at each slot. Higher is better.\n3. **Selection:** Tournament selection (three sampled candidates).\n4. **Crossover:** Single-point crossover with probability CO_R per parent pair.\n5. **Mutation:** With probability MUT_R per offspring, replace one randomly selected program gene with a different program. **This is a per-offspring mutation rate, not a per-bit rate.**\n6. **Elitism:** Preserve the two highest-fitness schedules each generation.\n7. **Output:** Best schedule found and best-so-far fitness across generations.""")
    st.warning("The provided tutorial and this deployable GA may differ in representation or operators. Verify against the Week 4 tutorial before claiming an exact reproduction.")
    st.caption("Results are stored in this browser session. Download CSV files before closing or resetting the app.")
