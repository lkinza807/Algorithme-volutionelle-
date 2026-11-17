import random
from collections import deque

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
            if (x, y) == SORTIE:
                break
    return chemin

def evaluer_labyrinthe(chromosome):
    chemin = simuler_parcours(chromosome)
    position_finale = chemin[-1]

    distance = abs(position_finale[0] - SORTIE[0]) + abs(position_finale[1] - SORTIE[1])
    return distance + (len(chemin) * 0.1)


def generer_voisin(chromosome):
    voisin = chromosome[:]
    i = random.randint(0, LONGUEUR_CHROMOSOME - 1)
    voisin[i] = random.choice(MOUVEMENTS)
    return voisin


def tabou_labyrinthe(iterations=1000, taille_tabou=50):
    solution_actuelle = [random.choice(MOUVEMENTS) for _ in range(LONGUEUR_CHROMOSOME)]
    meilleure_solution = solution_actuelle[:]
    meilleure_valeur = evaluer_labyrinthe(solution_actuelle)
    tabou_list = deque(maxlen=taille_tabou)

    for _ in range(iterations):
        voisins = [generer_voisin(solution_actuelle) for _ in range(20)]
        voisins = [v for v in voisins if v not in tabou_list]
        if not voisins: break

        solution_actuelle = min(voisins, key=evaluer_labyrinthe)
        valeur_actuelle = evaluer_labyrinthe(solution_actuelle)
        tabou_list.append(solution_actuelle)

        if valeur_actuelle < meilleure_valeur:
            meilleure_solution = solution_actuelle[:]
            meilleure_valeur = valeur_actuelle

    return meilleure_solution, meilleure_valeur


if __name__ == "__main__":
    print("=== LABYRINTHE - RECHERCHE TABOU ===")
    sol, val = tabou_labyrinthe()
    print(f"Distance finale à la sortie : {val:.2f}")
    print(f"Séquence de mouvements      : {sol}")