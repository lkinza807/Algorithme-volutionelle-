import random
import math

COUTS = [[5, 3, 4], [6, 7, 2]]
OFFRES = [8, 9]
DEMANDES = [4, 5, 8]
N_DEPOTS = len(OFFRES)
N_MAGASINS = len(DEMANDES)


def decoder(solution): return [solution[0:3], solution[3:6]]


def evaluer_transport(solution):
    mat = decoder(solution)
    for i in range(N_DEPOTS):
        if sum(mat[i]) != OFFRES[i]: return float('inf')
    for j in range(N_MAGASINS):
        if sum(mat[i][j] for i in range(N_DEPOTS)) != DEMANDES[j]: return float('inf')
    return sum(mat[i][j] * COUTS[i][j] for i in range(N_DEPOTS) for j in range(N_MAGASINS))


def generer_solution_initiale():
    while True:
        sol = [random.randint(0, min(OFFRES[i], DEMANDES[j])) for i in range(N_DEPOTS) for j in range(N_MAGASINS)]
        if evaluer_transport(sol) != float('inf'): return sol


def generer_voisin(solution):
    voisin = solution[:]
    i = random.randint(0, 5)
    j = random.randint(0, 5)
    if i != j and voisin[i] > 0:
        voisin[i] -= 1
        voisin[j] += 1
    return voisin


def recuit_transport(temp_init=100, temp_fin=0.1, alpha=0.95):
    solution_actuelle = generer_solution_initiale()
    valeur_actuelle = evaluer_transport(solution_actuelle)
    meilleure_solution = solution_actuelle[:]
    meilleure_valeur = valeur_actuelle
    temp = temp_init

    while temp > temp_fin:
        voisin = generer_voisin(solution_actuelle)
        valeur_voisin = evaluer_transport(voisin)
        if valeur_voisin == float('inf'): continue

        delta = valeur_voisin - valeur_actuelle
        if delta < 0 or random.random() < math.exp(-delta / temp):
            solution_actuelle = voisin
            valeur_actuelle = valeur_voisin
            if valeur_actuelle < meilleure_valeur:
                meilleure_solution = solution_actuelle[:]
                meilleure_valeur = valeur_actuelle
        temp *= alpha

    return decoder(meilleure_solution), meilleure_valeur


if __name__ == "__main__":
    print("=== TRANSPORT - RECUIT SIMULÉ ===")
    sol, cout = recuit_transport()
    print(f"Matrice d'allocation (D1, D2) :\n{sol}")
    print(f"Coût total minimal            : {cout}")