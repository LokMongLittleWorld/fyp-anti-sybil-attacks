# Use Python 3.10 image as the base
FROM python:3.10-slim-buster

# Install system dependencies and MySQL client
RUN apt-get update && apt-get install -y \
  default-mysql-client \
  && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Command to keep the container running
CMD ["tail", "-f", "/dev/null"]