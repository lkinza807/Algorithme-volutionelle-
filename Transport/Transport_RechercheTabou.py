import random
from collections import deque

COUTS = [[5, 3, 4], [6, 7, 2]]
OFFRES = [8, 9]
DEMANDES = [4, 5, 8]
N_DEPOTS = len(OFFRES)
N_MAGASINS = len(DEMANDES)


def decoder(solution):
    return [solution[0:3], solution[3:6]]


def evaluer_transport(solution):
    mat = decoder(solution)
    cout_total = 0
    for i in range(N_DEPOTS):
        if sum(mat[i]) != OFFRES[i]: return float('inf')
    for j in range(N_MAGASINS):
        if sum(mat[i][j] for i in range(N_DEPOTS)) != DEMANDES[j]: return float('inf')

    for i in range(N_DEPOTS):
        for j in range(N_MAGASINS):
            cout_total += mat[i][j] * COUTS[i][j]
    return cout_total


def generer_solution_initiale():
    while True:
        sol = [random.randint(0, min(OFFRES[i], DEMANDES[j])) for i in range(N_DEPOTS) for j in range(N_MAGASINS)]
        if evaluer_transport(sol) != float('inf'):
            return sol


def generer_voisins(solution):
    voisins = []
    for i in range(6):
        for j in range(i + 1, 6):
            if solution[i] > 0:
                voisin = solution[:]
                voisin[i] -= 1
                voisin[j] += 1
                if evaluer_transport(voisin) != float('inf'):
                    voisins.append(voisin)
    return voisins


def tabou_transport(iterations=500, taille_tabou=10):
    solution_actuelle = generer_solution_initiale()
    meilleure_solution = solution_actuelle[:]
    meilleure_valeur = evaluer_transport(solution_actuelle)
    tabou_list = deque(maxlen=taille_tabou)

    for _ in range(iterations):
        voisins = [v for v in generer_voisins(solution_actuelle) if v not in tabou_list]
        if not voisins: break

        solution_actuelle = min(voisins, key=evaluer_transport)
        valeur_actuelle = evaluer_transport(solution_actuelle)
        tabou_list.append(solution_actuelle)

        if valeur_actuelle < meilleure_valeur:
            meilleure_solution = solution_actuelle[:]
            meilleure_valeur = valeur_actuelle

    return decoder(meilleure_solution), meilleure_valeur


if __name__ == "__main__":
    print("=== TRANSPORT - RECHERCHE TABOU ===")
    sol, cout = tabou_transport()
    print(f"Matrice d'allocation (D1, D2) :\n{sol}")
    print(f"Coût total minimal            : {cout}")