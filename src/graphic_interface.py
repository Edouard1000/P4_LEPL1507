import webbrowser
import threading
import dash
import time
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import parse as parse
import utility_functions as uf
import dijkstra as dij
import networkx as nx

graph, id_to_index = parse.parse_airport_data("./csv/airports.csv", "./csv/pre_existing_routes.csv")
cost_graph, id_to_index2 = parse.parse_cost()
# Load data
airports = pd.read_csv("./csv/airports.csv")  # Columns: ID, Name, Latitude, Longitude

#network_graph_adj_matrix = nx.adjacency_matrix(graph, weight= "distance").todense()
#df = pd.DataFrame(network_graph_adj_matrix)
#df.to_csv("./output_csv/network_graph_adj_matrix.csv", index=False, header=False)
#network_graph_adj_matrix_price = nx.adjacency_matrix(cost_graph, weight= "distance").todense()
#df_price = pd.DataFrame(network_graph_adj_matrix_price)
#df_price.to_csv("./output_csv/network_graph_adj_matrix_costs.csv", index=False, header=False)

cost_matrix  = pd.read_csv("./output_csv/network_graph_adj_matrix_costs.csv", header=None).values
dist_matrix  = pd.read_csv("./output_csv/network_graph_adj_matrix.csv", header=None).values
waiting_time = pd.read_csv("./csv/waiting_times.csv", header=None).values

waiting_time = pd.DataFrame(waiting_time)
waiting_time.columns = waiting_time.iloc[0]  # Set the first row as the header
waiting_time = waiting_time.drop(0).reset_index(drop=True)
waiting_time['idle_time'] = waiting_time['idle_time'].astype(float)

