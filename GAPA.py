import random, math
from KMCA_complete import KMCA, result_interpreter
# from metrics_only_assignment import MOA, result_interpreter
import sys, getopt
POPULATION_SIZE = 30 # = TOP + MID + LOW
TOP_SIZE = 10
MID_SIZE = 10
LOW_SIZE = 10

ITERATION = 500
K = 0
V = 0

# by default, this file implements GAPA and KMCA is imported to calculate metric 
# when MOA is utilized to calculate metric, this file implements MOP


def random_placement(size):

    placement_set = set()
    possible_locations = [i for i in range(1, V + 1)]
    while len(placement_set) < size:
        placement_set.add(tuple(random.sample(possible_locations, K)))

    return placement_set


def population_generation(size):

    population = []
    placement_list = list(random_placement(size))
    for i in range(0, size):
        metrics = KMCA(placement_list[i], K, V)
        # metrics = MOA(placement_list[i], K, V)
        population.append({"placement": list(placement_list[i]), "metrics": metrics})

    return population


def population_ranking(population):

    boundry_stack = []
    boundry_stack.append(0)
    boundry_stack.append(POPULATION_SIZE - 1)

    while len(boundry_stack) > 0:
        high = boundry_stack.pop()
        low = boundry_stack.pop()

        if high <= low:
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

    child1 = mother[0:boundry] + father[boundry:]
    child2 = father[0:boundry] + mother[boundry:]

    return child1, child2


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
    log_file.write("Initial population: " + str(population) +"\n")
    summary_file.write("Improve from " + str(population[0]["metrics"])+ " to ")
    for i in range(0, ITERATION):
        top_p = population[0:TOP_SIZE]
        mid_p = population[TOP_SIZE:TOP_SIZE+MID_SIZE]
        low_p = population[TOP_SIZE+MID_SIZE:]

        crossover_children = []
        for j in range(0, MID_SIZE):
            mother = random.sample(top_p, 1)
            father = random.sample(mid_p, 1)

            crossover1, crossover2 = cross_over(mother[0]["placement"], father[0]["placement"])
            mutated1 = mutation(crossover1)
            mutated2 = mutation(crossover2)
            metrics1 = KMCA(mutated1, K, V)
            metrics2 = KMCA(mutated2, K, V)
            # metrics1 = MOA(mutated1, K, V)
            # metrics2 = MOA(mutated2, K, V)

            crossover_children.append({"placement": mutated1, "metrics": metrics1})
            crossover_children.append({"placement": mutated2, "metrics": metrics2})
        random_children = population_generation(LOW_SIZE)

        population = top_p + crossover_children + random_children
        population = population_ranking(population)
        log_file.write("iteration " + str(i) + ": " + str(population) +"\n")

    log_file.write("Updated population: " +str(population) +"\n")
    min_child = population[0]
    log_file.write("min: " +str(population[0])+ "\n")
    summary_file.write(str(population[0]["metrics"]) + "\n")
    return min_child

if __name__ == '__main__':
    log_file_name = "output"
    summary_file_name = "summary_output"
    opts, args = getopt.getopt(sys.argv[1:],"hk:v:o:s:",["controllers=","forwarding_devices=","output=","summary="])
    for opt,arg in opts:
        if opt == "-h":
            print("Run this with --controllers=<K> --forwarding_devices=<V> --output=<name_of_output_file>")
            exit()
        elif opt in ("-k", "--controllers"):
            K = int(arg)
        elif opt in ("-v", "--forwarding_devices"):
            V = int(arg)
        elif opt in ("-o", "--output"):
            log_file_name = arg
        elif opt in ("-s", "--summary"):
            summary_file_name = arg
    log_file = open(log_file_name, 'w')
    summary_file = open(summary_file_name, 'w')

    BALANCE_ARRAY = [math.ceil(V/K)] * K
	
    placement_solution = genetic_algorithm()
    
    print("Placement solution:", placement_solution["placement"])
    print("Minimum average delay: ", placement_solution["metrics"])

    # GAPA results output begin
    # this section needs to be commented when switching to MOP
    node_assignment = result_interpreter(placement_solution["placement"], K, V)

    node_count = [0 for i in range(0, K)]
    for i in range(0, K):
        node_count[i] = len(node_assignment[i])

    print("Node count:", node_count)

    print("Node assignment solution:")
    print("Controller index\tAssigned nodes")
    for i in range(0, K):
        print(i, "\t", node_assignment[i])
    # GAPA results output end

    summary_file.close()   
    log_file.close()


# MOP results output begin
# this section needs to be commented when switching to GAPA
'''
node_count = result_interpreter(placement_solution["placement"], K, V)
print(node_count)
'''
# MOP results output end

