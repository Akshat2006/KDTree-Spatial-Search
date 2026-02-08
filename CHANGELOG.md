# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-07

### Added
- **KD-Tree Spatial Search**: Efficient C implementation for POI discovery
- **Dual Search Modes**: Radius-based and K-Nearest Neighbor searches
- **Campus Navigation**: Custom Dijkstra pathfinding for RV University campus
- **Eco-Friendly Routing**: CO₂ emission tracking for different transport modes
- **GPS Integration**: Real-time location tracking with automatic campus detection
- **Interactive Map**: Leaflet-based visualization with custom markers
- **Multi-Modal Routes**: Walking, cycling, and driving options
- **Smart Location Snapping**: Auto-snap to campus main gate when on campus
- **Custom Start Points**: Click-to-set location feature
- **Category Filtering**: 12+ POI categories including restaurants, hospitals, schools
- **Text Search**: Query-based filtering of locations
- **OpenRouteService Integration**: Real-world road routing for external locations

### Features
- 1,156 indexed locations (1,043 city + 113 campus)
- 27 campus road network nodes with 35+ edges
- Real-time GPS tracking with position watching
- Campus boundary detection
- Route comparison with emission metrics
- Responsive dark-themed UI with glassmorphism effects
- Sub-10ms search performance

### Technical Highlights
- 3-tier architecture (React + FastAPI + C)
- O(log n) average search complexity
- Haversine distance calculations for accuracy
- Priority queue-based KNN search
- Graph-based campus pathfinding

## [Unreleased]

### Planned
- Multi-language support
- Offline mode with cached data
- Route history and favorites
- Additional campus maps
- Mobile app version
- Real-time traffic integration
- Public transport routing
- Accessibility features
