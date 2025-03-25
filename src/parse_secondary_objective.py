from parse import parse_flow_network, indexToId

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
