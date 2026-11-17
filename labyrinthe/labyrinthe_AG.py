import random

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
LONGUEUR_CHROMOSOME = 60
MOUVEMENTS = ['H', 'B', 'G', 'D']


def simuler_parcours(chromosome):
    x, y = DEPART
    chemin = [DEPART]
    mouvements_valides = []

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
            mouvements_valides.append(move)
            if (x, y) == SORTIE:
                break

    return chemin, mouvements_valides


def evaluer_labyrinthe(chromosome):
    chemin, _ = simuler_parcours(chromosome)
    pos_finale = chemin[-1]

    if pos_finale == SORTIE:
        return -1000 + len(chemin)
    else:
        distance = abs(pos_finale[0] - SORTIE[0]) + abs(pos_finale[1] - SORTIE[1])
        return distance + (len(chemin) * 0.1)


def selection_tournoi(population, k=3):
    return min(random.sample(population, k), key=evaluer_labyrinthe)

def croisement_simple(p1, p2):
    point = random.randint(1, LONGUEUR_CHROMOSOME - 1)
    e1 = p1[:point] + p2[point:]
    e2 = p2[:point] + p1[point:]
    return e1, e2


def mutation_transposition_quelconque(sol, taux=0.1):
    v = sol[:]
    if random.random() < taux:
        i, j = random.sample(range(LONGUEUR_CHROMOSOME), 2)
        v[i], v[j] = v[j], v[i]
    return v


def ag_labyrinthe(pop_size=100, generations=500):
    population = [[random.choice(MOUVEMENTS) for _ in range(LONGUEUR_CHROMOSOME)] for _ in range(pop_size)]

    for _ in range(generations):
        population = sorted(population, key=evaluer_labyrinthe)
        nouvelle_pop = population[:5]

        while len(nouvelle_pop) < pop_size:
            p1 = selection_tournoi(population)
            p2 = selection_tournoi(population)
            e1, e2 = croisement_simple(p1, p2)
            e1 = mutation_transposition_quelconque(e1)
            e2 = mutation_transposition_quelconque(e2)
            nouvelle_pop.extend([e1, e2])

        population = nouvelle_pop[:pop_size]

    meilleure = min(population, key=evaluer_labyrinthe)
    return meilleure, evaluer_labyrinthe(meilleure)


if __name__ == "__main__":
    print("=== LABYRINTHE - ALGORITHME GÉNÉTIQUE ===")
    sol, val = ag_labyrinthe()
    chemin, mouvements_utiles = simuler_parcours(sol)

    print(f"\nStatut : {'SUCCÈS ! Le robot a trouvé la sortie.' if chemin[-1] == SORTIE else 'ÉCHEC - Le robot est bloqué.'}")
    print(f"Distance finale : {val:.2f}")
    print(f"Nombre de pas   : {len(chemin) - 1}")
    print(f"\nChemin emprunté :")
    print(f"Départ {DEPART} -> ... -> Arrivée {chemin[-1]}")
