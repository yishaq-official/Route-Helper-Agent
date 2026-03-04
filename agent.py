import heapq

graph = {
    "Addis Ababa": {"Debre Birhan": 130, "Adama": 100},
    "Debre Birhan": {"Addis Ababa": 130, "Dessie": 280},
    "Adama": {"Addis Ababa": 100, "Hawassa": 270},
    "Dessie": {"Debre Birhan": 280},
    "Hawassa": {"Adama": 270}
}

def dijkstra(graph, start, goal):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        (cost, node, path) = heapq.heappop(queue)

        if node in visited:
            continue

        path = path + [node]
        visited.add(node)

        if node == goal:
            return cost, path

        for neighbor, distance in graph[node].items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + distance, neighbor, path))

    return float("inf"), []

# CLI Interaction
print("Available places:")
for place in graph:
    print("-", place)

start = input("\nEnter starting place: ")
goal = input("Enter destination: ")

distance, path = dijkstra(graph, start, goal)

if distance != float("inf"):
    print("\nShortest Path:", " -> ".join(path))
    print("Total Distance:", distance, "km")
else:
    print("No route found.")