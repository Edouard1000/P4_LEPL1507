import math
import pandas as pd
import networkx as nx
import utility_functions as uf
import dijkstra as dij
import parse as prs

def addlistTofile(list, filename):
    with open(filename, "a") as file:
        file.write(str(list[0]))
        file.write(",")
        file.write(str(list[1]))
        file.write("\n")

def clearFile(filename):
    with open(filename, "w") as file:
        file.write("")

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
        
    

def f(trajectories, network, C, airport_to_connect):
    "prend en argument une liste de boolean qui represente si la trajectoire(dans network) est prise ou non "
    "prend en argument une liste d'ajacence avec les distances ex {0 : [1, 2], 1: [0, 2], 2: [0, 1, 3], 3: [2]}"
    "prend en argument un cout C"
    "prend en argument un dossier de sortie"
    "prend en argument une liste d'aeroport a connecter ex [[0, 2], [1, 3], [2, 3]]"

    "retourne la valeure de f"

    print("\n ############ ")
    print("argument = ")
    print(trajectories)
    print(network)
    print(C)
    print(airport_to_connect)
    print(" ############ \n")


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

    print("\n ############ ")
    print("network = ", network)
    print("starts = ", starts)
    print("ends = ", ends)
    print(" ############ \n")

    MaximMatrix = dij.dijkstra_adj_list(network, starts, ends)[0]
    
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
    "prend en argument une methode : 'only sub', 'Ilias' "

    "retourne la trajectoire optimale (liste de boolean)"

    sizeOfnetwork = 0
    for key in network:
        for _ in network[key]:
            sizeOfnetwork +=1

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

    

    l = translateDicoToList(appliquer_masque(network, trajectory))

    print(l)
    
    clearFile(output_folder + "/optimal_trajectory.txt")
    for el in l:
        addlistTofile(el, output_folder + "/optimal_trajectory.txt")
    print("le fichier à été enregistré à l'adresse : ", output_folder + "/optimal_trajectory.txt")

    return trajectory


def generateNeighMatrix(array):
    neighList = []
    for i in range(len(array)):
        if(array[i] == 1):
            array[i] = 0
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
    def hashArray(array):
        return "".join(map(str, array))
    neighList = []
    visited = {}
    queue = Queue()
    queue.push((array, 0))
    while not queue.empty():
        currentArray, currentDepth = queue.pop()
        for i in range(len(currentArray)):
            if currentArray[i] == 1:
                currentArray[i] = 0
                hash = hashArray(currentArray)
                if hash not in visited:
                    neighList.append(currentArray.copy())
                    visited[hash] = True
                    if currentDepth < depth:
                        queue.push((currentArray, currentDepth + 1))
                currentArray[i] = 1



def Queue():
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






