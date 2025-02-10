import math
import pandas as pd
import networkx as nx
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './code')))
import utility_functions as uf
import parse as p

def f(trajectories, airports_file = "./csv/airports.csv", routes_file = "./csv/pre_existing_routes.csv"):
    network_graph = p.parse_airport_data(airports_file, routes_file)
    pass

