import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the airports data
df = pd.read_csv('csv/airports.csv')

# Check column names
print("Airports columns:", df.columns)

# Ensure correct column names
df = df.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude', 'City': 'city', 'ID': 'id'})

# Plot airports
fig = px.scatter_geo(df, lat='latitude', lon='longitude', hover_name='city')

# Load the routes data
routes_df = pd.read_csv('csv/pre_existing_routes.csv')

# Check column names
print("Routes columns:", routes_df.columns)

# Ensure correct column names
routes_df = routes_df.rename(columns={'source_id': 'ID_start', 'destination_id': 'ID_end'})

# Add routes
for i, row in routes_df.iterrows():
    source = df[df['id'] == row['ID_start']]
    destination = df[df['id'] == row['ID_end']]

    if source.empty or destination.empty:
        continue  # Skip missing routes

    source = source.iloc[0]
    destination = destination.iloc[0]

    fig.add_trace(go.Scattergeo(
        lat=[source['latitude'], destination['latitude']],
        lon=[source['longitude'], destination['longitude']],
        mode='lines',
        line=dict(width=2, color='blue'),
        opacity=0.6
    ))

# Update layout
fig.update_layout(
    title='Cities from Airports CSV',
    geo=dict(
        scope='world',
        projection_type="natural earth"
    )
)

# Show the plot
fig.show()
