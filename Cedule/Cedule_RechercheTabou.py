import random
from collections import deque

CAPACITES = [20, 15, 35, 40, 15, 15, 10]
INTERVALLES_REQUIS = [2, 2, 1, 1, 1, 1, 1]
DEMANDES = [80, 90, 65, 70]
CAPACITE_TOTALE = sum(CAPACITES)
N_UNITES = len(CAPACITES)


def evaluer_maintenance(solution):
    perte = [0, 0, 0, 0]
    for i in range(N_UNITES):
        for j in range(4):
            if solution[i][j] == '1':
                perte[j] += CAPACITES[i]

    reserves = [CAPACITE_TOTALE - perte[j] - DEMANDES[j] for j in range(4)]
    min_reserve = min(reserves)

    if min_reserve < 0:
        return min_reserve * 1000

    return min_reserve


def generer_solution_valide():
    solution = []
    for i in range(N_UNITES):
        bits = ['0'] * 4
        indices = random.sample(range(4), INTERVALLES_REQUIS[i])
        for idx in indices:
            bits[idx] = '1'
        solution.append(''.join(bits))
    return solution


def generer_voisins(solution):
    voisins = []
    for i in range(N_UNITES):
        if 0 < solution[i].count('1') < 4:
            for j in range(4):
                for k in range(4):
                    if j != k and solution[i][j] == '1' and solution[i][k] == '0':
                        voisin = solution[:]
                        bits = list(voisin[i])
                        bits[j] = '0'
                        bits[k] = '1'
                        voisin[i] = ''.join(bits)
                        voisins.append(voisin)
    return voisins


def tabou_maintenance(iterations=1000, taille_tabou=20):
    solution_actuelle = generer_solution_valide()
    meilleure_solution = solution_actuelle[:]
    meilleure_valeur = evaluer_maintenance(solution_actuelle)
    tabou_list = deque(maxlen=taille_tabou)

    for _ in range(iterations):
        voisins = generer_voisins(solution_actuelle)

        voisins_valides = [v for v in voisins if v not in tabou_list]
        if not voisins_valides:
            voisins_valides = voisins

        if not voisins_valides:
            break

        solution_actuelle = max(voisins_valides, key=evaluer_maintenance)
        valeur_actuelle = evaluer_maintenance(solution_actuelle)
        tabou_list.append(solution_actuelle)

        if valeur_actuelle > meilleure_valeur:
            meilleure_solution = solution_actuelle[:]
            meilleure_valeur = valeur_actuelle

    return meilleure_solution, meilleure_valeur


if __name__ == "__main__":
    print("=== MAINTENANCE - RECHERCHE TABOU ===")
    sol, val = tabou_maintenance()
    print(f"Séquence de maintenance (Unités 1 à 7) :\n{sol}")
    print(f"Réserve minimale (MW)                  : {val}")