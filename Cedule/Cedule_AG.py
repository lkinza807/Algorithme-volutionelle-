import random

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


def valide(solution):
    return all(solution[i].count('1') == INTERVALLES_REQUIS[i] for i in range(N_UNITES))


def generer_solution_valide():
    solution = []
    for i in range(N_UNITES):
        bits = ['0'] * 4
        indices = random.sample(range(4), INTERVALLES_REQUIS[i])
        for idx in indices:
            bits[idx] = '1'
        solution.append(''.join(bits))
    return solution


def selection_roulette(population):
    fitness = [max(0, evaluer_maintenance(ind)) for ind in population]
    total = sum(fitness)
    if total == 0: return random.sample(population, len(population))

    selectionnes = []
    for _ in range(len(population)):
        r = random.random() * total
        cumul = 0
        for i, f in enumerate(fitness):
            cumul += f
            if cumul >= r:
                selectionnes.append(population[i])
                break
    return selectionnes


def croisement_simple(p1, p2):
    point = random.randint(1, N_UNITES - 1)
    e1 = p1[:point] + p2[point:]
    e2 = p2[:point] + p1[point:]
    return e1, e2


def mutation_transposition_consecutive(sol):
    v = sol[:]
    i = random.randint(0, N_UNITES - 1)
    bits = list(v[i])
    j = random.randint(0, 2)
    bits[j], bits[j + 1] = bits[j + 1], bits[j]
    v[i] = ''.join(bits)
    return v


def ag_maintenance(pop_size=100, generations=200):
    population = [generer_solution_valide() for _ in range(pop_size)]

    for _ in range(generations):
        selectionnes = selection_roulette(population)
        nouvelle_pop = []

        for i in range(0, pop_size, 2):
            p1 = selectionnes[i]
            p2 = selectionnes[(i + 1) % pop_size]
            e1, e2 = croisement_simple(p1, p2)
            e1 = mutation_transposition_consecutive(e1)
            e2 = mutation_transposition_consecutive(e2)

            if valide(e1): nouvelle_pop.append(e1)
            if valide(e2): nouvelle_pop.append(e2)

        if len(nouvelle_pop) < pop_size:
            nouvelle_pop += [generer_solution_valide() for _ in range(pop_size - len(nouvelle_pop))]

        population = nouvelle_pop[:pop_size]

    meilleure = max(population, key=evaluer_maintenance)
    return meilleure, evaluer_maintenance(meilleure)


if __name__ == "__main__":
    print("=== MAINTENANCE - ALGORITHME GÉNÉTIQUE ===")
    print("- Sélection : Roulette")
    print("- Croisement : Simple (1 point)")
    print("- Mutation : Transposition de deux allèles consécutifs")
    sol, val = ag_maintenance()
    print(f"\nSéquence de maintenance (Unités 1 à 7) :\n{sol}")
    print(f"Réserve minimale (MW)                  : {val}")