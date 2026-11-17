import random
import math

LABYRINTHE = [
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0]
]
N, M = len(LABYRINTHE), len(LABYRINTHE[0])
DEPART = (0, 0)
SORTIE = (9, 9)
LONGUEUR_CHROMOSOME = 40
MOUVEMENTS = ['H', 'B', 'G', 'D']


def simuler_parcours(chromosome):
    x, y = DEPART
    chemin = [DEPART]
    for move in chromosome:
        nx, ny = x, y
        if move == 'H':
            nx -= 1
        elif move == 'B':
            nx += 1
        elif move == 'G':
            ny -= 1
        elif move == 'D':
            ny += 1
        if 0 <= nx < N and 0 <= ny < M and LABYRINTHE[nx][ny] == 0:
            x, y = nx, ny
            chemin.append((x, y))
            if (x, y) == SORTIE: break
    return chemin


def evaluer_labyrinthe(chromosome):
    chemin = simuler_parcours(chromosome)
    pos_finale = chemin[-1]
    return abs(pos_finale[0] - SORTIE[0]) + abs(pos_finale[1] - SORTIE[1]) + (len(chemin) * 0.1)


def generer_voisin(chromosome):
    voisin = chromosome[:]
    i = random.randint(0, LONGUEUR_CHROMOSOME - 1)
    voisin[i] = random.choice(MOUVEMENTS)
    return voisin


def recuit_labyrinthe(temp_init=10.0, temp_fin=0.01, alpha=0.99):
    solution_actuelle = [random.choice(MOUVEMENTS) for _ in range(LONGUEUR_CHROMOSOME)]
    valeur_actuelle = evaluer_labyrinthe(solution_actuelle)
    meilleure_solution = solution_actuelle[:]
    meilleure_valeur = valeur_actuelle
    temp = temp_init

    while temp > temp_fin:
        voisin = generer_voisin(solution_actuelle)
        valeur_voisin = evaluer_labyrinthe(voisin)

        delta = valeur_voisin - valeur_actuelle

        if delta < 0 or random.random() < math.exp(-delta / temp):
            solution_actuelle = voisin
            valeur_actuelle = valeur_voisin
            if valeur_actuelle < meilleure_valeur:
                meilleure_solution = solution_actuelle[:]
                meilleure_valeur = valeur_actuelle
        temp *= alpha

    return meilleure_solution, meilleure_valeur


if __name__ == "__main__":
    print("=== LABYRINTHE - RECUIT SIMULÉ ===")
    sol, val = recuit_labyrinthe()
    print(f"Distance finale à la sortie : {val:.2f}")
    print(f"Séquence de mouvements      : {sol}")