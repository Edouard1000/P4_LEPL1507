import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import parse as parse
import secondary_parse as parse2
import dijkstra as dij

graph, id_to_index = parse.parse_airport_data("./csv/airports.csv", "./csv/pre_existing_routes.csv")
cost_graph, id_to_index2 = parse2.parse_cost()

cost_matrix  = pd.read_csv("./output_csv/network_graph_adj_matrix_costs.csv", header=None).values
time_matrix  = pd.read_csv("./output_csv/network_graph_adj_matrix.csv", header=None).values
# Load data
airports = pd.read_csv("./csv/airports.csv")  # Columns: ID, Name, Latitude, Longitude

# Create a Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Airport Routes Visualization"),
    
    html.Div([
        html.Div([
            html.Label("Select a departure Airport", style={'fontSize': '18px', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id="airport-dropdown1",
                options=[{"label": name, "value": airport_id} for name, airport_id in zip(airports["name"], airports["ID"])],
                placeholder="Select an airport",
                value=airports["ID"].iloc[0],  # Default selection
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("Select a destination Airport", style={'fontSize': '18px', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id="airport-dropdown2",
                options=[{"label": name, "value": airport_id} for name, airport_id in zip(airports["name"], airports["ID"])],
                placeholder="Select an airport",
                value=airports["ID"].iloc[1],  # Default selection
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Select your flight criterium to optimize", style={'fontSize': '18px', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id="flight-criterium",
                options=[
                    {"label": "Distance", "value": "distance"},
                    {"label": "Time", "value": "time"},
                    {"label": "Cost", "value": "cost"}
                ],
                value="distance",
                clearable=False
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
    ], style={'display': 'flex', 'justifyContent': 'space-between'}), 

    html.Div([
        html.Div([
            html.Label("Distance in km", style={'fontSize': '18px', 'fontWeight': 'bold'}),
            html.Div(id="distance")
        ], style={'width': '15%', 'display': 'inline-block', 'marginLeft': '15%'}),

        html.Div([
            dcc.Graph(id="routes-map")
        ], style={'width': '75%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'justifyContent': 'space-between'}),
])

# Callbacks

@app.callback(
    [Output("routes-map", "figure"), Output("distance", "children")],
    [Input("airport-dropdown1", "value"), Input("airport-dropdown2", "value"), Input("flight-criterium", "value")]
)
def update_best_route(start, end, criterium):
    fig = go.Figure()
    if (end == start or start is None or end is None or criterium is None):
        fig = add_node(fig, airports[airports["ID"] == start].iloc[0], color="red")
        return update_layout(fig, "Choose a valid start and destination airport and criterium"), 0

    start_ind = id_to_index[start]
    end_ind = id_to_index[end]
    distances = None
    paths = None
    best_path = None

    if criterium == "distance":
        distances, paths = dij.optimized_dijkstra(graph, [start_ind], [[end_ind]])
        best_path = paths[start_ind][end_ind]
    elif criterium == "time":
        distances, paths = parse2.dijkstra_time(graph, [start_ind], {start_ind : end_ind}, 2, time_matrix)
        best_path = [start_ind]+paths[start_ind][end_ind]+[end_ind]
    elif criterium == "cost":
        distances, paths = dij.optimized_dijkstra(cost_graph, [start_ind], [[end_ind]])
        print("paths")
        print(paths)
        if (end_ind not in paths[start_ind]):
            fig.add_node(fig, airports[airports["ID"] == start].iloc[0], color="red")
            return update_layout(fig, f"No existing route from {start} to {end}"), 0
        best_path = paths[start_ind][end_ind]

    if best_path is None:
        return update_layout(fig, f"No existing route from {start} to {end}"), 0

    source_airport = airports[airports["ID"] == start].iloc[0]
    dest_airport = airports[airports["ID"] == end].iloc[0]
    
    current = source_airport

    for i, next_node in enumerate(best_path[1:]):
        if (i != len(best_path)-1):
            next = airports[airports["ID"] == graph.nodes[next_node]["ID"]].iloc[0]
            fig = add_trace(fig, current, next)
        if (i == 0):
            fig = add_node(fig, current, "start airport", color="green")
        if (i == len(best_path) - 2):
            fig = add_node(fig, current, "dest airport", color="blue")
            fig = add_node(fig, next, "dest airport", color="red")
        else:
            fig = add_node(fig, current, "intermediate airport")  
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
        title_x=0.5
    )
    return fig
if __name__ == "__main__":
    app.run_server(debug=True)
