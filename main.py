import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './code')))
from python_files.parse import parse_airport_data
from python_files.f import f

# Assuming the data file is named 'airports_data.txt' and located in the same directory
airports_file = "./csv/airports.csv"
routes_file = "./csv/pre_existing_routes.csv"

# Parse the data
airports_data = parse_airport_data(airports_file, routes_file)

# Trajectories
trajectories = None

# Output folder
output_folder = None

# Run the function f with the parsed data
result = f(airports_data, trajectories, output_folder)

# Print the result
print(result)