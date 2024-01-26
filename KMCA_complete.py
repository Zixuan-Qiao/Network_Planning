import numpy as np
from omega_matrices import omega_50
from omega_matrices import omega_35
from omega_matrices import omega_65
from scipy.optimize import linear_sum_assignment
import math
# all algorithms import these settings from one file

# operations are row based,
# the result will be transposed at the end
def weight_matrix_generation(placement, K, V):
    BALANCE_ARRAY = [math.ceil(V/K)] * K
	
    if V == 50:
        delay_matrix = omega_50
    elif V == 35:
        delay_matrix = omega_35
    else:
        delay_matrix = omega_65

    metric =[]
    for i in range(0, K):
        metric.append(delay_matrix[placement[i] - 1])


    weight_matrix = []
    for i in range(0, K):
        for j in range(0, BALANCE_ARRAY[i]):
            weight_matrix.append(metric[i])

    weight_matrix = [[row[i] for row in weight_matrix] for i in range(0, len(weight_matrix[0]))]

    if len(weight_matrix) < len(weight_matrix[0]):

        difference = len(weight_matrix[0]) - len(weight_matrix)
        for i in range(0, difference):
            weight_matrix.append([0 for j in range(0, len(weight_matrix[0]))])

    return weight_matrix

# KM algorithm implemented by SciPy
'''-----Idea contributed by group member: John Bousfield-----'''
def Kuhn_Munkres(weight, V):

    np_weight = np.array(weight)
    row_index, col_index = linear_sum_assignment(weight)

    min_val = np_weight[row_index, col_index].sum()
    M = min_val / V

    return M
'''------------------------ END ------------------------------'''

# metrics version: only return value
def KMCA(placement, K, V):

    weight = weight_matrix_generation(placement, K, V)
    metric =Kuhn_Munkres(weight, V)

    return metric

# full version: return assignment (called for the final result)
def result_interpreter(placement, K, V):
    BALANCE_ARRAY = [math.ceil(V/K)] * K

    weight = weight_matrix_generation(placement, K, V)
    row_index, col_index = linear_sum_assignment(weight)

    sum = 0
    controller_range = []
    node_assignment = []
    for i in range(0, K):
        sum += BALANCE_ARRAY[i]
        controller_range.append(sum)
        node_assignment.append([])

    for i in range(0, V):
        for j in range(0, K):
            if col_index[i] < controller_range[j]:
                node_assignment[j].append(i + 1)
                break

    return node_assignment

