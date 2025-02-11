import pandas as pd

import plotly.express as px

# Load the data
df = pd.read_csv('csv/airports.csv')

# Assuming the CSV has columns 'City', 'Latitude', and 'Longitude'
fig = px.scatter_geo(df, lat='latitude', lon='longitude', hover_name='city')

# Update layout for better visualization
fig.update_layout(title='Cities from Airports CSV', geo_scope='world')

# Show the plot
fig.show()