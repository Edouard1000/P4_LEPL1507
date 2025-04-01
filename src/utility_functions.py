import math
import pandas as pd
import networkx as nx
import math
import heapq
from geographiclib.geodesic import Geodesic

geod = Geodesic.WGS84
RAYON_TERRESTRE = 6371.009

# Calcul distance entre deux points GPS
# Pre : x et y sont des listes ou tuples de coordonées gps en degrés (float)
def euclidean_distance(lat1, lon1, lat2, lon2):
    # Conversion des degrés en radians
    #lat1 = math.radians(x[0])
    #lon1 = math.radians(x[1])
    #lat2 = math.radians(y[0])
    #lon2 = math.radians(y[1])


    # Phi et Lambda représentent respectivement la latitude et la longitude en radians
    delta_phi = lat2 - lat1
    delta_lambda = lon2 - lon1

    # Calcul de la distance avec la formule de Haversine
    c = (math.sin(delta_phi/2) * math.sin(delta_phi/2) + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lambda/2) * math.sin(delta_lambda/2))
    d = 2 * math.atan2(math.sqrt(c), math.sqrt(1-c))
    return RAYON_TERRESTRE * d

def earth_distance(lat1, lon1, lat2, lon2): #à pas utiliser 
    g = geod.Inverse(lat1, lon1, lat2, lon2)
    return g['s12'] / 1000  # Conversion de la distance en kilomètres

def dist_to_time(distance_km, cruise_speed_kmh=900, extra_time=0.75):
    """
    Convert flight distance to estimated travel time.

    Parameters:
    - distance_km (float): Distance between two airports in kilometers.
    - cruise_speed_kmh (float): Speed of the aircraft in km/h (default 900 km/h).
    - extra_time (float): Additional time for takeoff and landing in hours (default 45 min -> 0.75 h).

    Returns:
    - float: Estimated flight duration in hours.
    """
    if distance_km <= 0:
        return 0  # No travel if distance is zero or invalid

    cruise_time = distance_km / cruise_speed_kmh 
    total_time = cruise_time + extra_time 
    return total_time

def distance(A1, A2, graph):
    lat1 = graph.nodes[A1]['latitude']
    lon1 = graph.nodes[A1]['longitude']
    lat2 = graph.nodes[A2]['latitude']
    lon2 = graph.nodes[A2]['longitude']
    return earth_distance(lat1, lon1, lat2, lon2)

