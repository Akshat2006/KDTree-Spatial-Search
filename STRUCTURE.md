# Project Structure

This document provides a detailed overview of the SmartPOI Finder project structure.

## Root Directory

```
smartpoi-finder/
├── backend/           # Backend services
├── frontend/          # React frontend application
├── .env.example       # Environment variable template
├── .gitignore         # Git ignore rules
├── LICENSE            # MIT License
├── README.md          # Project documentation
├── CONTRIBUTING.md    # Contribution guidelines
└── PROJECT_SUMMARY.md # Comprehensive project summary
```

## Backend Structure

```
backend/
├── c_core/
│   ├── src/
│   │   ├── kdtree.h       # KD-tree header file
│   │   ├── kdtree.c       # KD-tree implementation
│   │   ├── main.c         # C executable entry point
│   │   └── kdtree.exe     # Compiled executable (gitignored)
│   └── data/
│       ├── pois.csv                  # City POI dataset (~1043 locations)
│       └── rv_university_campus.csv  # Campus POI dataset (~113 locations)
└── python_api/
    ├── main.py          # FastAPI application
    ├── campus_paths.py  # Campus graph data and Dijkstra implementation
    └── format_data.py   # Data processing utilities
```

## Frontend Structure

```
frontend/
├── src/
│   ├── App.jsx        # Main React component
│   ├── main.jsx       # React entry point
│   └── index.css      # Global styles
├── public/            # Static assets
├── index.html         # HTML template
├── package.json       # Node dependencies
├── vite.config.js     # Vite configuration
├── tailwind.config.js # TailwindCSS configuration
└── postcss.config.js  # PostCSS configuration
```

## Key Files

### Configuration Files
- **`.env.example`**: Template for environment variables
- **`.gitignore`**: Specifies intentionally untracked files
- **`package.json`**: Node.js project metadata and dependencies

### Documentation Files
- **`README.md`**: Main project documentation
- **`PROJECT_SUMMARY.md`**: Detailed technical documentation
- **`CONTRIBUTING.md`**: Guidelines for contributors
- **`LICENSE`**: MIT License

### Data Files
- **`pois.csv`**: Main POI dataset (Bangalore area)
- **`rv_university_campus.csv`**: Campus-specific locations

## Technologies by Layer

### Frontend Layer
- React 19.2.0
- Leaflet 1.9.4
- TailwindCSS 4.1
- Vite 7.2.4

### Backend Layer
- Python FastAPI
- C (GCC compiled)
- OpenRouteService API

### Data Layer
- CSV files
- KD-Tree spatial index
- Campus graph structure
