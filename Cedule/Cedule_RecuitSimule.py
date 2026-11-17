import random
import math

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
    return min(reserves)


def generer_solution_valide():
    solution = []
    for i in range(N_UNITES):
        bits = ['0'] * 4
        indices = random.sample(range(4), INTERVALLES_REQUIS[i])
        for idx in indices:
            bits[idx] = '1'
        solution.append(''.join(bits))
    return solution


def generer_voisin(solution):
    voisin = solution[:]

    candidates = [i for i in range(N_UNITES) if 0 < solution[i].count('1') < 4]

    if not candidates:
        return voisin

    i = random.choice(candidates)
    bits = list(voisin[i])

    pos_1 = random.choice([k for k in range(4) if bits[k] == '1'])
    pos_0 = random.choice([k for k in range(4) if bits[k] == '0'])

    bits[pos_1], bits[pos_0] = bits[pos_0], bits[pos_1]
    voisin[i] = ''.join(bits)
    return voisin


def recuit_maintenance(temp_init=100, temp_fin=0.1, alpha=0.95):
    solution_actuelle = generer_solution_valide()
    valeur_actuelle = evaluer_maintenance(solution_actuelle)
    meilleure_solution = solution_actuelle[:]
    meilleure_valeur = valeur_actuelle
    temp = temp_init

    while temp > temp_fin:
        voisin = generer_voisin(solution_actuelle)
        valeur_voisin = evaluer_maintenance(voisin)

        delta = valeur_voisin - valeur_actuelle

        if delta > 0 or random.random() < math.exp(delta / temp):
            solution_actuelle = voisin
            valeur_actuelle = valeur_voisin

            if valeur_actuelle > meilleure_valeur:
                meilleure_solution = solution_actuelle[:]
                meilleure_valeur = valeur_actuelle

        temp *= alpha

    return meilleure_solution, meilleure_valeur


if __name__ == "__main__":
    print("=== MAINTENANCE - RECUIT SIMULÉ ===")
    sol, val = recuit_maintenance()
    print(f"Séquence de maintenance (Unités 1 à 7) :\n{sol}")
    print(f"Réserve minimale (MW)                  : {val}")