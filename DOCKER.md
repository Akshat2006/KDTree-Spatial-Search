# Docker Deployment Guide

## 🐳 Complete Docker Setup for SmartPOI Finder

This guide covers the complete Docker deployment of the SmartPOI Finder application with all recent updates including the improved campus routing system.

---

## 📋 Prerequisites

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Docker Compose** v2.0+
- **8GB RAM minimum** recommended
- **OpenRouteService API Key** ([Get free key](https://openrouteservice.org/dev/#/signup))

---

## 🚀 Quick Start

### 1. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API key
notepad .env  # Windows
# OR
nano .env     # Linux/Mac
```

Add your OpenRouteService API key:
```
ORS_API_KEY=your_actual_api_key_here
```

### 2. Build and Run

```bash
# Build and start all services
docker-compose up --build

# OR run in detached mode (background)
docker-compose up --build -d
```

### 3. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 📦 Architecture

```
┌─────────────────────────────────────────┐
│         Docker Compose Network          │
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   Frontend   │    │   Backend    │  │
│  │  (Nginx:80)  │◄───┤ (FastAPI)    │  │
│  │   Port 3000  │    │  Port 8000   │  │
│  └──────────────┘    └──────────────┘  │
│         │                    │          │
│         │                    │          │
│         ▼                    ▼          │
│    dist/ (built)      C Exec + Python  │
│                                         │
└─────────────────────────────────────────┘
```

### Services

#### Backend Container
- **Base**: `python:3.11-slim`
- **Compiles**: C KD-Tree engine
- **Runs**: FastAPI server with Uvicorn
- **Includes**: Campus routing with 50+ road nodes
- **Port**: 8000

#### Frontend Container
- **Build**: Node 18 Alpine (multi-stage)
- **Serve**: Nginx Alpine
- **Port**: 80 (mapped to 3000)

---

## 🛠️ Docker Commands

### Basic Operations

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs (all services)
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart

# Rebuild after code changes
docker-compose up --build
```

### Container Management

```bash
# List running containers
docker-compose ps

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh

# View resource usage
docker stats

# Remove everything (containers, networks, volumes)
docker-compose down -v
```

### Debugging

```bash
# Check container health
docker ps

# View container logs (last 100 lines)
docker-compose logs --tail=100 backend

# Follow logs in real-time
docker-compose logs -f backend

# Check if C executable compiled
docker-compose exec backend ls -la /app/c_core/src/

# Test backend endpoint
curl http://localhost:8000/
```

---

## 📝 Configuration Files

### docker-compose.yml
Orchestrates both services with:
- Environment variables
- Port mappings
- Volume mounts
- Health checks
- Network configuration

### Backend Dockerfile
1. Installs GCC and build tools
2. Compiles C KD-Tree engine
3. Installs Python dependencies
4. Copies Python API code
5. Exposes port 8000

### Frontend Dockerfile (Multi-stage)
**Stage 1 (Builder):**
- Uses Node 18 Alpine
- Installs dependencies
- Builds production bundle

**Stage 2 (Production):**
- Uses Nginx Alpine
- Copies built files
- Serves on port 80

### nginx.conf
- Serves static React app
- Proxies `/api` requests to backend
- Enables gzip compression
- Handles SPA routing

---

## 🔧 Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `ORS_API_KEY` | OpenRouteService API key | `5e3ce359-87...` |

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_PORT` | `8000` | Backend API port |
| `FRONTEND_PORT` | `3000` | Frontend web port |

---

## 🐛 Troubleshooting

### Port Already in Use

**Error**: `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solution**:
```bash
# Find process using port
netstat -ano | findstr :3000     # Windows
lsof -i :3000                    # Linux/Mac

# Kill process or change port in docker-compose.yml
ports:
  - "3001:80"  # Use different host port
```

### Backend Won't Start

**Check**:
1. C executable compiled correctly
2. Python dependencies installed
3. Environment variables loaded

```bash
# View backend logs
docker-compose logs backend

# Check C compilation
docker-compose exec backend ls -la /app/c_core/src/kdtree

# Verify environment
docker-compose exec backend env | grep ORS
```

### Frontend Shows 404

**Check**:
1. Build completed successfully
2. Nginx configuration loaded
3. Dist files copied

```bash
# Rebuild frontend
docker-compose up --build frontend

# Check nginx config
docker-compose exec frontend cat /etc/nginx/conf.d/default.conf

# Verify dist files
docker-compose exec frontend ls -la /usr/share/nginx/html/
```

### API Requests Failing

**Check**:
1. Backend is running
2. Network connectivity
3. CORS configuration

```bash
# Test backend directly
curl http://localhost:8000/

# Check backend health
docker-compose ps backend

# View backend logs
docker-compose logs -f backend
```

---

## 🔄 Development vs Production

### Development (Local)
```bash
# Backend
cd backend/python_api
python main.py

# Frontend
cd frontend
npm run dev
```
- Backend: http://localhost:8000
- Frontend: http://localhost:5173 (Vite dev server)
- ✅ Hot reload
- ✅ Source maps
- ✅ Fast iteration

### Production (Docker)
```bash
docker-compose up -d
```
- Backend: http://localhost:8000
- Frontend: http://localhost:3000 (Nginx)
- ✅ Optimized build
- ✅ Production-ready
- ✅ Auto-restart
- ✅ Health monitoring

---

## 📊 Health Checks

Both services have health checks configured:

### Backend
```yaml
test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/')"]
interval: 30s
timeout: 10s
retries: 3
```

### Frontend
```yaml
test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:80"]
interval: 30s
timeout: 10s
retries: 3
```

**Check Status**:
```bash
docker-compose ps
# Look for "healthy" status
```

---

## 🔐 Security Best Practices

1. **Never commit** `.env` file
2. **Use** `.env.example` for templates
3. **Rotate** API keys regularly
4. **Run** containers as non-root (add in Dockerfiles if needed)
5. **Scan** images for vulnerabilities:
   ```bash
   docker scan smartpoi-backend
   docker scan smartpoi-frontend
   ```

---

## 📦 Volume Mounts

Currently mounting:
```yaml
volumes:
  - ./backend/c_core/data:/app/c_core/data:ro
```

This allows:
- **Hot reloading** of POI data without rebuilding
- **Read-only** mount for security
- **Easy updates** to campus/POI data

---

## 🚢 Deployment Options

### Option 1: Docker Hub

```bash
# Tag images
docker tag smartpoi-backend yourusername/smartpoi-backend:latest
docker tag smartpoi-frontend yourusername/smartpoi-frontend:latest

# Push to Docker Hub
docker push yourusername/smartpoi-backend:latest
docker push yourusername/smartpoi-frontend:latest
```

### Option 2: Cloud Platforms

- **AWS ECS**: Elastic Container Service
- **Google Cloud Run**: Serverless containers
- **Azure Container Instances**: Simple container hosting
- **DigitalOcean App Platform**: PaaS deployment

### Option 3: VPS with Docker Compose

```bash
# On VPS
git clone https://github.com/yourusername/smartpoi-finder.git
cd smartpoi-finder
cp .env.example .env
# Edit .env with production values
docker-compose up -d
```

---

## 📈 Performance Optimization

### Image Size Reduction

```dockerfile
# Use Alpine variants
FROM python:3.11-alpine
FROM node:18-alpine

# Multi-stage builds (already implemented)
# Clean up in same RUN command
RUN apt-get update && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/*
```

### Caching

```dockerfile
# Copy dependencies first (better caching)
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .  # Copy code last
```

---

## 🔢 Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      replicas: 3  # Run 3 backend instances
    
  # Add load balancer
  nginx-lb:
    image: nginx:alpine
    volumes:
      - ./lb.conf:/etc/nginx/nginx.conf
    ports:
      - "8000:8000"
```

---

## 📚 Additional Resources

- **Docker Docs**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **Best Practices**: https://docs.docker.com/develop/dev-best-practices/
- **OpenRouteService**: https://openrouteservice.org/dev/

---

## ✅ Verification Checklist

- [ ] `.env` file configured with API key
- [ ] Docker Desktop/Engine running
- [ ] Ports 3000 and 8000 available
- [ ] Images build successfully
- [ ] Containers start without errors
- [ ] Health checks pass
- [ ] Frontend accessible at http://localhost:3000
- [ ] Backend API docs at http://localhost:8000/docs
- [ ] POI search works
- [ ] Campus routing works
- [ ] Routes follow white roads

---

## 🆘 Support

If you encounter issues:

1. **Check logs**: `docker-compose logs -f`
2. **Verify health**: `docker-compose ps`
3. **Test endpoints**: `curl http://localhost:8000/`
4. **Rebuild**: `docker-compose up --build`
5. **Clean start**: `docker-compose down -v && docker-compose up --build`

---

**Last Updated**: 2026-02-09
**Version**: 2.0 (with improved campus routing)
