import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import parse as parse
import dijkstra as dij

graph, id_to_index = parse.parse_airport_data("./csv/airports.csv", "./csv/pre_existing_routes.csv")
# Load data
airports = pd.read_csv("./csv/airports.csv")  # Columns: ID, Name, Latitude, Longitude
routes = pd.read_csv("./csv/pre_existing_routes.csv")      # Columns: Start, End (Airport IDs)

# Create a Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Airport Routes Visualization"),
    html.Label("Select a departure Airport", style={'fontSize': '18px', 'fontWeight': 'bold'}),
    dcc.Dropdown(
        id="airport-dropdown1",
        options=[{"label": name, "value": airport_id} for name, airport_id in zip(airports["name"], airports["ID"])],
        placeholder="Select an airport",
        value=airports["ID"].iloc[0],  # Default selection
        clearable=False
    ),
    html.Label("Select a destination Airport", style={'fontSize': '18px', 'fontWeight': 'bold'}),
    dcc.Dropdown(
        id="airport-dropdown2",
        options=[{"label": name, "value": airport_id} for name, airport_id in zip(airports["name"], airports["ID"])],
        placeholder="Select an airport",
        value=airports["ID"].iloc[1],  # Default selection
        clearable=False
    ), 
    html.Label("Best Route", style={'fontSize': '18px', 'fontWeight': 'bold'}),
    html.Div(id="best-route"),
    dcc.Graph(id="routes-map")
])


# ---------------------------
# -- All routes from start --
# ---------------------------


# Callback to update the map
#@app.callback(
#    Output("routes-map", "figure"),
#    [Input("airport-dropdown1", "value")]
#)
#def update_map(selected_airport):
#    # Filter routes for the selected airport
#    airport_routes = routes[routes["ID_start"] == selected_airport]
#    
#    # Get source airport details
#    source_airport = airports[airports["ID"] == selected_airport]
#    if source_airport.empty:
#        return go.Figure()  # Return an empty figure if no match
#    source_airport = source_airport.iloc[0]
#    
#    # Create figure
#    fig = go.Figure()
#
#    # Add selected airport marker
#    fig.add_trace(go.Scattergeo(
#        lon=[source_airport["longitude"]],
#        lat=[source_airport["latitude"]],
#        text=f"{source_airport['name']} ({source_airport['ID']})",
#        mode="markers",
#        marker=dict(size=8, color="red"),
#        name="Selected Airport"
#    ))
#    
#    # Add routes
#    for _, route in airport_routes.iterrows():
#        dest_airport = airports[airports["ID"] == route["ID_end"]]
#        if not dest_airport.empty:
#            dest_airport = dest_airport.iloc[0]
#            fig.add_trace(go.Scattergeo(
#                lon=[source_airport["longitude"], dest_airport["longitude"]],
#                lat=[source_airport["latitude"], dest_airport["latitude"]],
#                mode="lines",
#                line=dict(width=1, color="blue"),
#                name=f"to {dest_airport['ID']}"
#            ))
#            fig.add_trace(go.Scattergeo(
#                lon=[dest_airport["longitude"]],
#                lat=[dest_airport["latitude"]],
#                mode="markers",
#                marker=dict(size=4, color="blue"),
#                name=f"{dest_airport['ID']}"
#            ))
#    
#    # Update layout
#    fig.update_layout(
#        title=f"Routes from {source_airport['name']} ({source_airport['ID']})",
#        geo=dict(
#            scope='world',
#            projection_type="natural earth"
#        ),
#        height=600,  # Control the height directly (in pixels)
#        width=1600
#    )
#    
#    return fig

# ------------------------
# -- Best Route Section --
# ------------------------

@app.callback(
    [Output("routes-map", "figure"), Output("best-route", "children")],
    [Input("airport-dropdown1", "value"), Input("airport-dropdown2", "value")]
)
def update_best_route(start, end):
    fig = go.Figure()
    if (end == start or start is None or end is None):
        fig = add_node(fig, airports[airports["ID"] == start].iloc[0], color="red")
        return update_layout(fig, "Choose a valid start and destination airport"), 0

    start_ind = id_to_index[start]
    end_ind = id_to_index[end]
    distances, paths = dij.optimized_dijkstra(graph, [start_ind], [[end_ind]])
    best_path = paths[start_ind][end_ind]

    if best_path is None:
        return update_layout(fig, f"No existing route from {start} to {end}"), 0

    source_airport = airports[airports["ID"] == start].iloc[0]
    dest_airport = airports[airports["ID"] == end].iloc[0]
    
    current = source_airport
    color = "blue"
    i = 0
    for next_node in best_path:
        if (i != len(best_path)-1):
            next = airports[airports["ID"] == graph.nodes[next_node]["ID"]].iloc[0]
            fig = add_trace(fig, current, next)
        if (i == 0):
            fig = add_node(fig, current, "start airport", color="green")
        elif (i == len(best_path) - 1):
            fig = add_node(fig, current, "dest airport", color="red")
        else:
            fig = add_node(fig, current, "intermediate airport")  
        i += 1
        current = next
    
    return update_layout(fig, f"Routes from {source_airport['name']} to {dest_airport['name']}"), distances[start_ind][end_ind]
# Run app

def add_node(fig, airport, name, color="blue"):
    fig.add_trace(go.Scattergeo(
        lon=[airport["longitude"]],
        lat=[airport["latitude"]],
        text=f"{airport['name']}",
        mode="markers",
        marker=dict(size=8, color=color),
        name=name
    ))
    return fig

def add_trace(fig, current, next, color="blue"):
    fig.add_trace(go.Scattergeo(
        lon=[current["longitude"], next["longitude"]],
        lat=[current["latitude"], next["latitude"]],
        mode="lines",
        line=dict(width=1, color=color)
    ))
    return fig

def update_layout(fig, title):
    fig.update_layout(
        title=title,
        geo=dict(
            scope='world',
            projection_type="natural earth"
        ),
        height=600,  # Control the height directly (in pixels)
        width=1600
    )
    return fig
if __name__ == "__main__":
    app.run_server(debug=True)
