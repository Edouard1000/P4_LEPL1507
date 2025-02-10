import heapq

def dijkstra(incidence_matrix, start, end):
    n = len(incidence_matrix)
    distances = [float('inf')] * n
    distances[start] = 0
    priority_queue = [(0, start)]
    visited = [False] * n

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if visited[current_node]:
            continue

        visited[current_node] = True

        for neighbor, weight in enumerate(incidence_matrix[current_node]):
            if weight > 0 and not visited[neighbor]:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

    return distances[end]