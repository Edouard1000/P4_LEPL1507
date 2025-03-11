import numpy as np
import random
import networkx as nx
import utility_functions as uf  
from tqdm import tqdm

def evaluate_fitness(graph, E, J, C):
    """Calcule la fitness d'un individu (ensemble de connexions)."""
    total_distance = 0

    for (At, Al) in J:
        try:
            total_distance += nx.shortest_path_length(graph, source=At, target=Al, weight='weight')
        except:
            total_distance += 1000000  # Pénalité pour trajets impossibles
    return (total_distance / len(J)) + C * len(E)

def initialize_population(P, population_size):
    """Génère une population initiale de solutions."""
    return [random.sample(P, random.randint(len(P)//3, len(P))) for _ in range(population_size)]

def selection(population, fitnesses, k=3):
    """Sélectionne les meilleurs individus par tournoi."""
    selected = random.choices(population, weights=[1/f for f in fitnesses], k=k)
    return min(selected, key=lambda ind: fitnesses[population.index(ind)])

def crossover(parent1, parent2):
    """Croisement entre deux parents."""
    split = random.randint(1, min(len(parent1), len(parent2))-1)
    child = list(set(parent1[:split] + parent2[split:]))
    return child

def mutate(individual, P, mutation_rate=0.1):
    """Mutation d'un individu."""
    if random.random() < mutation_rate:
        if random.random() < 0.5 and len(individual) > 1:
            individual.remove(random.choice(individual))  # Suppression
        else:
            individual.append(random.choice(list(set(P) - set(individual))))  # Ajout
    return individual

def distance(start, end):
    """Calcule la distance entre deux aéroports."""
    return 5


def genetic_algorithm(P, J, C, population_size=500, generations=200, mutation_rate=0.1):
    """Exécute l'algorithme génétique."""
    population = initialize_population(P, population_size)
    
    for _ in tqdm(range(generations), desc="Générations"):
        fitnesses = []
        for E in population:
            graph = nx.DiGraph()
            for start, end, weight in E:
                graph.add_edge(start, end, weight=weight)  # Ajout de poids aux arêtes
            fitnesses.append(evaluate_fitness(graph, E, J, C))
        
        new_population = []
        for _ in range(population_size//2):
            parent1, parent2 = selection(population, fitnesses), selection(population, fitnesses)
            child1, child2 = crossover(parent1, parent2), crossover(parent2, parent1)
            new_population.extend([mutate(child1, P, mutation_rate), mutate(child2, P, mutation_rate)])
        
        #population = sorted(new_population, key=lambda ind: evaluate_fitness(nx.DiGraph(ind), ind, J, C))[:population_size]
        population = sorted(
            new_population, 
            key=lambda ind: evaluate_fitness(nx.DiGraph([(start, end, {"weight": weight}) for start, end, weight in ind]), ind, J, C)
        )[:population_size]


    
    return population[0]  # Meilleure solution trouvée

