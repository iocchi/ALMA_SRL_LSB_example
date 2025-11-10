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

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy code into container
COPY . .

# Ensure WireGuard folder exists
RUN mkdir -p /etc/wireguard

EXPOSE 5000

# Default command (can be overridden by docker-compose)
CMD ["python", "/app/main.py", "--host", "0.0.0.0", "--port", "5000", "--srl-host", "srl_service", "--srl-port", "8000"]
