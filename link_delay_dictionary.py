import math
import os
import glob
from math import sin, cos, acos, radians
# import itertools

PATH = ".\\" + "selected_topology" + "\\"
EARTH_RADIUS = 6371
OPTICAL_SIGNAL_SPEED = 200000


def extract_nodes_and_links(file_name):

    nodes_location = []
    links = []
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
            nodes_location.append({"number": counter, "name": node_info[0],
                                   "longitude": float(node_info[2]), "latitude": float(node_info[3])})
            counter += 1

        while 1:
            line = f.readline()
            line = line.strip()
            if line == "LINKS (":
                break

        while 1:
            line = f.readline()
            line = line.strip()
            if line[0] == ')':
                break

            link_info = line.split()
            links.append([link_info[2], link_info[3]])

        return nodes_location, links


def propagation_delay(node1, node2):
    longitude1 = radians(node1["longitude"])
    latitude1 = radians(node1["latitude"])
    longitude2 = radians(node2["longitude"])
    latitude2 = radians(node2["latitude"])

    part1 = sin(latitude1) * sin(latitude2) * cos(longitude1 - longitude2)
    part2 = cos(latitude1) * cos(latitude2)

    try:
        shortest_path = EARTH_RADIUS * acos(part1 + part2)
    except:
        print(node1, node2)

    propagation_delay = shortest_path / OPTICAL_SIGNAL_SPEED

    return propagation_delay


for file_name in glob.glob(os.path.join(PATH, "*.txt")):

    nodes, links = extract_nodes_and_links(file_name)

    # delay_table = []
    new_file_name = file_name[len(PATH): -4] + "_links.py"

    with open(PATH + new_file_name, "a") as f:

        f.write("list_of_links = [\n")
        for link_nodes in links:

            nodes_info = []
            for node in nodes:
                if node["name"] == link_nodes[0] or node["name"] == link_nodes[1]:
                    nodes_info.append(node)

                if len(nodes_info) >= 2:
                    break

            delay = propagation_delay(nodes_info[0], nodes_info[1])

            line = "\t" + "{\"from\":\"" + nodes_info[0]["name"] + "\", \"to\":\"" + \
                    nodes_info[1]["name"] + "\",\"params\":{\"delay\":\"" + str(delay) + "\"}},\n"

            f.write(line)
        f.write("]")


