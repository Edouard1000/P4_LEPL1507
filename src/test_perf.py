import new_network as nn
import generate_journeys as gj
import time
import matplotlib.pyplot as plt

def calculateTimeComplexity(n1, n2, time1, time2):
    pass



def plot_gj(num_journeys_start = 1, num_journeys_end = 10, step = 10):
    times = []
    for num_journeys in range(num_journeys_start, num_journeys_end + step, step):
        gj.generate_journeys(num_journeys)
        start_time = time.time()
        nn.new_network("./csv/airports.csv", "./csv/pre_existing_routes.csv", "./csv/wanted_journeys.csv", 1000, True, 42, False, 20, 1000, 0.1, False, 20)
        end_time = time.time()
        times.append(end_time - start_time)

    plt.plot(range(num_journeys_start, num_journeys_end + step, step), times, marker='o')
    plt.xlabel('Number of Journeys')
    plt.ylabel('Execution Time (s)')
    plt.title('Execution Time vs Number of Journeys')
    plt.grid(True)
    plt.show()
        

plot_gj()