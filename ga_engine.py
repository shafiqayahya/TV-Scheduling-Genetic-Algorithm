
import numpy as np
import pandas as pd


# ============================================
# LOAD PROGRAM RATINGS
# ============================================

def load_ratings(csv_path="program_ratings_modified.csv"):
    df = pd.read_csv(csv_path)

    programs = df["Type of Program"].tolist()
    hour_columns = [
        col for col in df.columns
        if col.startswith("Hour ")
    ]

    ratings = df[hour_columns].to_numpy(dtype=float)
    hours = [int(col.split()[1]) for col in hour_columns]

    return programs, hours, ratings


# ============================================
# FITNESS FUNCTION
# ============================================

def fitness_function(chromosome, ratings):
    total = 0.0

    for slot, program_index in enumerate(chromosome):
        total += ratings[program_index, slot]

    return float(total)


# ============================================
# INITIAL POPULATION
# ============================================

def initialize_population(pop_size, num_slots, num_programs, rng):
    return [
        rng.integers(0, num_programs, size=num_slots).tolist()
        for _ in range(pop_size)
    ]


# ============================================
# TOURNAMENT SELECTION
# ============================================

def selection(population, ratings, rng, tournament_size=3):
    indices = rng.choice(
        len(population),
        size=min(tournament_size, len(population)),
        replace=False
    )

    best_index = max(
        indices,
        key=lambda i: fitness_function(population[i], ratings)
    )

    return population[int(best_index)].copy()


# ============================================
# SINGLE POINT CROSSOVER
# ============================================

def crossover(parent1, parent2, crossover_rate, rng):
    if rng.random() < crossover_rate and len(parent1) > 1:
        point = int(rng.integers(1, len(parent1)))

        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]

        return child1, child2

    return parent1.copy(), parent2.copy()


# ============================================
# MUTATION
# ============================================

def mutation(chromosome, mutation_rate, num_programs, rng):
    child = chromosome.copy()

    for i in range(len(child)):
        if rng.random() < mutation_rate:
            current = child[i]

            new_value = int(rng.integers(0, num_programs - 1))

            if new_value >= current:
                new_value += 1

            child[i] = new_value

    return child


# ============================================
# GENETIC ALGORITHM
# ============================================

def genetic_algorithm(
    ratings,
    pop_size=50,
    generations=100,
    crossover_rate=0.8,
    mutation_rate=0.2,
    seed=42
):
    if pop_size < 2:
        raise ValueError("Population size must be at least 2.")

    if generations < 1:
        raise ValueError("Generations must be at least 1.")

    if not 0 <= crossover_rate <= 0.95:
        raise ValueError("Crossover rate must be between 0 and 0.95.")

    if not 0 <= mutation_rate <= 1:
        raise ValueError("Mutation rate must be between 0 and 1.")

    num_programs, num_slots = ratings.shape

    rng = np.random.default_rng(seed)

    population = initialize_population(
        pop_size, num_slots, num_programs, rng
    )

    best_history = []

    for generation in range(generations):
        population.sort(
            key=lambda c: fitness_function(c, ratings),
            reverse=True
        )

        best_history.append(
            fitness_function(population[0], ratings)
        )

        # Elitism: retain the best chromosome
        new_population = [population[0].copy()]

        while len(new_population) < pop_size:
            parent1 = selection(population, ratings, rng)
            parent2 = selection(population, ratings, rng)

            child1, child2 = crossover(
                parent1, parent2, crossover_rate, rng
            )

            child1 = mutation(
                child1, mutation_rate, num_programs, rng
            )

            child2 = mutation(
                child2, mutation_rate, num_programs, rng
            )

            new_population.append(child1)

            if len(new_population) < pop_size:
                new_population.append(child2)

        population = new_population

    population.sort(
        key=lambda c: fitness_function(c, ratings),
        reverse=True
    )

    best_chromosome = population[0]
    best_fitness = fitness_function(best_chromosome, ratings)

    best_history.append(best_fitness)

    return best_chromosome, best_fitness, best_history


# ============================================
# GENERATE SCHEDULE TABLE
# ============================================

def create_schedule(chromosome, programs, hours, ratings):
    rows = []

    for slot, program_index in enumerate(chromosome):
        rows.append({
            "Time": f"{hours[slot]:02d}:00",
            "Program": programs[program_index],
            "Rating": float(ratings[program_index, slot])
        })

    return pd.DataFrame(rows)


# ============================================
# CALCULATE UPPER BOUND
# ============================================

def calculate_upper_bound(ratings):
    return float(np.max(ratings, axis=0).sum())
