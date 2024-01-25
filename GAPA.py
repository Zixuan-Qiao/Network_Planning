import random

K = 4 # controller number
V = 10 # location number

POPULATION_SIZE = 60 # = TOP + MID + LOW
TOP_SIZE = 20
MID_SIZE = 20
LOW_SIZE = 20

ITERATION = 20

def random_placement(size):

    placement_set = set()
    possible_locations = [i for i in range(1, V + 1)]
    while len(placement_set) < size:
        placement_set.add(tuple(random.sample(possible_locations, K)))

    return placement_set

def chromosome_metrics(placement):

    metrics = 0
    for i in range(0, len(placement)):
        metrics += 10**i * placement[i]

    return metrics

def population_generation(size):

    population = []
    placement_list = list(random_placement(size))
    for i in range(0, size):
        metrics = chromosome_metrics(placement_list[i])
        population.append({"placement": list(placement_list[i]), "metrics": metrics})

    return population

def population_ranking(population):

    boundry_stack = []
    boundry_stack.append(0)
    boundry_stack.append(POPULATION_SIZE - 1)

    while len(boundry_stack) > 0:
        high = boundry_stack.pop()
        low = boundry_stack.pop()

        if high <= low: # the current sub-array only contain 1 item or is empty
            continue

        base = population[low]

        i = low
        j = high
        while j > i:
            if population[j]["metrics"] < base["metrics"]:
                while i < j:
                    if population[i]["metrics"] > base["metrics"]:
                        temp = population[j]
                        population[j] = population[i]
                        population[i] = temp
                        break
                    i += 1

            if i == j:
                break

            j -= 1

        temp = population[j]
        population[j] = base
        population[low] = temp

        boundry_stack.extend([low, j - 1, j + 1, high])

    return population

def cross_over(mother, father):

    if K % 2 != 0:
        boundry = int((K + 1) / 2)
    else:
        boundry = int(K / 2)

    child = mother[0:boundry] + father[boundry:]

    return child


def mutation(crossover):

    swap1 = random.randint(0, K - 1)
    swap2 = random.randint(0, K - 1)

    temp = crossover[swap1]
    crossover[swap1] = crossover[swap2]
    crossover[swap2] = temp

    while 1:
        new_location = random.randint(1, V)
        if new_location not in crossover:
            i = random.randint(0, K - 1)
            crossover[i] = new_location
            break

    return crossover

def genetic_algorithm():

    population = population_generation(POPULATION_SIZE)
    population = population_ranking(population)
    print("Initial population: ", population)

    for i in range(0, ITERATION):
        top_p = population[0:TOP_SIZE]
        mid_p = population[TOP_SIZE:TOP_SIZE+MID_SIZE]
        low_p = population[TOP_SIZE+MID_SIZE:]

        crossover_children = []
        for j in range(0, MID_SIZE):
            mother = random.sample(top_p, 1)
            father = random.sample(mid_p, 1)

            crossover = cross_over(mother[0]["placement"], father[0]["placement"])
            mutated = mutation(crossover)
            metrics = chromosome_metrics(mutated)

            crossover_children.append({"placement": mutated, "metrics": metrics})

        random_children = population_generation(LOW_SIZE)

        population = top_p + crossover_children + random_children
        population = population_ranking(population)

    print("Updated population: ", population)
    min_child = population[0]

    return min_child

print(genetic_algorithm())



