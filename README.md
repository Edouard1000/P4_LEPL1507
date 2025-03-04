README

# csv
Contient les documents csv à prendre en entrée

## Fichiers des Aéroports

### 1. `airports.csv`
- **Description :** Contient les informations de 75 aéroports.
- **Colonnes :**
  - `name` : Nom de l'aéroport.
  - `city` : Ville où se situe l'aéroport.
  - `country` : Pays de l'aéroport.
  - `ID` : Identifiant unique de l'aéroport.
  - `extended_ID` : Identifiant étendu.
  - `latitude` : Latitude géographique.
  - `longitude` : Longitude géographique.

### 2. `airports_europe.csv`
- **Description :** Contient les informations de 12 aéroports européens.
- **Colonnes :** Identiques à `airports.csv`.

---

## Fichiers des Routes

### 3. `pre_existing_routes.csv`
- **Description :** Contient 1791 routes aériennes préexistantes.
- **Colonnes :**
  - `ID_start` : Identifiant de l'aéroport de départ.
  - `ID_end` : Identifiant de l'aéroport d'arrivée.

### 4. `pre_existing_routes_europe.csv`
- **Description :** Contient 50 routes aériennes en Europe.
- **Colonnes :** Identiques à `pre_existing_routes.csv`.

---

## Fichiers de Test

### 5. `testFileAirports.csv`
- **Description :** Contient 9 aéroports pour les tests.
- **Colonnes :** Identiques à `airports.csv`.

### 6. `testFilePreExistingRoutes.csv`
- **Description :** Contient 5 routes aériennes pour les tests.
- **Colonnes :** Identiques à `pre_existing_routes.csv`.

---


# output_csv
Contient les documents csv remis en sortie

## Fichiers de Matrice

### 1. `network_graph_adj_matrix.csv`
- **Description :** Matrice d'adjacence représentant les distances entre 12 aéroports dans le réseau.
- **Colonnes :**
  - Chaque colonne et ligne représente un aéroport (indices de 0 à 11).
  - Les valeurs indiquent la distance entre les aéroports correspondants.

---

## Fichiers de Trajectoire Optimale

### 2. `optimal_trajectory.csv`
- **Description :** Contient les connexions optimisées entre les aéroports après application de l'algorithme de recherche.
- **Colonnes :**
  - `ID_start` : Identifiant de l'aéroport de départ.
  - `ID_end` : Identifiant de l'aéroport d'arrivée.
- **Nombre de trajets optimisés :** 3

---

# src

### 1. `airpots_plot.py`
Affiche le réseau des aéroports et des routes aériennes.

- **`plot_airport_network(airports_file, routes_file, title="Airports and Flight Routes")`**
  - *Arguments:*
    - `airports_file (str)`: Chemin vers le fichier CSV contenant les aéroports.
    - `routes_file (str)`: Chemin vers le fichier CSV contenant les routes aériennes.
    - `title (str)`: Titre du graphique.
  - *Retourne:* Affiche une carte interactive du réseau aérien.

### 2. `dijkstra.py`
Implémente l'algorithme de Dijkstra pour la recherche de chemins optimaux.

- **`dijkstra_all_paths(graph, starts, endss)`**
  - *Arguments:*
    - `graph (networkx.Graph)`: Graphe représentant le réseau.
    - `starts (list[int])`: Liste des indices de départ.
    - `endss (list[list[int]])`: Liste des indices d'arrivée.
  - *Retourne:* Un dictionnaire de distances et chemins optimaux.

- **`optimized_dijkstra(graph, starts, endss)`**
  - Implémente une version optimisée de Dijkstra utilisant `networkx`.

### 3. `f.py`
Fichier contenant des fonctions de traitement de données et d'optimisation.

- **`appliquer_masque(dico, masque)`**
  - *Arguments:*
    - `dico (dict)`: Dictionnaire représentant les relations.
    - `masque (list)`: Liste de booléens appliquant un filtre.
  - *Retourne:* Un dictionnaire filtré.

- **`f(trajectories, network, C, airport_to_connect)`**
  - Fonction de calcul d'une métrique d'optimisation.

- **`findOptimalTrajectory(network, C, output_folder, airport_to_connect_list)`**
  - Recherche la meilleure trajectoire dans un réseau donné.

### 4. `genetics.py`
Implémente un algorithme génétique pour optimiser le réseau aérien.

- **`evaluate_fitness(graph, E, J, C)`**
  - Évalue la qualité d'un individu dans l'algorithme génétique.

- **`genetic_algorithm(P, J, C, population_size=50, generations=100, mutation_rate=0.1)`**
  - Exécute l'algorithme génétique sur un ensemble de connexions possibles.

### 5. `graphic_interface.py`
Interface graphique utilisant Dash pour visualiser les routes aériennes.

- **`update_best_route(start, end)`**
  - Met à jour l'affichage des meilleures routes entre deux aéroports.

### 6. `main.py`
Fichier principal exécutant l'analyse du réseau aérien.

- **`main()`**
  - Exécute la logique principale du projet en appelant les autres modules.

### 7. `parse.py`
Parse les fichiers CSV pour générer un graphe de réseau aérien.

- **`parse_airport_data(airports_file, routes_file)`**
  - *Arguments:*
    - `airports_file (str)`: Fichier contenant les aéroports.
    - `routes_file (str)`: Fichier contenant les routes aériennes.
  - *Retourne:* Un graphe de type `networkx.Graph` et un dictionnaire d'indexation.

### 8. `utility_functions.py`
Contient des fonctions utilitaires, notamment pour le calcul des distances.

- **`euclidean_distance(x, y)`**
  - Calcule la distance euclidienne entre deux points géographiques.

- **`earth_distance(lat1, lon1, lat2, lon2)`**
  - Calcule la distance terrestre entre deux points en utilisant la géodésie.


# tests

---

# comments

code : contains files relative to the parsing of the data and utility functions (distance, dijkstra,...)

csv : contains the csv files about the airports and routes data

tests : contains tests files for various uses

Run : "python main.py" to find the optimal routes to keep