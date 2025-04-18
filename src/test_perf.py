import new_network as nn
import generate_journeys as gj
import time
import matplotlib.pyplot as plt
import math as m
import random
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from itertools import product
from sklearn.linear_model import LinearRegression

def dumbLoop(n):
    for i in range(n):
        for j in range(n):
            pass  # Simulate some work

def mean(list):
    if len(list) == 0:
        return 0
    return sum(list) / len(list)

def varience(list):
    if len(list) == 0:
        return 0
    mean_value = mean(list)
    variance = sum((x - mean_value) ** 2 for x in list) / len(list)
    return variance



def test_time_complexity():
    n1 = 1000
    n2 = 10000

    time1 = time.time()
    dumbLoop(n1)
    time1 = time.time() - time1
    print("Time for n1:", time1)

    time2 = time.time()
    dumbLoop(n2)
    time2 = time.time() - time2
    print("Time for n2:", time2)

    exponent = EstimateTimeComplexity(n1, n2, time1, time2)
    print(f"Estimated exponent for the time complexity: {exponent}")

def EstimateTimeComplexity(n1, n2, time1, time2):
    if time1 == 0 or time2 == 0:
        return -1
    exponent = m.log(time2 / time1) / m.log(n2 / n1)
    return exponent

def test_study_time_complexity():
    n_list = [100, 1000, 10000, 2003, 1244, 14441, 1234, 12345, 12346, 12129]
    t_list = []
    for n in n_list:
        start_time = time.time()
        dumbLoop(n)
        end_time = time.time()
        t_list.append(end_time - start_time)

    print("t_list:", t_list)

    studyTimeComplexity(n_list, t_list)

def studyTimeComplexity(n_list, t_list, number_of_bars=10, number_of_estimators=100, withPlot=True):
    if len(n_list) != len(t_list):
        raise ValueError("n_list and t_list must have the same length")
    if len(n_list) < 2:
        raise ValueError("n_list must have at least two elements")
    if len(n_list) % 2 != 0:
        raise ValueError("n_list must have an even number of elements")

    estimators = []
    for _ in range(number_of_estimators):
        # Randomly select two distinct indices
        indices = random.sample(range(len(n_list)), 2)
        n1, n2 = n_list[indices[0]], n_list[indices[1]]
        t1, t2 = t_list[indices[0]], t_list[indices[1]]

        exponent = EstimateTimeComplexity(n1, n2, t1, t2)
        if exponent != -1:
            estimators.append(exponent)

    print("Estimators:", estimators)
    # Filter estimators to remove outliers
    estimators = [e for e in estimators if -5 <= e <= 7]

    # Définir l'intervalle des exponents
    min_estimator = min(estimators)
    max_estimator = max(estimators)
    if min_estimator == max_estimator:
        min_estimator -= 1e-10
        max_estimator += 1e-10
    interval_width = (max_estimator - min_estimator) / number_of_bars

    # Comptage des valeurs dans chaque intervalle
    bar_heights = [0] * number_of_bars
    for estimator in estimators:
        index = min(int((estimator - min_estimator) / interval_width), number_of_bars - 1)
        bar_heights[index] += 1

    # Définir positions et largeur des barres
    bar_edges = [min_estimator + i * interval_width for i in range(number_of_bars + 1)]
    bar_positions = [(bar_edges[i] + bar_edges[i+1]) / 2 for i in range(number_of_bars)]
    bar_width = interval_width * 0.9

    # Labels des intervalles
    xtick_labels = [f"[{bar_edges[i]:.2f}, {bar_edges[i+1]:.2f}]" for i in range(number_of_bars)]

    # Affichage du bar plot
    if withPlot:
        plt.figure(figsize=(10, 6))
        plt.bar(bar_positions, bar_heights, width=bar_width, align='center', edgecolor='black', color='skyblue')
        plt.xlabel('Estimated Exponent')
        plt.ylabel('Frequency')
        plt.title('PDF of Estimated Time Complexity Exponents (Filtered)')
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

    mean_estimator = mean(estimators)
    variance_estimator = varience(estimators)
    print("Mean of estimators:", mean_estimator)
    print("Variance of estimators:", variance_estimator)
    print("numberOfEstimators:", len(estimators))
    return estimators


def plot_gj(num_journeys_start = 1, num_journeys_end = 11, step = 10, num_bar = 10, num_estimator = 100, withPlot = True):
    if num_journeys_end < num_journeys_start:
        raise ValueError("num_journeys_end must be greater than num_journeys_start")
    if step <= 0:
        raise ValueError("step must be a positive integer")

    n = []
    times = []
    for num_journeys in range(num_journeys_start, num_journeys_end + step, step):
        print("num_journeys", num_journeys)
        n.append(num_journeys)
        gj.generate_journeys(num_journeys)
        start_time = time.time()
        nn.new_network("./csv/airports.csv", "./csv/pre_existing_routes.csv", "./csv/wanted_journeys.csv", 1000, True, 42, False, 20, 1000, 0.1, False, 20)
        end_time = time.time()
        times.append(end_time - start_time)
    if withPlot:
        plt.plot(range(num_journeys_start, num_journeys_end + step, step), times, marker='o')
        plt.xlabel('Number of Journeys')
        plt.ylabel('Execution Time (s)')
        plt.title('Execution Time vs Number of Journeys')
        plt.grid(True)
        plt.show()

        plt.loglog(range(num_journeys_start, num_journeys_end + step, step), times, marker='o')
        plt.xlabel('Number of Journeys (log scale)')
        plt.ylabel('Execution Time (s) (log scale)')
        plt.title('Log-Log Plot: Execution Time vs Number of Journeys')
        plt.grid(True, which="both", linestyle='--')
        plt.show()

    studyTimeComplexity(n, times, number_of_bars=10, number_of_estimators=num_estimator)

