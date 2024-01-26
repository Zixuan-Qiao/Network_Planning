import os
import glob
# import itertools

PATH = ".\\" + "delay_tables" + "\\"

new_file_name = PATH + "omega_matrices.py"

def delay_extract_and_store(file_name, V):

    omega = [[0 for j in range(0, V)] for i in range(0, V)]
    with open(file_name, "r") as f:

        line = f.readline()
        while 1:
            line = f.readline()
            if not line:
                break

            line = line.strip()
            line_components = line.split(",")
            omega[int(line_components[1]) - 1][int(line_components[3]) - 1] = float(line_components[4])
            omega[int(line_components[3]) - 1][int(line_components[1]) - 1] = float(line_components[4])

    with open(new_file_name, "a") as f:

        f.write("omega_" + str(V) + " = [\n")
        for i in range(0, V):
            f.write(str(omega[i]) + ",\n")
        f.write("]\n")
        f.write("\n")


file_name = PATH + input("File name: ")
V = int(input("Number of cities: "))

delay_extract_and_store(file_name, V)