# TV Scheduling Using Genetic Algorithm

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

This app uses `program_ratings_modified.csv` (10 programs, 18 hourly slots). Each slot receives one program; programs can repeat. GA uses tournament selection, single-point crossover, one-gene mutation per selected child, and elitism. Fitness is the sum of the chosen program's rating in each slot. There are no constraints on repeated programs or genre diversity. The theoretical upper bound is the sum of the maximum rating per slot under these assumptions.

## Experiment

Use identical generations, population size and random seed across three trials; e.g. (CO_R, MUT_R) = (0.40, 0.01), (0.70, 0.03), (0.95, 0.05). Save each trial in the app and export comparison CSV. To assess randomness more reliably, repeat each combination with multiple seeds.

**Assignment ambiguity:** Default mutation rate 0.20 conflicts with the stated range 0.01–0.05. App retains the 0.20 default and permits the experimental range; seek lecturer clarification.

## Deploy

Upload `app.py`, `ga_engine.py`, `requirements.txt`, and `program_ratings_modified.csv` to a GitHub repository, then deploy `app.py` using Streamlit Community Cloud. Include deployment URL in report appendix.
