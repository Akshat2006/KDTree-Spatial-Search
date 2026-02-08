# Quick Docker Commands Reference

## Port Configuration

### Frontend
- Container Port: 80 (nginx)
- Host Port: 3000
- URL: http://localhost:3000

### Backend  
- Container Port: 8000 (FastAPI)
- Host Port: 8000
- URL: http://localhost:8000
- API Docs: http://localhost:8000/docs

## How to Run

### First Time Setup
```powershell
# 1. Configure environment
cp .env.example .env
notepad .env  # Add your ORS_API_KEY

# 2. Build and start
docker-compose up --build

# 3. Access the app
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Daily Use

```powershell
# Start (in foreground, see logs)
docker-compose up

# Start (in background, detached)
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart

# Rebuild after code changes
docker-compose up --build
```

### Useful Commands

```powershell
# Check running containers
docker-compose ps

# Check container health
docker ps

# Stop and remove everything (including volumes)
docker-compose down -v

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh

# View resource usage
docker stats

# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune
```

## Changing Ports

If you need different ports, edit `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8080:8000"  # Change 8080 to any available port
  
  frontend:
    ports:
      - "3001:80"    # Change 3001 to any available port
```

Then restart:
```powershell
docker-compose down
docker-compose up -d
```

## Troubleshooting

### Port Already in Use
```powershell
# Check what's using port 3000
netstat -ano | findstr :3000

# Kill process (if needed)
taskkill /PID <process_id> /F

# Or change port in docker-compose.yml
```

### Container Won't Start
```powershell
# View logs
docker-compose logs backend

# Check if .env file exists
ls .env

# Rebuild
docker-compose up --build
```

### Can't Access Frontend
```powershell
# Check if container is running
docker-compose ps

# Check nginx logs
docker-compose logs frontend

# Verify port mapping
docker ps
```

### Backend API Not Responding
```powershell
# Check if backend is healthy
curl http://localhost:8000

# View backend logs
docker-compose logs backend

# Check if C executable compiled
docker-compose exec backend ls -la /app/c_core/src/kdtree
```

## Quick Start (Copy-Paste)

```powershell
# Complete setup in one go
cp .env.example .env
# (Edit .env manually to add ORS_API_KEY)
docker-compose up --build -d
docker-compose logs -f
```

## Access URLs

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000  
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Redoc**: http://localhost:8000/redoc

## Development vs Docker

### Local Development
```powershell
# Backend
cd backend/python_api
python main.py

# Frontend (separate terminal)
cd frontend
npm run dev
```
- Backend: http://localhost:8000
- Frontend: http://localhost:5173 (Vite dev server)

### Docker (Production)
```powershell
docker-compose up -d
```
- Backend: http://localhost:8000
- Frontend: http://localhost:3000 (nginx)

## Next Steps

1. ✅ Ensure Docker Desktop is running
2. ✅ Set ORS_API_KEY in `.env` file
3. ✅ Run: `docker-compose up --build`
4. ✅ Open: http://localhost:3000
5. ✅ Test POI search and routing
