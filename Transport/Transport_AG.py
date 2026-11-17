import random

COUTS = [[5, 3, 4], [6, 7, 2]]
OFFRES = [8, 9]
DEMANDES = [4, 5, 8]
N_DEPOTS, N_MAGASINS = 2, 3


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


def selection_tournoi(population, k=3):
    return min(random.sample(population, k), key=evaluer_transport)


def croisement_simple(p1, p2):
    point = random.randint(1, 5)
    e1 = p1[:point] + p2[point:]
    e2 = p2[:point] + p1[point:]
    return e1, e2


def mutation_transposition(sol):
    v = sol[:]
    i, j = random.sample(range(6), 2)
    v[i], v[j] = v[j], v[i]
    return v


def ag_transport(pop_size=50, generations=100):
    population = [generer_solution_initiale() for _ in range(pop_size)]

    for _ in range(generations):
        nouvelle_pop = []
        for _ in range(pop_size // 2):
            p1 = selection_tournoi(population)
            p2 = selection_tournoi(population)
            e1, e2 = croisement_simple(p1, p2)
            e1 = mutation_transposition(e1)
            e2 = mutation_transposition(e2)
            if evaluer_transport(e1) != float('inf'): nouvelle_pop.append(e1)
            if evaluer_transport(e2) != float('inf'): nouvelle_pop.append(e2)

        if len(nouvelle_pop) > 0:
            population = nouvelle_pop + population[:pop_size - len(nouvelle_pop)]

    meilleure = min(population, key=evaluer_transport)
    return decoder(meilleure), evaluer_transport(meilleure)


if __name__ == "__main__":
    print("=== TRANSPORT - ALGORITHME GÉNÉTIQUE ===")
    sol, cout = ag_transport()
    print(f"Matrice d'allocation (D1, D2) :\n{sol}")
    print(f"Coût total minimal            : {cout}")