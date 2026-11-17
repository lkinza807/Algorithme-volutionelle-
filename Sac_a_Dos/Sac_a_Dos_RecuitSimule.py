import random
import math

# DONNÉES DU PROBLÈME , Format: (Valeur, Poids)
OBJETS = [
    (10, 4), (4, 12), (2, 1), (1, 1), (2, 2),
    (5, 3), (8, 6), (3, 2), (7, 5), (6, 4),
    (12, 8), (9, 7), (4, 3), (15, 9), (5, 2),
    (2, 1), (11, 6), (6, 3), (8, 4), (3, 1)
]
CAPACITE_SAC = 15
N_OBJETS = len(OBJETS)


def evaluer_sac(solution):
    poids_total = 0
    valeur_totale = 0
    for i in range(N_OBJETS):
        if solution[i] == 1:
            poids_total += OBJETS[i][1]
            valeur_totale += OBJETS[i][0]
    if poids_total > CAPACITE_SAC:
        depassement = poids_total - CAPACITE_SAC
        return valeur_totale - (depassement * 10)
    return valeur_totale


def poids_solution(solution):
    return sum(OBJETS[i][1] for i in range(N_OBJETS) if solution[i] == 1)


def generer_solution_valide():
    solution = [0] * N_OBJETS
    poids = 0
    indices = list(range(N_OBJETS))
    random.shuffle(indices)
    for i in indices:
        if poids + OBJETS[i][1] <= CAPACITE_SAC and random.random() < 0.7:
            solution[i] = 1
            poids += OBJETS[i][1]
    return solution


def generer_voisin(solution):
    voisin = solution[:]
    if random.random() < 0.5:
        i = random.randint(0, N_OBJETS - 1)
        voisin[i] = 1 - voisin[i]
    else:
        i, j = random.sample(range(N_OBJETS), 2)
        voisin[i] = 1 - voisin[i]
        voisin[j] = 1 - voisin[j]
    return voisin


def recuit_simule_sac(temperature_init=500, temperature_fin=0.01, alpha=0.995, iterations_par_temp=10):
    solution_actuelle = generer_solution_valide()
    valeur_actuelle = evaluer_sac(solution_actuelle)
    meilleure_solution = solution_actuelle[:]
    meilleure_valeur = valeur_actuelle
    temp = temperature_init

    while temp > temperature_fin:
        for _ in range(iterations_par_temp):
            voisin = generer_voisin(solution_actuelle)
            valeur_voisin = evaluer_sac(voisin)

            delta = valeur_voisin - valeur_actuelle

            if delta > 0 or random.random() < math.exp(delta / temp):
                solution_actuelle = voisin
                valeur_actuelle = valeur_voisin

                if valeur_actuelle > meilleure_valeur and poids_solution(solution_actuelle) <= CAPACITE_SAC:
                    meilleure_solution = solution_actuelle[:]
                    meilleure_valeur = valeur_actuelle

        temp *= alpha

    return meilleure_solution, meilleure_valeur


if __name__ == "__main__":
    print("=== SAC À DOS - RECUIT SIMULÉ ===")
    print("Paramètres : T_init=500, T_fin=0.01, alpha=0.995, 10 itérations/temp")
    sol, val = recuit_simule_sac()
    poids = poids_solution(sol)
    print(f"\nMeilleure solution trouvée : {sol}")
    print(f"Valeur maximale            : {val}")
    print(f"Poids total utilisé        : {poids} / {CAPACITE_SAC} kg")
    print(f"Solution valide ?          : {'OUI' if poids <= CAPACITE_SAC else 'NON'}")