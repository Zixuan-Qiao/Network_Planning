import os
import glob
# import itertools

PATH = ".\\" + "selected_topology" + "\\"

def extract_nodes(file_name):

    nodes = []
    with open(file_name, "r") as f:
        while 1:
            line = f.readline()
            line = line.strip()
            if line == "NODES (":
                break

        counter = 1
        while 1:
            line = f.readline()
            line = line.strip()
            if line[0] == ')':
                break

            node_info = line.split()
            nodes.append({"number": counter, "name": node_info[0]})
            counter += 1

        return nodes


for file_name in glob.glob(os.path.join(PATH, "*.txt")):

    nodes = extract_nodes(file_name)
    default_controller_string = ",\"isController\": False, \"controller\":\"" + nodes[0]["name"]
    new_file_name = file_name[len(PATH): -4] + "_cities.py"

    with open(PATH + new_file_name, "a") as f:

        f.write("list_of_cities = [\n")
        for node in nodes:
            line = "\t" + "{\"name\":\"" + node["name"] + "\",\"city_index\":" + \
                    str(node["number"]) + default_controller_string + "\"},\n"

            f.write(line)

        f.write("]")

