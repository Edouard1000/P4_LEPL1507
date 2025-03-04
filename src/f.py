import math
import pandas as pd
import networkx as nx
import utility_functions as uf
import dijkstra as dij
import parse as prs
import random

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

def findOptimalTrajectory(network,C , output_folder, airport_to_connect_list):
    "prend en argument une liste d'ajacence"
    "prend en argument un cout C"
    "prend en argument un dossier de sortie"
    "prend en argument une liste d'aeroport a connecter"

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
        for neigh in IlliasgenerateNeighBourhood(trajectory, 1):
            new_f_value = f(neigh, network, C, airport_to_connect_list)
            if new_f_value < current_f_value:
                current_f_value = new_f_value
                trajectory = neigh
                update = True

    
    print("la trajectoire optimale est : ", appliquer_masque(network, trajectory))
    
    l = translateDicoToList(appliquer_masque(network, trajectory))

    print(" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! l =" )
    print(l)
    

    clearFile(output_folder + "/optimal_trajectory.csv")
    for el in l:
        addlistTofile(el, output_folder + "/optimal_trajectory.csv")
    print("le fichier à été enregistré à l'adresse : ", output_folder + "/optimal_trajectory.csv")

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
        for neigh in generateNeighMatrix(currentArray):
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
        


def generateRandomNumber(n):
    return random.randint(0, n)

def generateRandomNeigh(array):
    neigh = array.copy()
    index = generateRandomNumber(len(array) - 1)
    if(neigh[index] == 0):
        neigh[index] = 1
    else:
        neigh[index] = 0
    return neigh


def findOptimalTrajectoryWithHeat(network, C, output_folder, airport_to_connect_list, initial_temperature, cooling_rate):
    "prend en argument une liste d'ajacence"
    "prend en argument un cout C"
    "prend en argument un dossier de sortie"
    "prend en argument une liste d'aeroport a connecter"
    "prend en argument une profondeur de recherche"
    "prend en argument une température initiale"
    "prend en argument un taux de refroidissement"
    
    "retourne la trajectoire optimale (liste de boolean)"

    def acceptance_probability(old_cost, new_cost, temperature):
        if new_cost < old_cost:
            return 1.0
        return math.exp((old_cost - new_cost) / temperature)

    sizeOfnetwork = 0
    for key in network:
        for _ in network[key]:
            sizeOfnetwork += 1

    current_trajectory = [1 for _ in range(sizeOfnetwork)]
    current_f_value = f(current_trajectory, network, C, airport_to_connect_list)
    best_trajectory = current_trajectory
    best_f_value = current_f_value

    temperature = initial_temperature

    while temperature > 1:
        new_trajectory = generateRandomNeigh(current_trajectory)
        new_f_value = f(new_trajectory, network, C, airport_to_connect_list)

        if acceptance_probability(current_f_value, new_f_value, temperature) > random.random():
            current_trajectory = new_trajectory
            current_f_value = new_f_value

        if new_f_value < best_f_value:
            best_trajectory = new_trajectory
            best_f_value = new_f_value

        temperature *= cooling_rate

    return best_trajectory, best_f_value

def findOptimalTrajectoryWithHeatMultipleExecution(network, C, output_folder, airport_to_connect_list, initial_temperature, cooling_rate, numberOfstart):
    best_trajectory = None
    best_f_value = 0
    for i in range(numberOfstart):
        trajectory, f_value = findOptimalTrajectoryWithHeat(network, C, output_folder, airport_to_connect_list, initial_temperature, cooling_rate)
        if(best_trajectory == None or f_value < best_f_value):
            best_trajectory = trajectory
            best_f_value = f_value

    print("la trajectoire optimale est : ", appliquer_masque(network, best_trajectory))
    
    l = translateDicoToList(appliquer_masque(network, best_trajectory))

    print(" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! l =" )
    print(l)
    print("la valeur de f est : ", best_f_value)
    

    clearFile(output_folder + "/optimal_trajectory.csv")
    for el in l:
        addlistTofile(el, output_folder + "/optimal_trajectory.csv")
    print("le fichier à été enregistré à l'adresse : ", output_folder + "/optimal_trajectory.csv")

    return best_trajectory


