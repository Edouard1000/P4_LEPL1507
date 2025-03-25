from parse import parse_flow_network, indexToId
import networkx as nx

# Parse le graphe
G, id_to_index = parse_flow_network()

print("\nNombre total d'aéroports (nœuds) :", G.number_of_nodes())
print("Nombre total de connexions (arêtes) :", G.number_of_edges())

# 🔎 Exemple : afficher les 3 premiers aéroports
print("\nAéroports (nœuds) [extrait] :")
for i, data in list(G.nodes(data=True))[:3]:
    print(f" - index {i} : {data['ID']} ({data['city']}, {data['country']}) - capacité : {data['capacity']}")

# 🔁 Test inverse : ID ↔ index
test_id = "CDG"
print(f"\nMapping ID to index : {test_id} → {id_to_index.get(test_id, 'inconnu')}")
print(f"Mapping index to ID : {id_to_index.get(test_id)} → {indexToId(id_to_index.get(test_id))}")

# ✈️ Afficher quelques routes avec distance et capacité
print("\n🛣️ Connexions [extrait] :")
for u, v, data in list(G.edges(data=True))[:5]:
    print(f" - {G.nodes[u]['ID']} → {G.nodes[v]['ID']} | dist = {data['distance']:.2f} km | cap = {data['capacity']}")

# 💥 Vérifie si un aéroport a une capacité non assignée (erreur possible)
missing_caps = [i for i, data in G.nodes(data=True) if data["capacity"] is None]
print("\nAéroports sans capacité (devraient être 0 si tout est bien mappé) :", len(missing_caps))



def optimize_flow(G, id_to_index, source_code, target_code, F):
    """
    Résout un problème de flot à coût minimal pour l'objectif A.
    - source_code : ID de l'aéroport de départ (ex: 'CDG')
    - target_code : ID de l'aéroport d'arrivée (ex: 'PEK')
    - F : flux de personnes à transporter
    """

    # Copie du graphe pour éviter de modifier l'original
    G_flow = G.copy()

    # Appliquer les "demandes" de flux
    for n in G_flow.nodes():
        G_flow.nodes[n]["demand"] = 0
    G_flow.nodes[id_to_index[source_code]]["demand"] = -F
    G_flow.nodes[id_to_index[target_code]]["demand"] = F

    # Appel de l'algo de flot à coût minimal
    try:
        flow_dict = nx.min_cost_flow(G_flow)
    except nx.NetworkXUnfeasible:
        print("❌ Aucune solution trouvable avec ce flux et ces capacités.")
        return

    # Suivi du flux pour affichage
    print("\n📦 Cheminement du flux :")
    total_distance = 0
    paths = []  # Pour une visualisation plus claire

    def recurse_flow(u, current_flow, path):
        for v in flow_dict[u]:
            f = flow_dict[u][v]
            if f > 0:
                d = G[u][v]["distance"]
                total = f * d
                nonlocal total_distance
                total_distance += total
                subpath = path + [(v, f)]
                paths.append(subpath)
                recurse_flow(v, f, subpath)

    recurse_flow(id_to_index[source_code], F, [(id_to_index[source_code], F)])

    # Print les chemins construits
    for p in paths:
        trace = []
        for node, count in p:
            trace.append(f"{count} → {G.nodes[node]['ID']}")
        print("  " + " → ".join(trace))

    # Afficher la distance moyenne parcourue
    avg_distance = total_distance / F
    print(f"\n📏 Distance totale : {total_distance:.2f} km")
    print(f"📊 Distance moyenne par passager : {avg_distance:.2f} km")

G, id_to_index = parse_flow_network()
optimize_flow(G, id_to_index, source_code="CDG", target_code="BKK", F=1000)
