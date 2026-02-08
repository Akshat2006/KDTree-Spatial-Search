@echo off
REM SmartPOI Finder - Docker Quick Start Script (Windows)
REM This script helps you quickly deploy the application using Docker

echo.
echo ===================================================================
echo   SmartPOI Finder - Docker Deployment
echo ===================================================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [OK] Docker is running
echo.

REM Check if .env exists
if not exist .env (
    echo [WARNING] .env file not found!
    echo Creating .env from template...
    
    if exist .env.example (
        copy .env.example .env >nul
        echo [OK] .env file created
        echo.
        echo [IMPORTANT] Edit .env and add your ORS_API_KEY
        echo Get a free key at: https://openrouteservice.org/dev/#/signup
        echo.
        echo Opening .env in notepad...
        notepad .env
        echo.
        pause
    ) else (
        echo [ERROR] .env.example not found!
        pause
        exit /b 1
    )
) else (
    echo [OK] .env file found
)

REM Check if API key is configured
findstr /C:"your_actual_api_key_here" .env >nul 2>&1
if not errorlevel 1 (
    echo.
    echo [WARNING] ORS_API_KEY not configured in .env
    echo The application may not work correctly without it.
    echo.
    set /p CONTINUE="Continue anyway? (y/N): "
    if /i not "%CONTINUE%"=="y" exit /b 1
)

echo.
echo ===================================================================
echo   Building and Starting Docker Containers
echo ===================================================================
echo.
echo This may take a few minutes on first run...
echo.

REM Build and start containers
docker-compose up --build

echo.
echo ===================================================================
echo   Deployment Complete!
echo ===================================================================
echo.
pause
