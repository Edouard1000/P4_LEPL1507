import math
import pandas as pd
import networkx as nx
import utility_functions as uf
import dijkstra as dij

def appliquer_masque(dico, masque):
    indices_valides = {i for i, v in enumerate(masque) if v == 1}
    print(indices_valides)
    new_dico = {}
    
    current_indices = 0

    for key in dico:
        for el in dico[key]:
            if current_indices in indices_valides :
                if(key not in new_dico):
                    new_dico[key] = []
                new_dico[key].append(el)
            current_indices += 1
              
    return new_dico
        
    

def f(trajectories, network, C, airport_to_connect):
    "prend en argument une liste de bollean qui represente si la trajectoire(dans network) est prise ou non "
    "prend en argument une liste d'ajacence avec les distances ex {0 : [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2]}"
    "prend en argument un cout C"
    "prend en argument un dossier de sortie"
    "prend en argument une liste d'aeroport a connecter ex [[0, 2], [1, 3], [2, 3]]"

    "retourne la valeure de f"

    N = len(airport_to_connect)
    f = 0
    network = appliquer_masque(network, trajectories)

    starts = []
    ends = {}
    for i in range(0, len(airport_to_connect)):
        start = airport_to_connect[i][0]
        starts.append(start)
        if(start not in ends):
            ends[start] = []
        ends[start].append(airport_to_connect[i][1])

    MaximMatrix = dij.dijkstra_adj(network, starts, ends)
    
    for key in ends:
        for el in ends[key]:
            f += MaximMatrix[key][el]
    f /= N
    f += C * sum(trajectories)
    return f

def findOptimalTrajectory(network,C , output_folder, airport_to_connect_list):
    "prend en argument une liste d'ajacence"
    "prend en argument un cout C"
    "prend en argument un dossier de sortie"
    "prend en argument une liste d'aeroport a connecter"

    "retourne la trajectoire optimale (liste de boolean)"

    sizeOfnetwork = 0
    for key in network:
        for _ in network[key]:
            SizeOfnetwork +=1

    trajectory = [1 for _ in range(0, sizeOfnetwork)]
    current_f_value = f(trajectory, network, C, airport_to_connect_list)
    
    update = True
    while(update):
        update = False
        for neigh in generateNeighMatrix(trajectory):
            new_f_value = f(neigh, network, C, airport_to_connect_list)
            if new_f_value < current_f_value:
                current_f_value = new_f_value
                trajectory = neigh
                update = True

    with open(f"{output_folder}/optimal_trajectory.txt", "w") as file:
        file.write(",".join(map(str, trajectory)))

    return trajectory

def generateNeighMatrix(array):
    neighList = []
    for i in range(len(array)):
        if(array[i] == 1):
            array[i] = 0
            neighList.append(array.copy())
            array[i] = 1
    return neighList
    
        


# print(generateNeighMatrix([1,0,1,1,1,1,1,1,1,1]))

dico = {0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2]}
masque = [0, 0, 0, 1, 1, 1, 0, 1]

resultat = appliquer_masque(dico, masque)
print(resultat)  # {1: [2], 2: [0, 1], 3: [2]}






