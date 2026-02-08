# Docker

## Overview

This document provides instructions for running the SmartPOI Finder using Docker. For detailed setup and troubleshooting, see [DOCKER.md](DOCKER.md).

## Quick Start with Docker

1. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your ORS_API_KEY
   ```

2. **Build and run**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Docker vs Local Development

**Local Development** (Recommended for development):
```bash
# Backend
cd backend/python_api && python main.py

# Frontend  
cd frontend && npm run dev
```

**Docker** (Recommended for production):
```bash
docker-compose up -d
```

For complete Docker documentation, see [DOCKER.md](DOCKER.md).