def graphic_interface(airports, cost_graph, graph, waiting_time, cost_matrix, dist_matrix):


    style_sub={'fontSize': '24px', 'fontWeight': 'bold', 'color': 'white', 'fontFamily': 'Arial, sans-serif'}
    # Create a Dash app
    app = dash.Dash(__name__)

    # Layout
    app.layout = html.Div([
        html.H1("Airport Routes Visualization", style={'textAlign': 'center', 'fontFamily': 'Arial, sans-serif'}),

        # Dropdowns Section (Blue Background)
        html.Div([
            html.Div([
                html.Label("Departure Airport", style=style_sub),
                dcc.Dropdown(
                    id="airport-dropdown1",
                    options=[{"label": name, "value": airport_id} for name, airport_id in zip(airports["name"], airports["ID"])],
                    placeholder="Select an airport",
                    value=airports["ID"].iloc[0],
                    clearable=False
                )
            ], style={'width': '30%', 'display': 'inline-block'}),

            html.Button(html.Img(src="./assets/fleche_gauche_droite.png", style={'width': '40px', 'height': '40px'}), id="swap-button", n_clicks=0, style={
                'width': '3%', 'height': '40px', 'margin': '30px 10px',
                'fontSize': '20px', 'fontWeight': 'bold', 'cursor': 'pointer',
                'borderRadius': '10px', 'border': 'none', 'backgroundColor': 'white'
            }),

            html.Div([
                html.Label("Destination Airport", style=style_sub),
                dcc.Dropdown(
                    id="airport-dropdown2",
                    options=[{"label": name, "value": airport_id} for name, airport_id in zip(airports["name"], airports["ID"])],
                    placeholder="Select an airport",
                    value=airports["ID"].iloc[1],
                    clearable=False
                )
            ], style={'width': '30%', 'display': 'inline-block'}),

            html.Div([
                html.Label("Flight criterium to optimize", style=style_sub),
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

        ], style={  # Background for dropdowns
            'backgroundColor': '#007BFF',  # Blue background
            'padding': '20px',
            'borderRadius': '10px',
            'marginBottom': '20px',
            'display': 'flex',
            'justifyContent': 'space-between'
        }),

        # Main Content (Sidebar + Graph)
        html.Div([
            # Sidebar (Blue Background)
            html.Div([
                html.Label("Flight Parameters", style=style_sub),
                html.Div([
                    # Distance
                    html.Div([
                        html.Img(src="./assets/distance.png", style={'width': '30px', 'height': '30px', 'marginRight': '10px'}),
                        html.Label("Distance (km):", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'white', 'flexGrow': '1'}),
                        html.Div(id="distance", style={'fontSize': '16px', 'color': 'white'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),

                    # Time
                    html.Div([
                        html.Img(src="./assets/prime-time.png", style={'width': '30px', 'height': '30px', 'marginRight': '10px'}),
                        html.Label("Time (hours):", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'white', 'flexGrow': '1'}),
                        html.Div(id="time", style={'fontSize': '16px', 'color': 'white'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),

                    # Cost
                    html.Div([
                        html.Img(src="./assets/etiquette-de-prix.png", style={'width': '30px', 'height': '30px', 'marginRight': '10px'}),
                        html.Label("Cost ($):", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'white', 'flexGrow': '1'}),
                        html.Div(id="cost", style={'fontSize': '16px', 'color': 'white'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'}),
                ], style={'padding': '10px'}),

            ], style={  # Sidebar styles
                'backgroundColor': '#0056b3',
                'padding': '20px',
                'borderRadius': '10px',
                'width': '20%',
                'display': 'inline-block',
                'verticalAlign': 'top',
                'height': '250px'  # Adjust height to match the content
            }),

            # Graph Section
            html.Div([
                dcc.Graph(id="routes-map")
            ], style={'width': '75%', 'display': 'inline-block', 'marginLeft': '5%'})

        ], style={'display': 'flex', 'justifyContent': 'space-between'}),
    ])



    # Callbacks

    @app.callback(
        [Output("routes-map", "figure"), Output("distance", "children"), Output("time", "children"), Output("cost", "children")],
        [Input("airport-dropdown1", "value"), Input("airport-dropdown2", "value"), Input("flight-criterium", "value")]
    )
    def update_best_route(start, end, criterium):
        fig = go.Figure()
        if (end == start or start is None or end is None or criterium is None):
            fig = add_node(fig, airports[airports["ID"] == start].iloc[0], "airport", color="red")
            return update_layout(fig), 0, 0, 0

        start_ind = id_to_index[start]
        end_ind = id_to_index[end]
        source_airport = airports[airports["ID"] == start].iloc[0]
        distances = None
        paths = None
        best_path = None
        cost = 0
        dist = 0
        time = 0

        # Calculate the best path based on the selected criterium
        if criterium == "distance":
            try:
                distances, paths = nx.single_source_dijkstra(graph, source=start_ind, target=end_ind, weight="distance")
            except nx.NetworkXNoPath:
                return update_layout(fig), 0, 0, 0
            
            best_path = paths

            dist = distances
            for i, next_node in enumerate(best_path[1:]):
                cost += cost_matrix[best_path[i]][next_node]
                node_id = graph.nodes[next_node]["ID"]
                time += uf.dist_to_time(dist_matrix[best_path[i]][next_node])+waiting_time[waiting_time["ID"] == node_id]["idle_time"].iloc[0]/60
            time -= waiting_time[waiting_time["ID"] == end]["idle_time"].iloc[0]/60

        elif criterium == "time":
            distances, paths = dij.dijkstra_time(graph, [start_ind], {start_ind : [end_ind]}, dist_matrix, waiting_time, graph)
            
            best_path = [start_ind]+paths[start_ind][end_ind]+[end_ind]

            time = distances[start_ind][end_ind]
            for i, next_node in enumerate(best_path[1:]):
                cost += cost_matrix[best_path[i]][next_node]
                dist += dist_matrix[best_path[i]][next_node]

        elif criterium == "cost":
            try :
                distances, paths = nx.single_source_dijkstra(cost_graph, start_ind, target=end_ind, weight="distance")
            except nx.NetworkXNoPath:
                return update_layout(fig, f"No existing route from {start} to {end}"), 0, 0, 0
            
            best_path = paths

            cost = distances
            for i, next_node in enumerate(best_path[1:]):
                dist += dist_matrix[best_path[i]][next_node]
                node_id = graph.nodes[next_node]["ID"]
                time += uf.dist_to_time(dist_matrix[best_path[i]][next_node])+ waiting_time[waiting_time["ID"] == node_id]["idle_time"].iloc[0]/60
            time -= waiting_time[waiting_time["ID"] == end]["idle_time"].iloc[0]/60


        if best_path is None:
            return update_layout(fig), 0, 0, 0

        plot_path(fig, best_path, airports, source_airport)

        update_layout(fig)
        return fig, round(dist, 2), round(time, 2) , round(cost, 2)

    @app.callback(
        [Output("airport-dropdown1", "value"),
         Output("airport-dropdown2", "value")],
        Input("swap-button", "n_clicks"),
        [State("airport-dropdown1", "value"),
         State("airport-dropdown2", "value")]
    )    
    def swap_airports(n_clicks, dep_value, arr_value):
        if n_clicks % 2+1 == 1:  # Swap only on odd clicks
            return arr_value, dep_value
        return dep_value, arr_value  # No change on even clicks

    def plot_path(fig, best_path, airports, start):
        current = start
        for i, next_node in enumerate(best_path[1:]):
            if (i != len(best_path)-1):
                next = airports[airports["ID"] == graph.nodes[next_node]["ID"]].iloc[0]
                fig = add_trace(fig, current, next)
            if (i == 0):
                fig = add_node(fig, current, "start airport", color="green")           
            else:
                fig = add_node(fig, current, "intermediate airport")  
            current = next
        fig = add_node(fig, next, "dest airport", color="red")

    def add_node(fig, airport, name, color="blue"):
        fig.add_trace(go.Scattergeo(
            lon=[airport["longitude"]],
            lat=[airport["latitude"]],
            text=f"{airport['name']}",
            mode="markers",
            marker=dict(size=8, color=color),
            name=name,
            showlegend=False  # Do not show in legend
        ))
        return fig

    def add_trace(fig, current, next, color="blue"):
        fig.add_trace(go.Scattergeo(
            lon=[current["longitude"], next["longitude"]],
            lat=[current["latitude"], next["latitude"]],
            mode="lines+markers",
            line=dict(width=1, color=color),
            showlegend=False  # Do not show in legend
        ))
        return fig

    def update_layout(fig):
        fig.update_layout(
            #title=dict(
            #    text=title,
            #    font=dict(size=25, family="Arial, sans-serif", color="black"),
            #    x=0.5,  # Center the title
            #    y=0.95  # Move it slightly higher for better spacing
            #),
            geo=dict(
                scope="world",
                projection=dict(type="natural earth"),  # More natural-looking projection
                showland=True, landcolor="whitesmoke",  # Soft color for land
                showocean=True, oceancolor="lightblue",  # Light blue oceans
                showlakes=True, lakecolor="lightblue",
                showrivers=True, rivercolor="lightblue",
                showcountries=True, countrycolor="gray",
                countrywidth=0.7,  # Thin country borders
                coastlinecolor="black",
                coastlinewidth=0.7,
            ),
            margin=dict(l=20, r=20, t=40, b=20),  # Reduce margins for a cleaner look
            paper_bgcolor="white",  # Background color of entire figure
        )
        return fig

    return app

if __name__ == "__main__":
    app = graphic_interface(airports, cost_graph, graph, waiting_time, cost_matrix, dist_matrix)
    app.run_server(debug=True, use_reloader=False)

    
