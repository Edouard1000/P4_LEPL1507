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

def generate_airport(numberOfAirport):
    csv_folder_path = 'c:/Users/thoma/Desktop/3e/P4/code/P4_LEPL1507/csv'  # Change this to the path of the csv folder

    countries = [chr(i) for i in range(97, 97 + 10)]  # Generates 'a', 'b', ..., 'j'
    cities = [chr(i).upper() for i in range(97, 97 + 10)]  # Generates 'A', 'B', ..., 'J'
    airport_names = [f"Airport_{chr(i)}" for i in range(97, 97 + 10)]  # Generates 'Airport_a', 'Airport_b', ..., 'Airport_j'
    ids = [chr(i) * 3 for i in range(97, 97 + 10)]  # Generates 'aaa', 'bbb', ..., 'jjj'

    airports = []
    for _ in range(numberOfAirport):
        name = f"{random.choice(cities)} {random.choice(airport_names)}"
        city = random.choice(cities)
        country = random.choice(countries)
        ID = random.choice(ids)
        extended_ID = f"{ID}{random.randint(100, 999)}"
        latitude = round(random.uniform(-90, 90), 6)
        longitude = round(random.uniform(-180, 180), 6)
        airports.append((name, city, country, ID, extended_ID, latitude, longitude))

    with open(f'{csv_folder_path}/airports_generated.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'city', 'country', 'ID', 'extended_ID', 'latitude', 'longitude'])
        for airport in airports:
            writer.writerow(airport)


generate_journeys(100)
generate_airport(100)