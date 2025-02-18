import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

# Load data
airports = pd.read_csv("csv/airports.csv")  # Columns: ID, Name, Latitude, Longitude
routes = pd.read_csv("csv/pre_existing_routes.csv")      # Columns: Start, End (Airport IDs)

# Create a Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Airport Routes Visualization"),
    
    dcc.Dropdown(
        id="airport-dropdown",
        options=[{"label": name, "value": airport_id} for name, airport_id in zip(airports["name"], airports["ID"])],
        placeholder="Select an airport",
        value=airports["ID"].iloc[0],  # Default selection
        clearable=False
    ),
    
    dcc.Graph(id="routes-map")
])

# Callback to update the map
@app.callback(
    Output("routes-map", "figure"),
    [Input("airport-dropdown", "value")]
)
def update_map(selected_airport):
    # Filter routes for the selected airport
    airport_routes = routes[routes["Start"] == selected_airport]
    
    # Get source airport details
    source_airport = airports[airports["ID"] == selected_airport]
    if source_airport.empty:
        return go.Figure()  # Return an empty figure if no match
    source_airport = source_airport.iloc[0]
    
    # Create figure
    fig = go.Figure()

    # Add selected airport marker
    fig.add_trace(go.Scattergeo(
        lon=[source_airport["Longitude"]],
        lat=[source_airport["Latitude"]],
        text=f"{source_airport['Name']} ({source_airport['ID']})",
        mode="markers",
        marker=dict(size=10, color="red"),
        name="Selected Airport"
    ))
    
    # Add routes
    for _, route in airport_routes.iterrows():
        dest_airport = airports[airports["ID"] == route["End"]]
        if not dest_airport.empty:
            dest_airport = dest_airport.iloc[0]
            fig.add_trace(go.Scattergeo(
                lon=[source_airport["Longitude"], dest_airport["Longitude"]],
                lat=[source_airport["Latitude"], dest_airport["Latitude"]],
                mode="lines",
                line=dict(width=1, color="blue"),
                name=f"Route to {dest_airport['ID']}"
            ))
    
    # Update layout
    fig.update_layout(
        title=f"Routes from {source_airport['Name']} ({source_airport['ID']})",
        geo=dict(
            scope='world',
            projection_type="natural earth"
        )
    )
    
    return fig

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
