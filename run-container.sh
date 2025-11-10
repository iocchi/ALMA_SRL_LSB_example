#!/bin/bash

# manage.sh — Build and run FastAPI container in foreground mode
# You can stop it anytime with CTRL+C

set -e  # Exit immediately on errors

SERVICE_NAME="fastapi"
PORT=8000

echo "🔨 Building Docker image..."
docker compose build

echo "🚀 Starting FastAPI (press CTRL+C to stop)..."
echo "🌐 Open your browser at: http://127.0.0.1:${PORT}/docs"
echo

# Run container in foreground so logs are visible
docker compose up $1
