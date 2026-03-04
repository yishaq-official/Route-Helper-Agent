import heapq
import json
from copy import deepcopy
from pathlib import Path

GRAPH_FILE = Path("graph.json")
DEFAULT_GRAPH = {
    "Addis Ababa": {"Debre Birhan": 130, "Adama": 100},
    "Debre Birhan": {"Addis Ababa": 130, "Dessie": 280},
    "Adama": {"Addis Ababa": 100, "Hawassa": 270},
    "Dessie": {"Debre Birhan": 280},
    "Hawassa": {"Adama": 270},
}


def make_bidirectional(graph):
    """Ensure every edge exists in both directions with same distance."""
    changed = False
    for city, neighbors in list(graph.items()):
        graph.setdefault(city, {})
        for neighbor, distance in list(neighbors.items()):
            graph.setdefault(neighbor, {})
            if graph[neighbor].get(city) != distance:
                graph[neighbor][city] = distance
                changed = True
    return changed


def load_graph():
    if not GRAPH_FILE.exists():
        graph = deepcopy(DEFAULT_GRAPH)
        make_bidirectional(graph)
        save_graph(graph)
        return graph

    try:
        with GRAPH_FILE.open("r", encoding="utf-8") as f:
            graph = json.load(f)
        if not isinstance(graph, dict):
            raise ValueError("Graph JSON must be an object.")
        if make_bidirectional(graph):
            save_graph(graph)
        return graph
    except (json.JSONDecodeError, OSError, ValueError):
        print("Warning: graph.json is invalid. Loading default graph.")
        graph = deepcopy(DEFAULT_GRAPH)
        make_bidirectional(graph)
        save_graph(graph)
        return graph


def save_graph(graph):
    with GRAPH_FILE.open("w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=True)


def dijkstra(graph, start, goal):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)

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


def show_places(graph):
    print("\nAvailable places:")
    for place in sorted(graph):
        print(f"- {place}")


def get_city_input(prompt):
    return input(prompt).strip()


def get_positive_distance():
    while True:
        value = input("Enter distance (km): ").strip()
        try:
            distance = int(value)
            if distance <= 0:
                print("Distance must be a positive number.")
                continue
            return distance
        except ValueError:
            print("Invalid distance. Please enter a whole number.")


def add_or_link_city(graph, city_name):
    if city_name not in graph:
        graph[city_name] = {}
        print(f"Added city: {city_name}")

    while True:
        neighbor = get_city_input(
            f"Enter a city to connect with {city_name} (or press Enter to stop): "
        )
        if not neighbor:
            break
        if neighbor == city_name:
            print("A city cannot connect to itself.")
            continue
        if neighbor not in graph:
            graph[neighbor] = {}
            print(f"Added city: {neighbor}")
        distance = get_positive_distance()
        graph[city_name][neighbor] = distance
        graph[neighbor][city_name] = distance
        print(f"Linked {city_name} <-> {neighbor} ({distance} km)")

    save_graph(graph)


def ensure_city_exists(graph, city_name):
    if not city_name:
        print("City name cannot be empty.")
        return False

    if city_name in graph:
        return True

    print(f"City '{city_name}' does not exist.")
    choice = input("Do you want to add it now? (y/n): ").strip().lower()
    if choice == "y":
        add_or_link_city(graph, city_name)
        return True
    return False


def find_route(graph):
    start = get_city_input("\nEnter starting place: ")
    if not ensure_city_exists(graph, start):
        return

    goal = get_city_input("Enter destination: ")
    if not ensure_city_exists(graph, goal):
        return

    distance, path = dijkstra(graph, start, goal)
    if distance != float("inf"):
        print("\nShortest Path:", " -> ".join(path))
        print("Total Distance:", distance, "km")
    else:
        print("No route found.")


def main():
    graph = load_graph()

    while True:
        print("\nMenu")
        print("1. Show places")
        print("2. Find route")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            show_places(graph)
        elif choice == "2":
            find_route(graph)
            graph = load_graph()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
