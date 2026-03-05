# Goal-Based Travel Route Agent

A full-stack route-planning application that finds the shortest travel path between Ethiopian cities using Dijkstra's algorithm.

The project is split into:
- `server/` (Flask API + graph/routing logic)
- `client/` (React + Vite UI)

## Why This Project
- Finds shortest routes using weighted graph traversal.
- Supports multiple destinations in a single request.
- Validates invalid cities and unreachable routes.
- Clean API-driven separation between backend decision logic and frontend UX.

## Tech Stack
- Frontend: React (Vite), CSS
- Backend: Python, Flask, Flask-CORS
- Algorithm: Dijkstra (from `server/agent.py`)
- Data Store: JSON graph (`server/graph.json`)

## Project Structure
```text
To-Do-List-Optimizer-Agent-/
├── client/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   └── package.json
└── server/
    ├── app.py
    ├── agent.py
    ├── graph.json
    └── requirements.txt
```

## How It Works
1. Frontend loads available locations from `GET /locations`.
2. User selects a start city and one or more destinations.
3. Frontend sends route request to `POST /route`.
4. Backend computes segment-by-segment shortest paths using Dijkstra.
5. API returns the merged path and total distance.

## Quick Start

### 1. Clone and enter project
```bash
git clone <your-repo-url>
cd To-Do-List-Optimizer-Agent-
```

### 2. Create and activate virtual environment (root-level)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install backend dependencies
```bash
python -m pip install -r server/requirements.txt
```

### 4. Install frontend dependencies
```bash
cd client
npm install
cd ..
```

### 5. Run backend (Port 5000)
```bash
cd server
python app.py
```

### 6. Run frontend (Vite default Port 5173)
Open a second terminal:
```bash
cd client
npm run dev
```

App URL: `http://localhost:5173`  
API URL: `http://localhost:5000`

## API Reference

### `GET /locations`
Returns all cities in the graph.

Example response:
```json
["Addis Ababa", "Adama", "Bahir Dar", "Dessie"]
```

### `POST /route`
Computes shortest route from start through all destinations in order.

Request body:
```json
{
  "start": "Addis Ababa",
  "destinations": ["Bahir Dar", "Gondar"]
}
```

Success response:
```json
{
  "success": true,
  "path": ["Addis Ababa", "Bahir Dar", "Gondar"],
  "distance": 690
}
```

Error response:
```json
{
  "success": false,
  "message": "Invalid start city: UnknownCity"
}
```

## Validation Rules
- `start` is required and must be a valid city.
- `destinations` must be a non-empty array of valid city names.
- Start city cannot be the same as any destination.
- Unreachable route segments return an error.

## CORS
Backend allows requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:5173`
- `http://127.0.0.1:5173`

## Useful Commands
- Frontend build:
```bash
cd client && npm run build
```
- Backend syntax check:
```bash
cd server && python -m py_compile agent.py app.py
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'flask'`
Your virtual environment is likely not active.
```bash
source .venv/bin/activate
python -m pip install -r server/requirements.txt
```

### `error: externally-managed-environment`
You are using system `pip` (PEP 668). Use your venv pip:
```bash
source .venv/bin/activate
python -m pip install -r server/requirements.txt
```

## Notes
- Core algorithm logic is maintained in `server/agent.py`.
- API integration is handled in `server/app.py`.
- Graph data is loaded from `server/graph.json`.
