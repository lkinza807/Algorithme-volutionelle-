import random

DISTANCES_TSP = [
    [0, 2, 2, 7, 15, 2, 5, 7, 6, 5, 5, 2, 10, 2, 9],
    [2, 0, 10, 4, 14, 3, 7, 15, 8, 2, 2, 9, 10, 3, 4],
    [2, 10, 0, 1, 4, 3, 4, 3, 2, 3, 2, 1, 7, 4, 1],
    [7, 4, 1, 0, 2, 15, 7, 7, 5, 4, 2, 4, 7, 1, 3],
    [15, 14, 4, 2, 0, 7, 3, 2, 2, 7, 8, 6, 8, 2, 5],
    [2, 3, 3, 15, 7, 0, 1, 7, 2, 10, 3, 5, 7, 3, 1],
    [5, 7, 4, 7, 3, 1, 0, 2, 1, 3, 6, 2, 4, 10, 7],
    [7, 15, 3, 7, 2, 7, 2, 0, 1, 4, 2, 9, 4, 7, 7],
    [6, 8, 2, 5, 2, 2, 1, 1, 0, 2, 3, 5, 7, 1, 5],
    [5, 2, 3, 4, 7, 10, 3, 4, 2, 0, 8, 10, 15, 7, 1],
    [5, 2, 2, 2, 8, 3, 6, 2, 3, 8, 0, 7, 8, 5, 6],
    [2, 9, 1, 4, 6, 5, 2, 9, 5, 10, 7, 0, 6, 10, 6],
    [10, 10, 7, 7, 8, 7, 4, 4, 7, 15, 8, 6, 0, 1, 9],
    [2, 3, 4, 1, 2, 3, 10, 7, 1, 7, 5, 10, 1, 0, 4],
    [9, 4, 1, 3, 5, 1, 7, 7, 5, 1, 6, 6, 9, 4, 0]
]
N_VILLES = len(DISTANCES_TSP)


def calculer_distance(solution):
    distance = 0
    for i in range(len(solution)):
        distance += DISTANCES_TSP[solution[i]][solution[(i + 1) % len(solution)]]
    return distance

def selection_tournoi(population, k=3):
    selectionnes = []
    for _ in range(len(population)):
        concurrents = random.sample(population, k)
        gagnant = min(concurrents, key=calculer_distance)
        selectionnes.append(gagnant)
    return selectionnes


def croisement_simple(p1, p2):
    size = len(p1)
    point = random.randint(1, size - 1)
    enfant1 = [-1] * size
    enfant1[:point] = p1[:point]
    idx = point
    for ville in p2:
        if ville not in enfant1:
            enfant1[idx] = ville
            idx += 1
    enfant2 = [-1] * size
    enfant2[:point] = p2[:point]
    idx = point
    for ville in p1:
        if ville not in enfant2:
            enfant2[idx] = ville
            idx += 1
    return enfant1, enfant2

def mutation_transposition_quelconque(solution, taux_mutation=0.1):
    if random.random() < taux_mutation:
        i, j = random.sample(range(len(solution)), 2)
        solution[i], solution[j] = solution[j], solution[i]
    return solution

def algorithme_genetique_tsp(pop_size=100, generations=500):
    population = [random.sample(range(N_VILLES), N_VILLES) for _ in range(pop_size)]

    for _ in range(generations):
        selectionnes = selection_tournoi(population, k=3)

        nouvelle_pop = []

        for i in range(0, pop_size, 2):
            p1 = selectionnes[i]
            p2 = selectionnes[(i + 1) % pop_size]
            enfant1, enfant2 = croisement_simple(p1, p2)

            enfant1 = mutation_transposition_quelconque(enfant1)
            enfant2 = mutation_transposition_quelconque(enfant2)

            nouvelle_pop.extend([enfant1, enfant2])

        population = nouvelle_pop[:pop_size]

    meilleure_solution = min(population, key=calculer_distance)
    return meilleure_solution, calculer_distance(meilleure_solution)


if __name__ == "__main__":
    print("=== TSP - ALGORITHME GÉNÉTIQUE ===")
    print("Méthodes utilisées :")
    print("- Sélection : Tournoi (k=3)")
    print("- Croisement : Simple (Ordered Crossover)")
    print("- Mutation : Transposition de deux allèles quelconques")
    sol, dist = algorithme_genetique_tsp()
    print(f"\nMeilleure solution trouvée : {sol}")
    print(f"Distance minimale          : {dist}")