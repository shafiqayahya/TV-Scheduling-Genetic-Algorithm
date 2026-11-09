import csv
import math
import random


def load_ratings(path):
    with open(path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames
        if not columns or columns[0] != "Type of Program":
            raise ValueError("Expected first CSV column: Type of Program")
        if len(columns) < 3 or any(not c.startswith("Hour ") for c in columns[1:]):
            raise ValueError("Expected at least two 'Hour N' columns")
        try:
            hours = [int(column.removeprefix("Hour ")) for column in columns[1:]]
        except ValueError as exc:
            raise ValueError("Hour columns must contain integer hours") from exc
        if len(set(hours)) != len(hours):
            raise ValueError("Hour columns must be unique")
        ratings = {}
        for row in reader:
            name = (row[columns[0]] or "").strip()
            if not name or name in ratings:
                raise ValueError("Program names must be non-empty and unique")
            try:
                values = [float(row[column]) for column in columns[1:]]
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid rating for program {name}") from exc
            if not all(math.isfinite(v) and v >= 0 for v in values):
                raise ValueError("Ratings must be finite and non-negative")
            ratings[name] = values
    if len(ratings) < 2:
        raise ValueError("At least two programs are required")
    return ratings, hours


def fitness(schedule, ratings):
    return sum(ratings[program][slot] for slot, program in enumerate(schedule))


def run_ga(ratings, hours, crossover_rate=0.8, mutation_rate=0.2,
           generations=100, population_size=50, elitism_size=2, seed=42):
    if not 0 <= crossover_rate <= 0.95 or not 0 <= mutation_rate <= 1.0:
        raise ValueError("Invalid crossover or mutation rate")
    if population_size < 2 or not 1 <= elitism_size < population_size or generations < 1:
        raise ValueError("Invalid GA configuration")
    programs = list(ratings)
    n = len(hours)
    if len(programs) < 2 or n < 2 or any(len(v) != n for v in ratings.values()):
        raise ValueError("At least two programs, two slots and complete ratings are required")

    rng = random.Random(seed)
    population = [[rng.choice(programs) for _ in range(n)] for _ in range(population_size)]
    best = None
    best_score = float("-inf")
    history = []

    def tournament():
        candidates = rng.choices(population, k=3)
        return max(candidates, key=lambda schedule: fitness(schedule, ratings))

    for generation in range(generations + 1):
        population.sort(key=lambda schedule: fitness(schedule, ratings), reverse=True)
        score = fitness(population[0], ratings)
        if score > best_score:
            best_score = score
            best = population[0].copy()
        history.append({"Generation": generation, "Best Fitness": round(best_score, 4)})
        if generation == generations:
            break

        next_population = [p.copy() for p in population[:elitism_size]]
        while len(next_population) < population_size:
            p1, p2 = tournament(), tournament()
            if rng.random() < crossover_rate:
                point = rng.randint(1, n - 1)
                c1 = p1[:point] + p2[point:]
                c2 = p2[:point] + p1[point:]
            else:
                c1, c2 = p1.copy(), p2.copy()
            for child in (c1, c2):
                # Mutation rate is per offspring; one program gene changes on mutation.
                if rng.random() < mutation_rate:
                    idx = rng.randrange(n)
                    alternatives = [p for p in programs if p != child[idx]]
                    child[idx] = rng.choice(alternatives)
                if len(next_population) < population_size:
                    next_population.append(child)
        population = next_population

    rows = [
        {"Hour": f"Hour {hour}", "Program": program, "Rating": ratings[program][i]}
        for i, (hour, program) in enumerate(zip(hours, best))
    ]
    upper_bound = sum(max(values[i] for values in ratings.values()) for i in range(n))
    return rows, best_score, upper_bound, history
