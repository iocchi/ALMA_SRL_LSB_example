# Use Alpine Python image
FROM python:3.11-alpine

# Install packages: Python deps, bash, coreutils, ttyd, WireGuard
RUN apk add --no-cache \
    bash \
    coreutils \
    wireguard-tools \
    iproute2 \
    iptables \
    curl \
    jq \
    gcc \
    python3-dev \
    musl-dev \
    linux-headers

# Create workdir
WORKDIR /app

# Copy all files: Python code and VPN config
COPY . .

# Install Python dependencies
RUN pip install flask flask-socketio eventlet psutil

# Allow executing scripts
RUN chmod +x /app/register.sh /app/src/main.py

# make sure wireguard folder exists
RUN mkdir -p /etc/wireguard

# Entrypoint: bring up VPN then run python app
ENTRYPOINT ["/bin/bash", "-c", "sleep 6 && /app/register.sh --client lsb4 && python /app/src/main.py"]
