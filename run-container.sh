#!/bin/bash

# run-container.sh — Build and run services with configurable ports
# You can stop it anytime with CTRL+C

set -e  # Exit immediately on errors

# Default values (can be overridden by environment variables)
export SRL_PORT=${SRL_PORT:-8000}
export LSB_PORT=${LSB_PORT:-5000}
export SRL_CONNECT_HOST=${SRL_CONNECT_HOST:-srl_service}
export SRL_CONNECT_PORT=${SRL_CONNECT_PORT:-8000}

echo "🔨 Building Docker images..."
docker compose build

echo "🚀 Starting services with configuration:"
echo "   - SRL Service: http://localhost:${SRL_PORT}"
echo "   - LSB Service: http://localhost:${LSB_PORT}"
echo "   - LSB connecting to SRL at: ${SRL_CONNECT_HOST}:${SRL_CONNECT_PORT}"
echo ""
echo "Press CTRL+C to stop"
echo

# Run container in foreground so logs are visible
docker compose up $1
