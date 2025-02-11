import math
import pandas as pd
import networkx as nx
import utility_functions as uf
from dijkstra import dijkstra

def mask(array, mask):
    return [a for a, m in zip(array, mask) if m]

#trajectories = [1,1,1,1,1,1,1,1,1,1,...]
def f(trajectories, network,C , output_folder, Airport_to_connect_list):
    
    N = Airport_to_connect_list.length
    f = 0

    # Merge all tuples into a single list
    #Airport_to_connect_list = [(At, [Al1,Al2]), (A3, A4), ...]

    merged_list = [item for sublist in Airport_to_connect_list for item in sublist]
    MaximMatrix = dijkstra(network, merged_list[0], merged_list[1])

    for At, Al in Airport_to_connect_list:
        f += MaximMatrix[At][Al]

    f = f*1/N + C * sum(trajectories)
    return f

def generateNeighMatrix(array):
    neighList = []
    for i in range(len(array)):
        if(array[i] == 1):
            array[i] = 0
            neighList.append(array.copy())
            array[i] = 1
    return neighList

def findOptimalTrajectory(network,C , output_folder, Airport_to_connect_list):
    current_trajectories = [1] * network.edges.length
    current_f = f(current_trajectories, network,C , output_folder, Airport_to_connect_list)
    while(True):
        updated = False
        for trajectories in generateNeighMatrix(current_trajectories):
            new_f = f(trajectories, network,C , output_folder, Airport_to_connect_list)
            if(new_f < current_f):
                current_f = new_f
                current_trajectories = trajectories
                updated = True
        if(not updated):
            break
    return current_trajectories
        


#print(generateNeighMatrix([1,0,1,1,1,1,1,1,1,1]))






