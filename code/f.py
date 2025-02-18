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
    "prend en argument une liste de boolean qui represente si la trajectoire(dans network) est prise ou non "
    "prend en argument une liste d'ajacence avec les distances ex {0 : [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2]}"
    "prend en argument un cout C"
    "prend en argument un dossier de sortie"
    "prend en argument une liste d'aeroport a connecter ex [[0, 2], [1, 3], [2, 3]]"

    "retourne la valeure de f"

    N = len(airport_to_connect) # nombre de trajets dans J
    f = 0 # valeur de la fonction objectif
    confortPassager = 0 
    network = appliquer_masque(network, trajectories) # on applique le masque qui supprime les aretes non selectionnees

    starts = [] # liste des aeroports de depart
    ends = {} # dictionnaire des aeroports d'arrivee
    for i in range(0, N): # on remplit les listes starts et ends
        start = airport_to_connect[i][0]
        starts.append(start) # on ajoute l'aeroport de depart
        if(start not in ends): # si l'aeroport n'est pas deja dans le dictionnaire, on l'ajoute
            ends[start] = []
        ends[start].append(airport_to_connect[i][1]) # on ajoute l'aeroport d'arrivee a la liste des aeroports d'arrivee de l'aeroport de depart

    MaximMatrix = dij.dijkstra_adj(network, starts, ends)
    
    for key in ends:
        for el in ends[key]:
            f += MaximMatrix[key][el]
    f /= N
    f += C * sum(trajectories)
    return f

def findOptimalTrajectory(network,C , output_folder, Airport_to_connect_list):
    "prend en argument une liste d'ajacence"
    "prend en argument un cout C"
    "prend en argument un dossier de sortie"
    "prend en argument une liste d'aeroport a connecter"

    "retourne la trajectoire optimale (liste de boolean)"

    current_f_value = f()

    pass 

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






