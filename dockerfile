# Use the official Python image as a base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /src

# Copy .env file to the container
COPY .env /src/.env
 
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application with Uvicorn
CMD ["pyton", "-m", "src.main"]