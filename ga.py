import random
import dane
from deap import base, creator, tools, algorithms

# 1. Definicja fitnessu i osobnika – MAKSYMALIZACJA
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
N = dane.N  # długość permutacji

# 2. Osobnik: losowa permutacja 0..N-1
toolbox.register("indices", random.sample, range(N), N)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 3. Funkcja celu – MAKSYMALIZACJA
def eval_individual(ind):
    return dane.evaluate(ind)

toolbox.register("evaluate", eval_individual)

# 4. Operatory GA dla permutacji
toolbox.register("mate", tools.cxPartialyMatched)          # PMX
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=5)

# 5. Główna pętla ewolucyjna
def mainAG():
    pop = toolbox.population(n=3*N)
    NGEN, CXPB, MUTPB = 6*N, 0.7, 0.2

    algorithms.eaSimple(pop, toolbox,
                        cxpb=CXPB, mutpb=MUTPB,
                        ngen=NGEN, verbose=False)

    best = tools.selBest(pop, 1)[0]
    print("Najlepszy osobnik:", best)
    print("Fitness:", best.fitness.values)
    return best
