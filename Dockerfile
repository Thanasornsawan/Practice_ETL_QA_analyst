# Dockerfile

# Use a base Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . .

# Set environment variables (if necessary)
ENV DB_PATH="/opt/airflow/sqlite_db/etl.db"

# Command to run when the container starts
CMD ["pytest", "tests/test_etl.py"]
