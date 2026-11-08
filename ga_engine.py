import csv
import random
from pathlib import Path


def load_ratings(path):
    with open(path, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames
        if not columns or columns[0] != 'Type of Program':
            raise ValueError('Expected first CSV column: Type of Program')
        hours = [int(c.replace('Hour ', '')) for c in columns[1:]]
        ratings = {}
        for row in reader:
            name = row[columns[0]].strip()
            if not name or name in ratings:
                raise ValueError('Program names must be non-empty and unique')
            ratings[name] = [float(row[c]) for c in columns[1:]]
    if not ratings or not hours:
        raise ValueError('CSV must contain programs and time slots')
    return ratings, hours


def fitness(schedule, ratings):
    return sum(ratings[program][slot] for slot, program in enumerate(schedule))


def run_ga(ratings, hours, crossover_rate=0.8, mutation_rate=0.2,
           generations=100, population_size=50, elitism_size=2, seed=42):
    if not 0 <= crossover_rate <= 0.95 or not 0 <= mutation_rate <= 1:
        raise ValueError('Invalid crossover or mutation rate')
    if population_size < 2 or not 1 <= elitism_size < population_size or generations < 1:
        raise ValueError('Invalid GA configuration')
    rng = random.Random(seed)
    programs = list(ratings)
    n = len(hours)
    # One gene per time slot. Programs may repeat because there are more slots than programs.
    population = [[rng.choice(programs) for _ in range(n)] for _ in range(population_size)]
    best = None
    best_score = float('-inf')
    history = []

    def tournament():
        candidates = rng.choices(population, k=3)
        return max(candidates, key=lambda s: fitness(s, ratings))

    for generation in range(generations + 1):
        population.sort(key=lambda s: fitness(s, ratings), reverse=True)
        score = fitness(population[0], ratings)
        if score > best_score:
            best_score = score
            best = population[0].copy()
        history.append({'Generation': generation, 'Best Fitness': round(best_score, 4)})
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
                if rng.random() < mutation_rate:
                    idx = rng.randrange(n)
                    alternatives = [p for p in programs if p != child[idx]]
                    child[idx] = rng.choice(alternatives or programs)
                if len(next_population) < population_size:
                    next_population.append(child)
        population = next_population

    rows = [{'Time Slot': f'{hour:02d}:00', 'Program': program,
             'Rating': ratings[program][i]} for i, (hour, program) in enumerate(zip(hours, best))]
    upper_bound = sum(max(r[i] for r in ratings.values()) for i in range(n))
    return rows, best_score, upper_bound, history
