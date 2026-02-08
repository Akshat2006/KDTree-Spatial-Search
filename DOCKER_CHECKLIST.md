# Docker Setup Verification Checklist

Use this checklist to verify your Docker setup is working correctly.

## Pre-Flight Checklist

- [ ] Docker Engine installed (`docker --version`)
- [ ] Docker Compose installed (`docker-compose --version`)
- [ ] `.env` file created from `.env.example`
- [ ] ORS_API_KEY added to `.env` file
- [ ] All Docker files present:
  - [ ] `docker-compose.yml`
  - [ ] `backend/Dockerfile`
  - [ ] `frontend/Dockerfile`
  - [ ] `frontend/nginx.conf`

## Build and Start

```bash
# 1. Build and start containers
docker-compose up --build

# Expected output:
# ✓ Building backend...
# ✓ Building frontend...
# ✓ Creating network "smartpoi-network"
# ✓ Creating smartpoi-backend...
# ✓ Creating smartpoi-frontend...
```

- [ ] Backend builds successfully
- [ ] Frontend builds successfully
- [ ] Both containers start without errors

## Health Checks

### Backend Health
```bash
# Check if backend is running
curl http://localhost:8000

# Expected response:
# {"status":"active","message":"SmartPOI Finder API - Intelligent Location Discovery"}
```

- [ ] Backend responds at port 8000
- [ ] Status shows "active"

### Frontend Health
```bash
# Check if frontend is accessible
curl http://localhost:3000

# Expected: HTML content of React app
```

- [ ] Frontend loads at port 3000
- [ ] HTML contains React app markup

### Container Status
```bash
docker-compose ps

# Expected output:
# NAME                   STATUS              PORTS
# smartpoi-backend       Up (healthy)        0.0.0.0:8000->8000/tcp
# smartpoi-frontend      Up (healthy)        0.0.0.0:3000->80/tcp
```

- [ ] Both containers show "Up (healthy)"
- [ ] Ports are correctly mapped

## Functional Tests

### 1. Frontend UI Test
- [ ] Open http://localhost:3000 in browser
- [ ] Map loads correctly
- [ ] Location permission prompt appears
- [ ] Sidebar shows "SmartPOI Finder" title
- [ ] Search filters are visible

### 2. API Documentation Test
- [ ] Open http://localhost:8000/docs
- [ ] Swagger UI loads
- [ ] `/search` and `/route` endpoints listed

### 3. POI Search Test
Via browser at http://localhost:3000:
- [ ] Allow location access
- [ ] Select category (e.g., "Restaurant")
- [ ] Set search mode to "Radius"
- [ ] POI markers appear on map
- [ ] POI list shows in sidebar

### 4. Route Calculation Test
- [ ] Click on any POI in the list
- [ ] Route details appear in sidebar
- [ ] Route options show (Walking, Cycling, Car)
- [ ] CO₂ emissions displayed
- [ ] Route line appears on map

### 5. API Direct Test
```bash
# Test POI search
curl "http://localhost:8000/search?lat=12.923365&lon=77.501078&type=restaurant&radius=5&mode=radius"

# Expected: JSON array of POI results
```

- [ ] API returns JSON response
- [ ] POIs have name, lat, lon, type fields

```bash
# Test routing
curl "http://localhost:8000/route?start_lat=12.923365&start_lon=77.501078&end_lat=12.925&end_lon=77.502"

# Expected: JSON array with route options
```

- [ ] API returns route options
- [ ] Each route has distance, duration, co2_grams

## Network and Logs

### View Logs
```bash
# All logs
docker-compose logs -f

# Backend logs only
docker-compose logs -f backend

# Frontend logs only
docker-compose logs -f frontend
```

- [ ] No error messages in logs
- [ ] Backend shows successful C executable compilation
- [ ] Frontend shows successful build

### Network Inspection
```bash
docker network inspect smartpoi-network
```

- [ ] Network exists
- [ ] Both containers connected

## Stop and Clean Up

```bash
# Stop containers
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

- [ ] Containers stop gracefully
- [ ] No error messages

## Troubleshooting

### If Backend Fails
1. Check logs: `docker-compose logs backend`
2. Verify C compilation: `docker-compose exec backend ls -la /app/c_core/src/`
3. Verify data files: `docker-compose exec backend ls -la /app/c_core/data/`
4. Check .env file: `cat .env` (ensure ORS_API_KEY is set)

### If Frontend Fails
1. Check logs: `docker-compose logs frontend`
2. Verify nginx config: `docker-compose exec frontend cat /etc/nginx/conf.d/default.conf`
3. Check build: `docker-compose exec frontend ls -la /usr/share/nginx/html/`

### If API Calls Fail
1. Check backend health: `curl http://localhost:8000`
2. Check nginx proxy: `docker-compose exec frontend cat /etc/nginx/conf.d/default.conf`
3. Verify network: `docker network inspect smartpoi-network`

## Performance Tests

```bash
# Time to build
time docker-compose build

# Memory usage
docker stats --no-stream

# Container sizes
docker images | grep smartpoi
```

- [ ] Build completes in < 5 minutes
- [ ] Backend memory < 500MB
- [ ] Frontend memory < 50MB
- [ ] Frontend image < 100MB
- [ ] Backend image < 500MB

## Final Verification

- [ ] ✅ All containers running and healthy
- [ ] ✅ Frontend accessible at http://localhost:3000
- [ ] ✅ Backend accessible at http://localhost:8000
- [ ] ✅ POI search working
- [ ] ✅ Route calculation working
- [ ] ✅ Map displaying correctly
- [ ] ✅ No errors in browser console
- [ ] ✅ No errors in Docker logs

## Success! 🎉

If all checks pass, your Docker setup is complete and working correctly!

Next steps:
1. Read [DOCKER.md](DOCKER.md) for detailed documentation
2. Customize as needed for your deployment
3. Consider setting up CI/CD for automated builds
4. Deploy to production server if ready

## Notes

- First build will take longer (downloading base images)
- Subsequent builds use cached layers (faster)
- Data files are mounted read-only for safety
- Containers auto-restart unless manually stopped
