import math
import pandas as pd
import networkx as nx
import utility_functions as uf
import dijkstra as dij
import parse as prs
import random
import numpy as np

def addlistTofile(list, filename):
    with open(filename, "a") as file:
        file.write(str(list[0]))
        file.write(",")
        file.write(str(list[1]))
        file.write("\n")

def clearFile(filename):
    with open(filename, "w") as file:
        file.write("ID_start,ID_end\n")
    


def appliquer_masque(dico, masque):
    indices_valides = {i for i, v in enumerate(masque) if v == 1}
    # print(indices_valides)
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

def translateDicoToList(dico):
    list = []
    for key in dico:
        for el in dico[key]:
            list.append([prs.indexToId(key),prs.indexToId(el)])
    return list
        
    

def f(trajectories, network, C, airport_to_connect, fast = False, trajectories_pre = [], distances = [],paths = []):
    "prend en argument une liste de boolean qui represente si la trajectoire (dans network) est prise ou non / ex [1, 0, 1, 1, 0]"
    "prend en argument un dictionnaire d'ajacence / ex {0 : [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2]}"
    "prend en argument un cout C"
    "prend en argument une liste J de doublets d'aeroports a connecter / ex [[0, 2], [1, 3], [2, 3]]"

    "retourne la valeur de f"

    '''
    fast : ne calculer dijkstra que pour les doublets modifiés dans J contenant des aretes supprimées u,v 
    1. on recupere les aretes supprimées a l'aide de trajectories_pre et trajectories
    2. on recupère les doublets modifiés dans J 
    3. on recalcule dijkstra pour les aretes modifiées
    4. on calcule f
    '''

    if fast:
        # on recupere les aretes supprimées
        A = np.array(trajectories)
        B = np.array(trajectories_pre)
        modified_trajectories = A - B
        modified_network = appliquer_masque(network, modified_trajectories)
        u = modified_network.keys()[0] # on recupere un sommet du graphe
        v = modified_network.get(u)[0] # on recupere un voisin de u

        # on recupere les doublets modifiés dans J
        for doublet in airport_to_connect : # on parcourt les doublets
            if u == doublet[0] : # si u est le départ
                if v == paths[u][0] : # si v est le suivant
                    # on recalcule dijkstra pour les aretes modifiées
                paths[doublet[0]][doublet[1]]
            
        


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

    # print("starts = ", starts)
    # print("ends = ", ends)
    # print("network = ", network)

    MaximMatrix = dij.dijkstra_adj_list(network, starts, ends)[0]
    
    for key in ends:
        for el in ends[key]:
            f += MaximMatrix[key][el]
    f /= N
    f += C * sum(trajectories)

    print("f = ", f)
    return f

def findOptimalTrajectory(network, C, output_folder, airport_to_connect_list):
    "prend en argument un dictionnaire d'adjacence"
    "prend en argument un cout C"
    "prend en argument un dossier de sortie"
    "prend en argument une liste d'aeroports a connecter"
    "prend en argument une methode : 'only sub', 'Ilias' "

    "retourne la trajectoire optimale (liste de boolean)"
    
    # on recupere le nombre d'aretes dans le reseau 
    sizeOfnetwork = 0
    for key in network:
        for _ in network[key]:
            sizeOfnetwork +=1

    trajectory = [1 for _ in range(0, sizeOfnetwork)] # on initialise la trajectoire avec toutes les aretes selectionnees
    current_f_value = f(trajectory, network, C, airport_to_connect_list) # on calcule la valeur de f pour la trajectoire initiale
    update = True # on initialise la variable update a True pour entrer dans la boucle while
    while(update): # tant qu'on a une mise a jour de la trajectoire
        update = False # on initialise update a False
        for neigh in generateNeighBourhood(trajectory, 1): # on genere les voisins de la trajectoire actuelle avec une profondeur de 1 
            new_f_value = f(neigh, network, C, airport_to_connect_list)
            if new_f_value < current_f_value:
                current_f_value = new_f_value
                trajectory = neigh
                update = True

    
    print("la trajectoire optimale est : ", appliquer_masque(network, trajectory))
    
    l = translateDicoToList(appliquer_masque(network, trajectory))

    print(l)
    

    clearFile(output_folder + "/optimal_trajectory.csv")
    for el in l:
        addlistTofile(el, output_folder + "/optimal_trajectory.csv")
    print("le fichier à été enregistré à l'adresse : ", output_folder + "/optimal_trajectory.csv")

    return trajectory


