from omega_matrices import omega_65


def MOA(placement, K, V):

    metric = []
    for i in range(0, K):
        metric.append(omega_65[placement[i] - 1])

    metric = [[row[i] for row in metric] for i in range(0, len(metric[0]))]

    delay_sum = 0
    for i in range(0, V):
        delay_sum += min(metric[i])

    average_delay = delay_sum / V

    return average_delay

def result_interpreter(placement, K, V):

    metric = []
    for i in range(0, K):
        metric.append(omega_65[placement[i] - 1])

    metric = [[row[i] for row in metric] for i in range(0, len(metric[0]))]

    controller_utilization = [0 for i in range(0, K)]
    for i in range(0, V):
        controller_utilization[metric[i].index(min(metric[i]))] += 1

    return controller_utilization
