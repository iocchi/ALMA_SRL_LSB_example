#!/bin/bash

# run-container.sh — Build and run services with configurable ports
# You can stop it anytime with CTRL+C

set -e  # Exit immediately on errors

# Default values (can be overridden by environment variables)
export SRL_HOST=srl   # local docker service
export SRL_PORT=${SRL_PORT:-5000}

# if using public fake SRL
#export SRL_HOST=151.100.59.107
#export SRL_PORT=9890

export LSB1_PORT=5010
export LSB2_PORT=5020
export LSB2_WS_PORT=5021
export LSB3_PORT=5030
export LSB4_PORT=5040


echo "🔨 Building Docker images..."
docker compose build

echo "🚀 Starting services with configuration:"
echo "   - SRL Service: http://localhost:${SRL_PORT}/<service_name>"
echo "   - LSB connecting to SRL at: ${SRL_HOST}:${SRL_PORT}"
echo "   - LSB1 Services: http://localhost:${LSB1_PORT}"
echo "   - LSB2 Services: http://localhost:${LSB2_PORT},${LSB2_WS_PORT}"
echo "   - LSB3 Services: http://localhost:${LSB3_PORT}"
echo "   - LSB4 Services: http://localhost:${LSB4_PORT}"
echo ""
echo "Press CTRL+C to stop"
echo

# Run container in foreground so logs are visible
docker compose up $1 --remove-orphans

