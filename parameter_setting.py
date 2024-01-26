import math

K = 4
V = 50

CAPACITY_ARRAY = [50, 50, 50, 50]

def get_balance_array():

    capacity_sum = 0
    for i in range(0, K):
        capacity_sum += CAPACITY_ARRAY[i]

    balance_array = []
    for i in range(0, K):
        balance_array.append(math.ceil(CAPACITY_ARRAY[i] * V / capacity_sum))

    return balance_array

BALANCE_ARRAY = get_balance_array()