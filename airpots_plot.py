import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

def plot_airport_network(airports_file, routes_file, title="Airports and Flight Routes"):
    """
    Plots the airport network using the given airports and routes data.

    Parameters:
    - airports_file (str): Path to the airports CSV file.
    - routes_file (str): Path to the routes CSV file.
    - title (str): Title of the plot.
    """
    # Load the airports data
    df = pd.read_csv(airports_file)

    # Ensure correct column names
    df = df.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude', 'City': 'city', 'ID': 'id'})

    # Plot airports
    fig = px.scatter_geo(df, lat='latitude', lon='longitude', hover_name='city')

    # Load the routes data
    routes_df = pd.read_csv(routes_file)

    # Ensure correct column names
    routes_df = routes_df.rename(columns={'source_id': 'ID_start', 'destination_id': 'ID_end'})

    # Add routes to the plot
    for _, row in routes_df.iterrows():
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
            line=dict(width=1, color='blue'),
            opacity=0.6
        ))

    # Update layout
    fig.update_layout(
        title=title,
        geo=dict(
            scope='world',
            projection_type="natural earth"
        )
    )

    # Show the plot
    fig.show()

def interactive_network(airports_file, routes_file, title="Airport and flight routes"):

    app = dash.Dash(__name__)

    airports = pd.read_csv(airports_file)
    airports = airports.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude', 'City': 'city', 'ID': 'id'})
    # Plot airports
    fig = px.scatter_geo(airports, lat='latitude', lon='longitude', hover_name='city')

    # Load the routes data
    routes = pd.read_csv(routes_file)

    # Ensure correct column names
    routes = routes.rename(columns={'source_id': 'ID_start', 'destination_id': 'ID_end'})

    # Add routes to the plot
    for _, row in routes.iterrows():
        source = airports[airports['id'] == row['ID_start']]
        destination = airports[airports['id'] == row['ID_end']]

        if source.empty or destination.empty:
            continue  # Skip missing routes

        source = source.iloc[0]
        destination = destination.iloc[0]

        fig.add_trace(go.Scattergeo(
            lat=[source['latitude'], destination['latitude']],
            lon=[source['longitude'], destination['longitude']],
            mode='lines',
            line=dict(width=1, color='blue'),
            opacity=0.6
        ))

    # Update layout
    fig.update_layout(
        title=title,
        geo=dict(
            scope='world',
            projection_type="natural earth"
        )
    )
    app.layout = html.Div([
        html.H1("Airport Routes Visualization"),

        dcc.Dropdown(
            id="airport-dropdown",
            options=[{"label": name, "value": code} for name, code in zip(airports["Name"], airports["IATA"])],
            placeholder="Select an airport",
            value=airports["IATA"].iloc[0],  # Default selection
            clearable=False
        ),

        dcc.Graph(id="routes-map")
    ])
    
    @app.callback(
        Output('graph', 'figure'),
        [Input('slider', 'value')]
    )
    def update_graph(value):
        updated_fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[v * value for v in [4, 1, 2]])])
        return updated_fig
    app.run_server(debug=True)

# Example usage
plot_airport_network('csv/airports.csv', 'csv/pre_existing_routes.csv', title="Global Airport Network")
plot_airport_network('csv/testFileAirports.csv', 'csv/testFilePreExistingRoutes.csv', title="Test Airport Network")