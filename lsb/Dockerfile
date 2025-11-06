# Use Alpine Python image
FROM python:3.11-alpine

# Install system packages
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

# Create working directory
WORKDIR /app

# Copy code into container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir flask flask-socketio eventlet psutil

# Ensure WireGuard folder exists
RUN mkdir -p /etc/wireguard

EXPOSE 5000


# Run your main.py directly
ENTRYPOINT ["python", "/app/main.py"]
