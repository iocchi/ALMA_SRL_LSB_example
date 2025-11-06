# Use a lightweight official Python image as base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to the container's working directory

COPY . .

# Install FastAPI and Uvicorn (the ASGI server)
RUN pip install --no-cache-dir fastapi uvicorn

# Expose port 8000 so it can be accessed from outside the container
EXPOSE 8000

# Command to start the FastAPI app using Uvicorn
# --host 0.0.0.0 allows access from external machines
# --port 8000 defines the port to listen on
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
