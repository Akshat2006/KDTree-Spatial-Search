#!/bin/bash

# SmartPOI Finder - Docker Quick Start Script
# This script helps you quickly deploy the application using Docker

set -e  # Exit on error

echo "🚀 SmartPOI Finder - Docker Deployment"
echo "======================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running!"
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo "✅ Docker is running"

# Check if .env exists
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  .env file not found!"
    echo "Creating .env from template..."
    
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env file created"
        echo ""
        echo "⚠️  IMPORTANT: Edit .env and add your ORS_API_KEY"
        echo "   Get a free key at: https://openrouteservice.org/dev/#/signup"
        echo ""
        read -p "Press Enter after you've added your API key to .env..."
    else
        echo "❌ Error: .env.example not found!"
        exit 1
    fi
else
    echo "✅ .env file found"
fi

# Check if ORS_API_KEY is set
if grep -q "your_actual_api_key_here" .env; then
    echo ""
    echo "⚠️  WARNING: ORS_API_KEY not configured in .env"
    echo "   The application may not work correctly without it."
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Parse command line arguments
BUILD=true
DETACHED=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --no-build)
            BUILD=false
            shift
            ;;
        -d|--detached)
            DETACHED=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--no-build] [-d|--detached]"
            exit 1
            ;;
    esac
done

# Build and start containers
echo ""
echo "🐳 Starting Docker containers..."
echo ""

if [ "$BUILD" = true ]; then
    echo "Building images (this may take a few minutes)..."
    
    if [ "$DETACHED" = true ]; then
        docker-compose up --build -d
    else
        docker-compose up --build
    fi
else
    if [ "$DETACHED" = true ]; then
        docker-compose up -d
    else
        docker-compose up
    fi
fi

# If running in detached mode, show status
if [ "$DETACHED" = true ]; then
    echo ""
    echo "✅ Containers started in background"
    echo ""
    echo "📊 Container Status:"
    docker-compose ps
    
    echo ""
    echo "🌐 Access Points:"
    echo "   Frontend:  http://localhost:3000"
    echo "   Backend:   http://localhost:8000"
    echo "   API Docs:  http://localhost:8000/docs"
    
    echo ""
    echo "📋 Useful Commands:"
    echo "   View logs:       docker-compose logs -f"
    echo "   Stop services:   docker-compose down"
    echo "   Restart:         docker-compose restart"
fi
