README

# csv
Contient les documents csv à prendre en entrée

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

---

### 2. `pre_existing_routes.csv`
- **Description :** Contient 1791 routes aériennes préexistantes.
- **Colonnes :**
  - `ID_start` : Identifiant de l'aéroport de départ.
  - `ID_end` : Identifiant de l'aéroport d'arrivée.

---


### 3. `prices.csv`
- **Description :** Contient le prix des billets pour les 1791 routes aériennes préexistantes.
- **Colonnes :** 
  - `ID_start` : Identifiant de l'aéroport de départ.
  - `ID_end` : Identifiant de l'aéroport d'arrivée.
  - `price_tag` : Le prix du billet 

---

### 4. `waiting_times.csv`
- **Description :** Contient les temps d'attentes pour chaque aéroport.
- **Colonnes :** 
  - `ID` : Identifiant de l'aéroport.
  - `idle_time` : Temps d'attente dans l'aéroport.

---

### 5. `wanted_journeys.csv`
- **Description :** Contient les trajets à réaliser.
- **Colonnes :** 
  - `ID_start` : Identifiant de l'aéroport de départ.
  - `ID_end` : Identifiant de l'aéroport d'arrivée.

---

# output_csv
Contient les documents csv remis en sortie

## Fichiers de Matrice

### 1. `network_graph_adj_matrix_costs.csv`
- **Description :** Matrice d'adjacence représentant les prix des billets des routes aériennes préexistantes.
- **Colonnes :**
  - Chaque colonne et ligne représente un aéroport.
  - Les valeurs indiquent le prix du billet d'avion entre les aéroports correspondants.

---

### 2. `network_graph_adj_matrix.csv`
- **Description :** Matrice d'adjacence représentant les distances entre les routes aériennes préexistantes.
- **Colonnes :**
  - Chaque colonne et ligne représente un aéroport.
  - Les valeurs indiquent la distance entre les aéroports correspondants.

---

### 3. `optimal_trajectory.csv`
- **Description :** Contient les connexions optimisées entre les aéroports après application de l'algorithme de recherche.
- **Colonnes :**
  - `ID_start` : Identifiant de l'aéroport de départ.
  - `ID_end` : Identifiant de l'aéroport d'arrivée.


---

# src
Ce dossier contient tous les documents source du code utilisés dans le fichier principal main.py

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
Ce dossier contient plusieurs fichiers de test permettant de valider les fonctionnalités du projet.

## Tests de l'algorithme de Dijkstra

### 1. `dijkstra_test.py`
- **Description :** Ce fichier teste différentes implémentations de l'algorithme de Dijkstra sur un graphe généré aléatoirement.
- **Fonctions principales :**
  - `generate_graph(num_nodes, prob_edge, num_starts, num_ends_per_start)`: Génère un graphe aléatoire.
  - `dijkstra_tests(num_nodes, prob_edge, num_starts, num_ends_per_start)`: Compare différentes implémentations de Dijkstra et mesure leur performance.
  - Vérifie que les résultats de l'algorithme sont corrects à l'aide d'assertions.

---

## Test sur un échantillon réduit

### 2. `testOnSmallSample.py`
- **Description :** Exécute l'algorithme d'optimisation sur un petit ensemble de données.
- **Fonction principale :**
  - `testOnSmallSample(airports_file, routes_file, airport_to_connect_list, C)`: Charge un petit réseau aérien et exécute l'algorithme de recherche de la trajectoire optimale.
  - Génère un graphe optimisé et affiche la carte mise à jour.

---

## Tests unitaires

### 3. `unittest.py`
- **Description :** Contient des tests unitaires pour valider des fonctionnalités du projet.
- **Fonctions principales :**
  - `distance_test()`: Vérifie le calcul des distances entre plusieurs points géographiques.
  - `dijstra_test()`: Vérifie que l'algorithme de Dijkstra retourne la distance correcte.
  - Affiche un message de validation si tous les tests passent.

---

# comments

code : contains files relative to the parsing of the data and utility functions (distance, dijkstra,...)

csv : contains the csv files about the airports and routes data

tests : contains tests files for various uses

Run : "python main.py" to find the optimal routes to keep

## Formulation mathématique du problème

### Problème de flot à coût minimal

**Objectif :** Acheminer un flux `F` de passagers du nœud source `A_d` vers le nœud puits `A_a`, en minimisant la distance totale parcourue, tout en respectant les capacités des arcs.

**Formulation :**

Minimiser :  
  ∑(u,v) ∈ E   d_uv × f_uv

Sous contraintes :  
  ∑_u f_uv = ∑_w f_vw    pour tout nœud `v` ≠ `A_d`, `A_a`  
  ∑_v f_A_d,v − ∑_u f_u,A_d = F  
  ∑_u f_u,A_a − ∑_v f_A_a,v = F  
  0 ≤ f_uv ≤ c_uv    pour tout (u,v) ∈ E

---

### Définition des variables

- **G = (V, E)** : Graphe orienté des aéroports et trajets.
- **A_d** : Aéroport de départ (source).
- **A_a** : Aéroport d’arrivée (puits).
- **F** : Flux total de passagers à transférer.
- **f_uv** : Nombre de passagers empruntant la liaison de `u` vers `v`.
- **c_uv** : Capacité maximale (passagers/jour) de la liaison `u → v`.
- **d_uv** : Distance (ou coût) associé à la liaison `u → v`.



## Formulation mathématique du problème

### Problème de flot à coût minimal

**Objectif :** acheminer un flux \( F \) de passagers du nœud source \( A_d \) vers le nœud puits \( A_a \), en minimisant la distance totale parcourue tout en respectant les capacités des arcs.

\[
\begin{aligned}
\text{Minimiser} \quad & \sum_{(u,v) \in E} d_{uv} \cdot f_{uv} \\
\text{sous contraintes} \quad 
& \sum_{u} f_{uv} = \sum_{w} f_{vw} \quad \forall v \notin \{A_d, A_a\} \\
& \sum_{v} f_{A_d v} - \sum_{u} f_{u A_d} = F \\
& \sum_{u} f_{u A_a} - \sum_{v} f_{A_a v} = F \\
& 0 \leq f_{uv} \leq c_{uv} \quad \forall (u,v) \in E
\end{aligned}
\]

### Définition des variables

- \( G = (V, E) \) : Graphe orienté des aéroports et trajets.
- \( A_d \) : Aéroport de départ (source).
- \( A_a \) : Aéroport d’arrivée (puits).
- \( F \) : Flux total de passagers à transférer.
- \( f_{uv} \) : Nombre de passagers empruntant la liaison \( u \to v \).
- \( c_{uv} \) : Capacité maximale (passagers/jour) sur la liaison \( u \to v \).
- \( d_{uv} \) : Distance ou coût associé à la liaison \( u \to v \).
