# Use a lightweight official Python image as base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the current directory to the container's working directory
COPY . .

# Expose port 8000 so it can be accessed from outside the container
EXPOSE 8000

# Default command (can be overridden by docker-compose)
CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "8000"]
