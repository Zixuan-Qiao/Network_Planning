import random
from parameter_setting import K
from parameter_setting import V
from chromosome_metrics import KMCA, result_interpreter
# from metrics_only_assignment import MOA, result_interpreter

POPULATION_SIZE = 30 # = TOP + MID + LOW
TOP_SIZE = 10
MID_SIZE = 10
LOW_SIZE = 10

ITERATION = 20

def random_placement(size):

    placement_set = set()
    possible_locations = [i for i in range(1, V + 1)]
    while len(placement_set) < size:
        placement_set.add(tuple(random.sample(possible_locations, K)))

    return placement_set

# print(random_placement())

'''
def chromosome_metrics(placement):

    metrics = 0
    for i in range(0, len(placement)):
        metrics += 10**i * placement[i]

    return metrics

# print(chromosome_metrics((9, 1, 1, 1)))
'''

def population_generation(size):

    population = []
    placement_list = list(random_placement(size))
    for i in range(0, size):
        metrics = KMCA(placement_list[i])
        # metrics = MOA(placement_list[i])
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
            metrics = KMCA(mutated)
            # metrics = MOA(mutated)

            crossover_children.append({"placement": mutated, "metrics": metrics})

        random_children = population_generation(LOW_SIZE)

        population = top_p + crossover_children + random_children
        population = population_ranking(population)

    print("Updated population: ", population)
    min_child = population[0]

    return min_child

placement_solution = genetic_algorithm()

print("Placement solution:", placement_solution["placement"])
print("Minimum average delay: ", placement_solution["metrics"])

# GAPA results output
node_assignment = result_interpreter(placement_solution["placement"])

node_count = [0 for i in range(0, K)]
for i in range(0, K):
    node_count[i] = len(node_assignment[i])

print("Node count:", node_count)

print("Node assignment solution:")
print("Controller index\tAssigned nodes")
for i in range(0, K):
    print(i, "\t", node_assignment[i])


'''
# MOP results output
node_count = result_interpreter(placement_solution["placement"])
print(node_count)
'''
