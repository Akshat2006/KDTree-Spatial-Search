# Docker Deployment Guide

This guide explains how to run the SmartPOI Finder application using Docker.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+

## Quick Start

### 1. Configure Environment Variables

Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouteService API key:

```
ORS_API_KEY=your_actual_api_key_here
```

### 2. Build and Run

Build and start all services:

```bash
docker-compose up --build
```

Or run in detached mode:

```bash
docker-compose up -d --build
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Docker Services

### Backend Service
- **Image**: Built from `./backend/Dockerfile`
- **Ports**: 8000
- **Components**:
  - C Core (KD-Tree compiled with GCC)
  - Python FastAPI server

### Frontend Service
- **Image**: Built from `./frontend/Dockerfile` (Multi-stage build)
- **Ports**: 3000 (nginx)
- **Build**: Node.js → Production build → nginx

## Docker Commands

### Start Services
```bash
docker-compose up
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Rebuild Services
```bash
docker-compose up --build
```

### Check Service Health
```bash
docker-compose ps
```

### Remove Containers and Volumes
```bash
docker-compose down -v
```

## Development vs Production

### Development Mode
For development, continue using the local setup:
```bash
# Backend
cd backend/python_api
python main.py

# Frontend
cd frontend
npm run dev
```

### Production Mode
Use Docker for production deployments:
```bash
docker-compose up -d
```

## Troubleshooting

### Port Conflicts
If ports 3000 or 8000 are already in use, modify the port mappings in `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8080:8000"  # Change 8080 to any available port
  frontend:
    ports:
      - "3001:80"    # Change 3001 to any available port
```

### Backend Not Starting
Check if the C executable compiled correctly:
```bash
docker-compose logs backend
```

### Frontend Can't Connect to Backend
Ensure the backend service is healthy:
```bash
docker-compose ps
```

Check backend logs:
```bash
docker-compose logs backend
```

### Data Volume Issues
If POI data is missing, ensure the volume mount is correct:
```bash
ls backend/c_core/data/
```

## Architecture

```
┌─────────────────────────────────────────┐
│         User's Browser                  │
│         http://localhost:3000           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      nginx (Frontend Container)         │
│      - Serves React SPA                 │
│      - Proxies /api → backend:8000      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│     FastAPI (Backend Container)         │
│     - Python API server                 │
│     - Calls C executable                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│     C Core (Compiled in Backend)        │
│     - KD-Tree spatial search            │
│     - Reads CSV data files              │
└─────────────────────────────────────────┘
```

## Environment Variables

### Backend (.env)
- `ORS_API_KEY`: Your OpenRouteService API key (required)

### Frontend
- `VITE_API_URL`: Backend API URL (auto-configured)

## Network Configuration

Docker Compose creates a custom network `smartpoi-network` allowing services to communicate using service names:
- Backend accessible at `http://backend:8000` from frontend container
- Frontend proxies API requests to backend

## Health Checks

Both services include health checks:

**Backend**: HTTP GET to `/`
**Frontend**: HTTP GET via wget

Services automatically restart if health checks fail.

## Building for Different Platforms

### ARM64 (Apple Silicon, Raspberry Pi)
```bash
docker-compose build --platform linux/arm64
```

### AMD64 (Intel/AMD)
```bash
docker-compose build --platform linux/amd64
```

## Production Deployment

For production deployment on cloud platforms:

1. Use a reverse proxy (nginx/Traefik) with SSL
2. Set up proper logging and monitoring
3. Use Docker secrets for API keys
4. Configure resource limits in docker-compose.yml
5. Use a container orchestration platform (Kubernetes, Docker Swarm)

## Support

For issues and questions, check:
- Application logs: `docker-compose logs`
- Backend health: http://localhost:8000
- Container status: `docker-compose ps`
