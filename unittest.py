
from distance import earth_distance
from dijstra import dijkstra

def distance_test():
    def assertAlmostEqual(a, b, tol=1):
        assert abs(a - b) < tol

    def test_same_point():
        assertAlmostEqual(earth_distance(0, 0, 0, 0), 0)

    def test_known_distance():
        # Distance between Paris and London 
        assertAlmostEqual(earth_distance(48.8566, 2.3522, 51.5074, -0.1278), 343)

    def test_equator_distance():
        # Distance between two points on the equator
        assertAlmostEqual(earth_distance(0, 0, 0, 1), 111.2)

    def test_poles_distance():
        # Distance between the North Pole and the South Pole
        assertAlmostEqual(earth_distance(90, 0, -90, 0), 20003.5)

    test_equator_distance()
    test_poles_distance()
    test_known_distance()
    test_same_point()
    print("All distance tests pass")

def dijstra_test():
    incidence_matrix = [
        [0, 1, 4, 0, 0, 0],
        [0, 0, 4, 2, 7, 0],
        [0, 0, 0, 3, 4, 0],
        [0, 0, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 0]
    ]
    start_node = 0
    end_node = 5
    assert (dijkstra(incidence_matrix, start_node, end_node) == 7) 
    print("All Dijstra tests pass")

print("")
print("##############################################")
print("############## Running tests... ##############")
print("##############################################")

distance_test()
dijstra_test()

print("##############################################")
print("############## All tests pass ! ##############")
print("##############################################")
print("")



