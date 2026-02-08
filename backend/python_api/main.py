from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
import os
import requests
from typing import List, Optional
import heapq
from math import radians, cos, sin, asin, sqrt
from campus_paths import CAMPUS_NODES, CAMPUS_EDGES, BUILDING_TO_NODE, CAMPUS_EXITS
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

app = FastAPI(title="SmartPOI Finder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

C_EXE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../c_core/src/kdtree.exe"))
C_CWD = os.path.dirname(C_EXE_PATH)

ORS_API_KEY = os.getenv("ORS_API_KEY")
ORS_BASE_URL = "https://api.openrouteservice.org/v2/directions"

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def build_graph():
    graph = {}
    for node in CAMPUS_NODES:
        graph[node] = []
    
    for node1, node2, dist in CAMPUS_EDGES:
        graph[node1].append((node2, dist))
        graph[node2].append((node1, dist))
    
    return graph

def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == end:
            break
        
        for neighbor, weight in graph[current]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current
                heapq.heappush(pq, (distance, neighbor))
    
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    
    return path, distances[end]

def find_nearest_node(lat, lon):
    min_dist = float('inf')
    nearest = None
    for node, (node_lat, node_lon) in CAMPUS_NODES.items():
        dist = haversine(lat, lon, node_lat, node_lon)
        if dist < min_dist:
            min_dist = dist
            nearest = node
    return nearest, min_dist

def get_campus_route(start_lat, start_lon, end_lat, end_lon, start_building=None, end_building=None):
    graph = build_graph()
    
    if start_building and start_building in BUILDING_TO_NODE:
        start_node = BUILDING_TO_NODE[start_building]
    else:
        start_node, _ = find_nearest_node(start_lat, start_lon)
    
    if end_building and end_building in BUILDING_TO_NODE:
        end_node = BUILDING_TO_NODE[end_building]
    else:
        end_node, _ = find_nearest_node(end_lat, end_lon)
    
    path_nodes, total_dist_m = dijkstra(graph, start_node, end_node)
    
    path_coords = []
    path_coords.append([start_lat, start_lon])
    for node in path_nodes:
        lat, lon = CAMPUS_NODES[node]
        path_coords.append([lat, lon])
    path_coords.append([end_lat, end_lon])
    
    total_dist_km = total_dist_m / 1000.0
    total_dist_km += haversine(start_lat, start_lon, CAMPUS_NODES[path_nodes[0]][0], CAMPUS_NODES[path_nodes[0]][1])
    total_dist_km += haversine(end_lat, end_lon, CAMPUS_NODES[path_nodes[-1]][0], CAMPUS_NODES[path_nodes[-1]][1])
    
    return path_coords, total_dist_km


@app.get("/")
def read_root():
    return {"status": "active", "message": "SmartPOI Finder API - Intelligent Location Discovery"}

@app.get("/search")
def search_pois(lat: float, lon: float, type: str = "all", radius: float = 5.0, query: Optional[str] = None, mode: str = "radius", k: int = 3):
    try:
        query_str = query if query and query.strip() != "" else "NULL_QUERY"
        
        val = radius
        if mode == "knn":
            val = k
            
        cmd = [C_EXE_PATH, str(lat), str(lon), type, str(val), query_str, mode]
        
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=C_CWD,
            check=True
        )
        
        output = result.stdout.strip()
        print(f"DEBUG: C Output (First 500 chars): {output[:500]}")
        
        if not output:
            return []
            
        try:
            pois = json.loads(output)
            return pois
        except json.JSONDecodeError as e:
            print(f"JSON Error: {e}")
            print(f"Full malformed output: {output}")
            return []

    except subprocess.CalledProcessError as e:
        print(f"C Error: {e.stderr}")
        raise HTTPException(status_code=500, detail="Internal Server Error (C Module)")
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/route")
def get_route(start_lat: float, start_lon: float, end_lat: float, end_lon: float):
    CAMPUS_BOUNDS = {
        'lat_min': 12.9220,
        'lat_max': 12.9250,
        'lon_min': 77.4980,
        'lon_max': 77.5010
    }
    
    def is_on_campus(lat, lon):
        return (CAMPUS_BOUNDS['lat_min'] <= lat <= CAMPUS_BOUNDS['lat_max'] and
                CAMPUS_BOUNDS['lon_min'] <= lon <= CAMPUS_BOUNDS['lon_max'])
    
    both_on_campus = is_on_campus(start_lat, start_lon) and is_on_campus(end_lat, end_lon)
    start_on_campus = is_on_campus(start_lat, start_lon)
    end_on_campus = is_on_campus(end_lat, end_lon)
    
    if (start_on_campus and not end_on_campus) or (end_on_campus and not start_on_campus):
        pass
    
    if both_on_campus:
        try:
            path, dist_km = get_campus_route(start_lat, start_lon, end_lat, end_lon)
            
            walking_time = (dist_km / 5.0) * 60
            cycling_time = (dist_km / 15.0) * 60
            
            results = [
                {
                    "profile": "foot-walking",
                    "label": "Walking (Campus Path)",
                    "distance_km": round(dist_km, 2),
                    "duration_min": round(walking_time, 1),
                    "co2_grams": 0.0,
                    "geometry": path
                },
                {
                    "profile": "cycling-regular",
                    "label": "Cycling (Campus Path)",
                    "distance_km": round(dist_km, 2),
                    "duration_min": round(cycling_time, 1),
                    "co2_grams": 0.0,
                    "geometry": path
                }
            ]
            
            return results
        except Exception as e:
            print(f"Campus routing error: {e}")
            dist_km = haversine(start_lat, start_lon, end_lat, end_lon)
            walking_time = (dist_km / 5.0) * 60
            cycling_time = (dist_km / 15.0) * 60
            path = [[start_lat, start_lon], [end_lat, end_lon]]
            
            results = [
                {
                    "profile": "foot-walking",
                    "label": "Walking (Direct)",
                    "distance_km": round(dist_km, 2),
                    "duration_min": round(walking_time, 1),
                    "co2_grams": 0.0,
                    "geometry": path
                },
                {
                    "profile": "cycling-regular",
                    "label": "Cycling (Direct)",
                    "distance_km": round(dist_km, 2),
                    "duration_min": round(cycling_time, 1),
                    "co2_grams": 0.0,
                    "geometry": path
                }
            ]
            
            return results
    
    profiles = {
        "driving-car": {"label": "Car", "emission_factor": 120.0},
        "cycling-regular": {"label": "Cycling", "emission_factor": 0.0},
        "foot-walking": {"label": "Walking", "emission_factor": 0.0}
    }
    
    results = []
    
    headers = {
        'Authorization': ORS_API_KEY,
        'Content-Type': 'application/json'
    }
    
    for profile, info in profiles.items():
        try:
            url = f"{ORS_BASE_URL}/{profile}"
            params = {
                "api_key": ORS_API_KEY,
                "start": f"{start_lon},{start_lat}",
                "end": f"{end_lon},{end_lat}"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                feature = data['features'][0]
                props = feature['properties']
                geometry = feature['geometry']['coordinates']
                
                path = [[p[1], p[0]] for p in geometry]
                
                dist_m = props['summary']['distance']
                dur_s = props['summary']['duration']
                
                dist_km = dist_m / 1000.0
                dur_min = dur_s / 60.0
                
                co2 = dist_km * info['emission_factor']
                
                results.append({
                    "profile": profile,
                    "label": info['label'],
                    "distance_km": round(dist_km, 2),
                    "duration_min": round(dur_min, 1),
                    "co2_grams": round(co2, 1),
                    "geometry": path
                })
            else:
                print(f"ORS Error {profile}: {response.text}")
                pass

        except Exception as e:
            print(f"Exception for {profile}: {e}")

    if not results:
        print("Using fallback routing (API unavailable)")
        dist_km = haversine(start_lat, start_lon, end_lat, end_lon)
        
        results = [
            {
                "profile": "foot-walking",
                "label": "Walking (Estimated)",
                "distance_km": round(dist_km, 2),
                "duration_min": round((dist_km / 5.0) * 60, 1),
                "co2_grams": 0.0,
                "geometry": [[start_lat, start_lon], [end_lat, end_lon]]
            },
            {
                "profile": "cycling-regular",
                "label": "Cycling (Estimated)",
                "distance_km": round(dist_km, 2),
                "duration_min": round((dist_km / 15.0) * 60, 1),
                "co2_grams": 0.0,
                "geometry": [[start_lat, start_lon], [end_lat, end_lon]]
            },
            {
                "profile": "driving-car",
                "label": "Car (Estimated)",
                "distance_km": round(dist_km, 2),
                "duration_min": round((dist_km / 40.0) * 60, 1),
                "co2_grams": round(dist_km * 120, 1),
                "geometry": [[start_lat, start_lon], [end_lat, end_lon]]
            }
        ]

    results.sort(key=lambda x: x['co2_grams'])
    
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
