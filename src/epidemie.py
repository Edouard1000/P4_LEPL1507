import networkx as nx
import parse
from itertools import combinations
import plotly.graph_objects as go
import community.community_louvain as community_louvain
from collections import defaultdict
import igraph as ig
import leidenalg
from cdlib import algorithms
from cdlib import NodeClustering

def closeness_airports(G, k=2):
    """
    This function returns the k most central airports in the network.
    """
    # Calculate the closeness centrality for each node in the graph
    closeness_centrality = nx.closeness_centrality(G, distance='distance')

    # Normalize closeness centrality values
    max_centrality = max(closeness_centrality.values())
    min_centrality = min(closeness_centrality.values())
    normalized_centrality = {
        node: (value - min_centrality) / (max_centrality - min_centrality)
        for node, value in closeness_centrality.items()
    }

    top_k_airports = sorted(
        closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:k]

    # Extract all node data for the Scattergeo
    lats = [G.nodes[n]['latitude'] for n in G.nodes]
    lons = [G.nodes[n]['longitude'] for n in G.nodes]
    colors = [normalized_centrality[n] for n in G.nodes]

    fig = go.Figure()

    # Single trace with colors
    fig.add_trace(go.Scattergeo(
        lat=lats,
        lon=lons,
        mode='markers',
        marker=dict(
            size=10,
            color=colors,
            colorscale='Viridis',
            cmin=0,
            cmax=1,
            colorbar=dict(title="Closeness Centrality"),
            line_width=0,
        ),
        text=[f"{n}<br>Centrality: {closeness_centrality[n]:.4f}" for n in G.nodes],
        hoverinfo='text',
    ))

    # Highlight the top k airports
    for airport in top_k_airports:
        airport_id = airport[0]
        airport_data = G.nodes[airport_id]
        fig.add_trace(go.Scattergeo(
            lat=[airport_data['latitude']],
            lon=[airport_data['longitude']],
            mode='markers',
            marker=dict(size=18, color='red', symbol='star'),
        ))

    # Update layout
    fig.update_layout(
        title="Airport Network - Closeness Centrality",
        geo=dict(
            scope='world',
            projection_type="natural earth"
        )
    )

    fig.show()
    
    return top_k_airports

def central_airports(G, k=2):
    """
    This function returns the k most central airports in the network.
    """
    # Find the k airports that minimize the maximum time to reach any other airport
    fig = go.Figure()
    best_airports = []
    min_max_time = float('inf')

    # Iterate over all combinations of k airports
    # Precompute single-source Dijkstra path lengths for all nodes
    dijkstra_paths = {
        source: nx.single_source_dijkstra_path_length(G, source, weight='distance')
        for source in G.nodes
    }

    airport_combinations = []
    for airport_combination in combinations(G.nodes, k):
        max_time = 0
        for target in G.nodes:
            if target not in airport_combination:
                # Find the minimum time to reach the target from any airport in the combination
                min_time_to_target = min(
                    dijkstra_paths[source].get(target, float('inf'))
                    for source in airport_combination
                )
                max_time = max(max_time, min_time_to_target)
        airport_combinations.append((airport_combination, max_time))

    # Sort combinations by their maximum time in ascending order
    airport_combinations.sort(key=lambda x: x[1])

    # Normalize the maximum times for airport combinations
    max_times = [combo[1] for combo in airport_combinations]
    max_time_min = min(max_times)
    max_time_max = max(max_times)
    normalized_times = [
        (combo[0], (combo[1] - max_time_min) / (max_time_max - max_time_min))
        for combo in airport_combinations
    ]
    for n in normalized_times:
        print(f"Combination: {n[0][0]}, Normalized Time: {n[1]}")

    # Extract all node data for the Scattergeo
    lats = [G.nodes[n[0][0]]['latitude'] for n in normalized_times]
    lons = [G.nodes[n[0][0]]['longitude'] for n in normalized_times]
    colors = [normalized_times[n[0][0]][1] for n in normalized_times]  # Use the best combination's normalized time

    fig = go.Figure()

    # Single trace with colors
    fig.add_trace(go.Scattergeo(
        lat=lats,
        lon=lons,
        mode='markers',
        marker=dict(
            size=10,
            color=colors,
            colorscale='Viridis',
            cmin=0,
            cmax=1,
            colorbar=dict(title="Normalized Max Time"),
            line_width=0,
        ),
        text=[f"{n}" for n in G.nodes],
        hoverinfo='text',
    ))

    # Highlight the best airport combination
    best_combination = normalized_times[0][0]
    for airport_id in best_combination:
        airport_data = G.nodes[airport_id]
        fig.add_trace(go.Scattergeo(
            lat=[airport_data['latitude']],
            lon=[airport_data['longitude']],
            mode='markers',
            marker=dict(size=18, color='red', symbol='star'),
            name=f"Best Airport {airport_id}"
        ))

    fig.update_layout(
        title="Airport Network - Max distance to reach any airport",
        geo=dict(
            scope='world',
            projection_type="natural earth"
        )
    )
    # Show the plot
    fig.show()

def clusters(G):
    """
    This function returns the clusters of airports in the network.
    """
    
    G_ig = ig.Graph(directed=True)
    G_ig.add_vertices(list(G.nodes()))
    G_ig.add_edges(list(G.edges()))

    # Apply Leiden with directed modularity
    partition = leidenalg.find_partition(G_ig, leidenalg.ModularityVertexPartition, weights=None)

    clusters = defaultdict(list)
    for node, comm in enumerate(partition.membership):
        clusters[comm].append(G_ig.vs[node]["name"])

    print(f"Number of clusters: {len(clusters)}")

    fig = go.Figure()

    # Add clusters to the plot
    colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    for i, cluster_airports in enumerate(clusters.values()):
        latitudes = [G.nodes[airport]['latitude'] for airport in cluster_airports]
        longitudes = [G.nodes[airport]['longitude'] for airport in cluster_airports]
        fig.add_trace(go.Scattergeo(
            lat=latitudes,
            lon=longitudes,
            mode='markers',
            marker=dict(size=10, color=colors[i % len(colors)]),
            name=f"Cluster {i + 1} ({len(clusters)})"
        ))

    # Update layout
    fig.update_layout(
        title="Airport Network - Louvain Clustering",
        showlegend=True,
        geo=dict(
            scope='world',
            projection_type="natural earth"
        )
    )

    fig.show()
    return len(clusters)

G = parse.parse_airport_data("./csv/airports.csv", "./csv/pre_existing_routes.csv")[0]
print(clusters(G))
#closeness_airports(G, k=1)
#central_airports(G, k=1)