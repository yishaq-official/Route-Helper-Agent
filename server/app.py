from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS

import agent

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "http://localhost:5173",
                "http://127.0.0.1:5173",
            ]
        }
    },
)

# Ensure graph.json is resolved relative to this server directory.
agent.GRAPH_FILE = Path(__file__).resolve().with_name("graph.json")


def error_response(message, status_code=400):
    return jsonify({"success": False, "message": message}), status_code


def safe_load_graph():
    try:
        graph = agent.load_graph()
        if not isinstance(graph, dict) or not graph:
            raise ValueError("Graph data is empty or invalid.")
        return graph, None
    except Exception as exc:  # pragma: no cover - defensive boundary
        return None, str(exc)


def sanitize_route_payload(payload):
    if not isinstance(payload, dict):
        return None, None, "Request body must be valid JSON."

    start = payload.get("start")
    destinations = payload.get("destinations")

    if not isinstance(start, str) or not start.strip():
        return None, None, "Field 'start' is required."

    if not isinstance(destinations, list) or not destinations:
        return None, None, "Field 'destinations' must be a non-empty list."

    normalized_destinations = []
    for destination in destinations:
        if not isinstance(destination, str) or not destination.strip():
            return None, None, "Each destination must be a non-empty string."
        normalized_destinations.append(destination.strip())

    return start.strip(), normalized_destinations, None


def compute_route(graph, start, destinations):
    total_distance = 0
    full_path = [start]
    current_city = start

    for destination in destinations:
        segment_distance, segment_path = agent.dijkstra(graph, current_city, destination)

        if segment_distance == float("inf") or not segment_path:
            return None, None, destination

        total_distance += segment_distance
        full_path.extend(segment_path[1:])
        current_city = destination

    return full_path, total_distance, None


@app.get("/locations")
def get_locations():
    graph, error = safe_load_graph()
    if error:
        return error_response("Unable to load locations.", 500)

    return jsonify(sorted(graph.keys()))


@app.post("/route")
def post_route():
    graph, error = safe_load_graph()
    if error:
        return error_response("Unable to load graph data.", 500)

    start, destinations, payload_error = sanitize_route_payload(request.get_json(silent=True))
    if payload_error:
        return error_response(payload_error, 400)

    if start not in graph:
        return error_response(f"Invalid start city: {start}", 400)

    invalid_destinations = [city for city in destinations if city not in graph]
    if invalid_destinations:
        return error_response(
            "Invalid destination city/cities: " + ", ".join(invalid_destinations), 400
        )

    if any(city == start for city in destinations):
        return error_response("Start and destination cannot be the same.", 400)

    route_path, route_distance, unreachable_destination = compute_route(
        graph, start, destinations
    )
    if unreachable_destination:
        return error_response(
            f"No reachable route to destination: {unreachable_destination}", 400
        )

    return jsonify({"success": True, "path": route_path, "distance": route_distance})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
