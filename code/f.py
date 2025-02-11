import math
import pandas as pd
import networkx as nx
import utility_functions as uf

def mask(matrix, mask):
    masked_matrix = []
    for row, mask_row in zip(matrix, mask):
        masked_row = [val if m else float('inf') for val, m in zip(row, mask_row)]
        masked_matrix.append(masked_row)
    return masked_matrix

#trajectories = [1,1,1,1,1,1,1,1,1,1,...]
def f(trajectories, network,C , output_folder, Airport_to_connect_list_indext):
    
    N = Airport_to_connect_list_indext.length
    f = 0

    start = range(0, network.nodes.length)
    end = range(0, network.nodes.length)

    trajectoriesMatrix = []
    for i in range(0, network.nodes.length):
        for j in range (0, network.nodes.length):
            trajectoriesMatrix.append(trajectories[i*network.nodes.length + j])

    adjacence_matrix = mask(network.adjacence_matrix, trajectoriesMatrix)
    maxMat = uf.MaximMatrix(adjacence_matrix, start, end)

    for At ,Al in Airport_to_connect_list_indext:
        f = f + maxMat[At][Al]  

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






