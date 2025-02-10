import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../code')))
from code.parse import parse_airports_data
from code.f import f

# Assuming the data file is named 'airports_data.txt' and located in the same directory
data_file = 'airports_data.txt'

# Parse the data
airports_data = parse_airports_data(data_file)

# Run the function f with the parsed data
result = f(airports_data)

# Print the result
print(result)