def generateNeighMatrix(array): 
    '''
    array : liste de boolean ex : [1, 0, 1, 1, 0]
    retourne la liste des voisins de la trajectoire actuelle
    '''
    neighList = [] # on initialise la liste des voisins
    for i in range(len(array)): # pour chaque arete de la trajectoire
        if(array[i] == 1): # si l'arete est selectionnee
            array[i] = 0 # on la deselectionne
            neighList.append(array.copy()) 
            array[i] = 1
    return neighList

def IliasgenerateNeighMatrix(array):
    neighList = []
    for i in range(len(array)):
        if(array[i] == 1):
            array[i] = 0
            neighList.append(array.copy())
            array[i] = 1
        if(array[i] == 0):
            array[i] = 1
            neighList.append(array.copy())
            array[i] = 0
    return neighList


def generateNeighBourhood(array, depth): 
    # on genere les voisins de la trajectoire actuelle
    '''
    array : liste de boolean ex : [1, 0, 1, 1, 0]
    depth : profondeur de recherche des voisins ex : 1

    retourne la liste des voisins de la trajectoire actuelle ex : [[1, 0, 1, 1, 0], [1, 1, 1, 1, 0], [1, 0, 1, 1, 1], [1, 0, 1, 0, 0], [1, 0, 1, 0, 1]]
    '''

    def hashArray(array): # on hash la liste de boolean pour pouvoir la comparer
        return "".join(map(str, array)) # on convertit la liste en chaine de caracteres ex: [1, 0, 1, 1, 0] -> "10110"
    neighList = [] # on initialise la liste des voisins
    visited = {} # on initialise le dictionnaire des noeuds visites
    queue = Queue() # on initialise la file pour parcourir les noeuds 
    queue.push((array, 0)) # on ajoute la trajectoire actuelle a la file
    while not queue.empty(): # tant que la file n'est pas vide
        currentArray, currentDepth = queue.pop() # on recupere le noeud actuel et sa profondeur
        for neigh in generateNeighMatrix(currentArray): # on genere les voisins du noeud actuel
            if hashArray(neigh) not in visited:
                visited[hashArray(neigh)] = []
                visited[hashArray(neigh)].append(neigh)
                neighList.append(neigh)
                if currentDepth < depth:
                    queue.push((neigh, currentDepth + 1))
            if hashArray(neigh) in visited and (neigh not in visited[hashArray(neigh)]):
                visited[hashArray(neigh)].append(neigh)
                neighList.append(neigh)
                if currentDepth < depth:
                    queue.push((neigh, currentDepth + 1))
    return neighList

def IlliasgenerateNeighBourhood(array, depth):
    def hashArray(array):
        return "".join(map(str, array))
    neighList = []
    visited = {}
    queue = Queue()
    queue.push((array, 0))
    while not queue.empty():
        currentArray, currentDepth = queue.pop()
        for neigh in IliasgenerateNeighMatrix(currentArray):
            if hashArray(neigh) not in visited:
                visited[hashArray(neigh)] = []
                visited[hashArray(neigh)].append(neigh)
                neighList.append(neigh)
                if currentDepth < depth:
                    queue.push((neigh, currentDepth + 1))
            if hashArray(neigh) in visited and (neigh not in visited[hashArray(neigh)]):
                visited[hashArray(neigh)].append(neigh)
                neighList.append(neigh)
                if currentDepth < depth:
                    queue.push((neigh, currentDepth + 1))
    return neighList




class Queue:
    def __init__(self):
        self.queue = []
    def push(self, element):
        self.queue.append(element)
    def pop(self):
        return self.queue.pop(0)
    def empty(self):
        return len(self.queue) == 0
        


# print(generateNeighMatrix([1,0,1,1,1,1,1,1,1,1]))

# dico = {0: [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2]}
# masque = [0, 0, 0, 1, 1, 1, 0, 1]

# resultat = appliquer_masque(dico, masque)
# print(resultat)  # {1: [2], 2: [0, 1], 3: [2]}

def findOptimalTrajectoryOptimised(network,C , output_folder, airport_to_connect_list, depth):
    "prend en argument une liste"
    "prend en argument un cout C"
    "prend en argument un dossier de sortie"
    "prend en argument une liste d'aeroport a connecter"
    "prend en argument une profondeur de recherche"
    "prend en argument la profondeur de recherche"
    
    "retourne la trajectoire optimale (liste de boolean)"

    return 0;