def plot_ga(num_airports_start = 1, num_airports_end = 11, step = 10, num_bar = 10, num_estimator = 100, num_journeys = 100, withPlot = True):
    if num_airports_end >= 75:
        raise ValueError("num_airports_end must be less than 75")
    n = []
    times = []
    for num_airport in range(num_airports_start, num_airports_end + step, step):
        n.append(num_airport)
        gj.generate_airport(num_airport)
        gj.generate_journeys(num_journeys, 'c:/Users/thoma/Desktop/3e/P4/code/P4_LEPL1507/csv/airports_generated.csv') # à changer
        start_time = time.time()
        nn.new_network("./csv/airports_generated.csv", "./csv/pre_existing_routes.csv", "./csv/wanted_journeys.csv", 1000, True, 42, False, 20, 1000, 0.1, False, 20)
        end_time = time.time()
        times.append(end_time - start_time)

    if withPlot:
        plt.plot(range(num_airports_start, num_airports_end + step, step), times, marker='o')
        plt.xlabel('Number of Airports')
        plt.ylabel('Execution Time (s)')
        plt.title('Execution Time vs Number of Airports')
        plt.grid(True)
        plt.show()

        plt.loglog(range(num_airports_start, num_airports_end + step, step), times, marker='o')
        plt.xlabel('Number of Airports (log scale)')
        plt.ylabel('Execution Time (s) (log scale)')
        plt.title('Log-Log Plot: Execution Time vs Number of Airports')
        plt.grid(True, which="both", linestyle='--')
        plt.show()

    return studyTimeComplexity(n, times, number_of_bars=num_bar, number_of_estimators=num_estimator, withPlot=withPlot)

def plot_pa():
    num_airports_list = [10, 20, 30, 40, 50, 60]
    step = 100
    i_values = range(5, 1006, step)
    plt.figure(figsize=(10, 6))

    for num_airports in num_airports_list:
        times = []
        gj.generate_airport(num_airports)
        gj.generate_journeys(100, 'c:/Users/thoma/Desktop/3e/P4/code/P4_LEPL1507/csv/airports_generated.csv')
        for i in i_values:
            start_time = time.time()
            nn.new_network("./csv/airports_generated.csv", "./csv/pre_existing_routes.csv", "./csv/wanted_journeys.csv", 1000, True, 42, False, i, 1000, 0.1, False, 20)
            end_time = time.time()
            times.append(end_time - start_time)
        plt.plot(i_values, times, marker='o', label=f'{num_airports} Airports')

    plt.xlabel('Parameter i')
    plt.ylabel('Execution Time (s)')
    plt.title('Execution Time vs Parameter population size (i)')
    plt.legend()
    plt.grid(True)
    plt.show()

plot_pa()

num_simulations_for_complexity = 5 # half the number of simulations (charging bars) - 2
step = 10 # step for the number of journeys
num_bar = 10 #nombre de barres dans la pdf
num_estimator = 10000 # un nombre trop petit comme inférieur au nombre de barres de chargement fait perdre de l'information. Prendre un nombre trop grand n'est pas utile.

plot_gj(num_journeys_start= 1, num_journeys_end=1 + step + step * 2 * num_simulations_for_complexity, step=step, num_bar=num_bar, num_estimator=num_estimator)
# pour généré un plots pour des wanteds_journeys de différentes tailles.

step = 1
num_bar = 100 #nombre de barres dans la pdf
num_estimator = 10000 # un nombre trop petit comme inférieur au nombre de barres de chargement fait perdre de l'information. Prendre un nombre trop grand n'est pas utile.
num_simulations_for_complexity = 33 # attention max 75 aeroport donc le plus proche possible de 75 mais pas 75

# k = plot_ga(num_airports_start= 5 , num_airports_end= 5 + step + step * 2 * num_simulations_for_complexity, step=step, num_bar=num_bar, num_estimator=num_estimator, num_journeys = 75*74)
# print("k ", k)

def generateMatrix1():
    i = 2
    step2 = 10
    while(i < 103):
        k = plot_ga(num_airports_start= 5 , num_airports_end= 5 + step + step * 2 * num_simulations_for_complexity, step=step, num_bar=num_bar, num_estimator=num_estimator, num_journeys = i, withPlot= False)
        i+= step2
        with open("estimators_matrix.txt", "a") as file:  # Use "a" mode to append instead of overwrite
            file.write(" ".join(map(str, k)) + "\n")

def calculateRowMeans():
    means = []
    with open("estimators_matrix.txt", "r") as file:
        for line in file:
            values = list(map(float, line.split()))
            row_mean = mean(values)
            means.append(row_mean)
    print("Row means:", means)
    return means

def calculateMatrix():
    means = calculateRowMeans()

    x_values = np.arange(22, 263, 20)
    model = LinearRegression().fit(x_values.reshape(-1, 1), means)
    plt.plot(x_values, means, marker='o', linestyle='-', color='b', label='Row Means')
    plt.plot(x_values, model.predict(x_values.reshape(-1, 1)), color='r', label='Linear Approximation')
    plt.xlabel('number of wanted journeys (|J|)')
    plt.ylabel('Mean Value of estimators of complexity')
    plt.title('Mean Value of estimators of complexity in function of number of wanted journeys (|J|)')
    plt.legend()
    plt.grid(True)
    plt.show()


