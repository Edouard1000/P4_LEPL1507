import parse as prs
import random
import csv
def generate_journeys(numberOfJourneys):
    csv_folder_path = 'c:/Users/thoma/Desktop/3e/P4/code/P4_LEPL1507/csv' # Change this to the path of the csv folder

    G, _ = prs.parse_airport_data()
    airports = []
    for i in G.nodes:
        airports.append(G.nodes[i]["ID"])

    # print(airports)

    journeys = []
    for _ in range(numberOfJourneys):
        start = random.choice(airports)
        end = random.choice(airports)
        while start == end:  # Ensure start and end are different
            end = random.choice(airports)
        journeys.append((start, end))

    # print(journeys)

    with open(f'{csv_folder_path}/wanted_journeys.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID_start', 'ID_end'])
        for journey in journeys:
            writer.writerow(journey)

generate_journeys(100)