import parse as prs
import random
import csv
def generate_journeys(numberOfJourneys, airports_file = 'c:/Users/thoma/Desktop/3e/P4/code/P4_LEPL1507/csv/airports.csv'):
    csv_folder_path = 'c:/Users/thoma/Desktop/3e/P4/code/P4_LEPL1507/csv' # Change this to the path of the csv folder

    G, _ = prs.parse_airport_data(airports_file = airports_file)
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

def generate_airport(numberOfAirport):
    csv_folder_path = 'c:/Users/thoma/Desktop/3e/P4/code/P4_LEPL1507/csv'  # Change this to the path of the csv folder
    input_csv_path = f'{csv_folder_path}/airports.csv'

    airports = []
    with open(input_csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            airports.append((row['name'], row['city'], row['country'], row['ID'], row['extended_ID'], row['latitude'], row['longitude']))
            if len(airports) >= numberOfAirport:
                break

    with open(f'{csv_folder_path}/airports_generated.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'city', 'country', 'ID', 'extended_ID', 'latitude', 'longitude'])
        for airport in airports:
            writer.writerow(airport)


# generate_journeys(100, 'c:/Users/thoma/Desktop/3e/P4/code/P4_LEPL1507/csv/airports_generated.csv')
# generate_airport(15)