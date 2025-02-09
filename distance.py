import math
from geographiclib.geodesic import Geodesic

geod = Geodesic.WGS84

def earth_distance(lat1, lon1, lat2, lon2):
    g = geod.Inverse(lat1, lon1, lat2, lon2)
    return g['s12'] / 1000  # Conversion de la distance en kilomètres