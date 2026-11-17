import random
import math

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

def recuit_simule_tsp(temperature_init=1000, temperature_fin=0.1, alpha=0.99):
    solution_actuelle = list(range(N_VILLES))
    random.shuffle(solution_actuelle)
    distance_actuelle = calculer_distance(solution_actuelle)
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = distance_actuelle
    temp = temperature_init

    while temp > temperature_fin:
        i, j = sorted(random.sample(range(N_VILLES), 2))
        voisin = solution_actuelle[:i] + solution_actuelle[i:j + 1][::-1] + solution_actuelle[j + 1:]
        distance_voisin = calculer_distance(voisin)

        delta = distance_voisin - distance_actuelle
        if delta < 0 or random.random() < math.exp(-delta / temp):
            solution_actuelle = voisin
            distance_actuelle = distance_voisin
            if distance_actuelle < meilleure_distance:
                meilleure_solution = solution_actuelle[:]
                meilleure_distance = distance_actuelle
        temp *= alpha

    return meilleure_solution, meilleure_distance

if __name__ == "__main__":
    print("=== TSP - RECUIT SIMULÉ ===")
    sol, dist = recuit_simule_tsp()
    print(f"Meilleure solution trouvée : {sol}")
    print(f"Distance minimale          : {dist}")