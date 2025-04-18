## Structure du Projet
---

```bash                     
├── csv/                       
│ ├── airports.csv            
│ └── capacities_airports.csv 
├── output_csv/    
│ ├── network_graph_adj_matrix.csv            
│ └── network_graph_adj_matrix.csv 
│ ├── optimal_trajectory.csv                               
├── src/                 
│ ├── analyse/
│ │ └── assets/
│ │   └── ...                   # Emoticones pour l'interface graphique
│ ├── airpots_plot.py
│ ├── dijkstra.py
│ ├── generate_journeys.py      # Generation de parcours (J)
│ ├── genetics.py
│ ├── graphic_interface.py
│ ├── main.py
│ ├── new_network.py            # Description du projet (ce fichier)
│ └── parse.py
├── .gitignore   
└── README.md                   # Fichier de configuration Git

```

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

### 3. `genetics.py`
Implémente un algorithme génétique pour optimiser le réseau aérien.

- **`evaluate_fitness(graph, E, J, C)`**
  - Évalue la qualité d'un individu dans l'algorithme génétique.

- **`genetic_algorithm(P, J, C, population_size=50, generations=100, mutation_rate=0.1)`**
  - Exécute l'algorithme génétique sur un ensemble de connexions possibles.

### 4. `graphic_interface.py`
Interface graphique utilisant Dash pour visualiser les routes aériennes.

- **`update_best_route(start, end)`**
  - Met à jour l'affichage des meilleures routes entre deux aéroports.

### 5. `main.py`
- **Description :** Exécute le pipeline : chargement données, optimisation génétique, export matrices, visualisation, interface utilisateur.
- **Fonctions principales :**
  1. **`main()`** : Orchestre le pipeline (chargement CSV, parsing, matrices adjacence, temps d'escale, `compute_genetics()`, export optimal, affichage réseau, reconstruction matrices optimisées, `graphic_interface()`).
  2. **`compute_genetics(C, random_seed=42, population_size=1000, generations=200, mutation_rate=0.1, network_graph=None, id_to_index=None, wanted_journeys_csv=None)`** : Lance l'algorithme génétique. Retourne `optimal_trajectory`, `evolution`.


### 6. `parse.py`
- **Description :** Parse les CSV et génère les graphes.
- **Fonctions principales :**
  - **`parse_airport_data(airports_file, routes_file)`** : Crée un graphe de distances.
  - **`parse_cost(costs_file, network_graph, id_to_index)`** : Ajoute les coûts au graphe.
  - **`parse_flow_network(airports_file, routes_file, airport_caps_file, connection_caps_file)`** : Crée un graphe de flux avec capacités et distances pour un objectif secondaire.
  - **`indexToId(index)`** : Convertit un index de nœud en ID d'aéroport.

### 7. `objective2_a.py`
- **Description :** Implémente une fonction pour optimiser le flux de passagers en utilisant l'algorithme de flot à coût minimal de NetworkX.
- **Fonction principale :**
  - **`optimize_flow(G, id_to_index, source_code, target_code, F)`** : Résout le problème de flot à coût minimal pour acheminer un flux `F` d'un aéroport source à un aéroport cible. Affiche le cheminement du flux et la distance moyenne parcourue.
    - `G`: Graphe du réseau.
    - `id_to_index`: Mapping des ID d'aéroports vers leurs index.
    - `source_code`: ID de l'aéroport de départ.
    - `target_code`: ID de l'aéroport d'arrivée.
    - `F`: Flux de passagers à transporter.
### 8. `utility_functions.py`
Contient des fonctions utilitaires, notamment pour le calcul des distances.

  - **`euclidean_distance(lat1, lon1, lat2, lon2)`** : Calcule la distance euclidienne approximative entre deux points GPS.
  - **`earth_distance(lat1, lon1, lat2, lon2)`** : Calcule la distance terrestre précise entre deux points GPS en kilomètres.
  - **`dist_to_time(distance_km, cruise_speed_kmh=900, extra_time=0.75)`** : Convertit une distance en temps de vol estimé (en heures), incluant le temps de croisière et un temps additionnel pour le décollage et l'atterrissage.
  - **`distance(A1, A2, graph)`** : Récupère et calcule la distance terrestre entre deux nœuds d'un graphe en utilisant leurs coordonnées GPS.


# tests
Ce dossier contient plusieurs fichiers de test permettant de valider les fonctionnalités du projet.

## Tests de l'algorithme de Dijkstra

### 1. `dijkstra_test.py`
- **Description :** Ce fichier teste différentes implémentations de l'algorithme de Dijkstra sur un graphe généré aléatoirement.
- **Fonctions principales :**
  - `generate_graph(num_nodes, prob_edge, num_starts, num_ends_per_start)`: Génère un graphe aléatoire.
  - `dijkstra_tests(num_nodes, prob_edge, num_starts, num_ends_per_start)`: Compare différentes implémentations de Dijkstra et mesure leur performance.
  - Vérifie que les résultats de l'algorithme sont corrects à l'aide d'assertions.


## Tests unitaires

### 2. `unittest.py`
- **Description :** Contient des tests unitaires pour valider des fonctionnalités du projet.
- **Fonctions principales :**
  - `distance_test()`: Vérifie le calcul des distances entre plusieurs points géographiques.
  - `dijstra_test()`: Vérifie que l'algorithme de Dijkstra retourne la distance correcte.
  - Affiche un message de validation si tous les tests passent.

---
## Compilation
Le projet est composé de 2 fichiers principaux :
- **main.py :** 
  ```bash
  python main.py
  ```
- **graphic_interface.py :** 
  ```bash
  python graphic_interface.py
  ```