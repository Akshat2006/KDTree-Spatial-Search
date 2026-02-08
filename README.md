# SmartPOI Finder

An intelligent Point-of-Interest (POI) discovery and route planning application that combines advanced spatial search algorithms with eco-friendly routing recommendations.

## Features

- **Advanced Spatial Search**: KD-Tree implementation in C for efficient POI discovery
- ** Eco-Friendly Routing**: CO₂ emission tracking for different transport modes
- **Campus Navigation**: Custom Dijkstra-based pathfinding for RV University campus
- **Smart Location**: GPS integration with automatic campus detection
- **Dual Search Modes**: Radius-based and K-Nearest Neighbor (KNN) search

## Architecture

### 3-Tier Architecture

```
Frontend (React + Vite + Leaflet)
         ↓
Backend (Python FastAPI)
         ↓
C Core (KD-Tree Engine)
```

### Technology Stack

**Frontend:**
- React 19.2.0
- Leaflet 1.9.4 (Interactive maps)
- TailwindCSS 4.1 (Styling)
- Vite 7.2.4 (Build tool)

**Backend:**
- FastAPI (Python)
- OpenRouteService API (External routing)
- Custom Dijkstra implementation (Campus routing)

**Core:**
- C (KD-Tree spatial indexing)
- GCC compiler

## Prerequisites

- **Python** 3.8+
- **Node.js** 18+
- **GCC** compiler (MinGW for Windows)
- **OpenRouteService API Key** ([Get free key](https://openrouteservice.org/dev/#/signup))

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/smartpoi-finder.git
cd smartpoi-finder
```

### 2. Backend Setup

```bash
cd backend/python_api

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Install dependencies
pip install fastapi uvicorn requests
```

### 3. Compile C Core

```bash
cd ../c_core/src

# Windows (MinGW)
gcc -o kdtree.exe main.c kdtree.c -lm

# Linux/Mac
gcc -o kdtree main.c kdtree.c -lm
```

### 4. Frontend Setup

```bash
cd ../../../frontend

# Install dependencies
npm install
```

### 5. Environment Configuration

Create `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouteService API key:

```
ORS_API_KEY=your_actual_api_key_here
```

## Running the Application

### Start Backend

```bash
cd backend/python_api
python main.py
```

Backend runs at `http://localhost:8000`

### Start Frontend

```bash
cd frontend
npm run dev
```

Frontend runs at `http://localhost:5173`

## Usage

1. **Allow Location Access**: Grant browser permission for GPS
2. **Search POIs**: 
   - Select category (restaurants, hospitals, etc.)
   - Choose search mode (Radius or KNN)
   - Adjust search parameters
3. **Get Routes**: Click on any POI to see eco-friendly route options
4. **Compare Options**: View CO₂ emissions for different transport modes

## Project Structure

```
smartpoi-finder/
├── backend/
│   ├── c_core/
│   │   ├── src/
│   │   │   ├── main.c
│   │   │   ├── kdtree.c
│   │   │   └── kdtree.h
│   │   └── data/
│   │       ├── pois.csv
│   │       └── rv_university_campus.csv
│   └── python_api/
│       ├── main.py
│       ├── campus_paths.py
│       └── format_data.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── .env.example
├── .gitignore
└── README.md
```

## Algorithms

### KD-Tree Search
- **Construction**: O(n log n)
- **Range Search**: O(√n + k) average
- **KNN Search**: O(log n + k) average

### Dijkstra's Shortest Path
- **Time Complexity**: O((V + E) log V)
- **Use Case**: Campus road network routing

### Haversine Distance
- Calculates great-circle distance on Earth's surface
- Accuracy: ~0.5% error

## API Endpoints

### `GET /search`
Search for POIs using KD-Tree

**Parameters:**
- `lat`: Latitude
- `lon`: Longitude
- `type`: POI category
- `radius`: Search radius in km (for radius mode)
- `k`: Number of results (for KNN mode)
- `mode`: "radius" or "knn"
- `query`: Optional text filter

### `GET /route`
Get route options between two points

**Parameters:**
- `start_lat`: Start latitude
- `start_lon`: Start longitude
- `end_lat`: End latitude
- `end_lon`: End longitude

**Returns:** Array of routes with distance, duration, and CO₂ emissions

## Campus Data

The system includes detailed mapping for RV University campus:
- 27 intersection nodes
- 35+ bidirectional edges
- 60+ building mappings
- Custom pathfinding for accurate on-campus navigation

## Performance

- **POI Index Size**: ~1,156 locations (1,043 city + 113 campus)
- **Search Time**: < 10ms for typical queries
- **Build Time**: < 50ms for KD-tree construction

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenRouteService for routing API
- OpenStreetMap for map tiles
- Leaflet.js for interactive maps

## Contact

Project Link: [https://github.com/yourusername/smartpoi-finder](https://github.com/yourusername/smartpoi-finder)
