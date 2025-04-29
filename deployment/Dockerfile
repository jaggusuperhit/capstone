FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
# Install all requirements except the local package
RUN grep -v "^-e \." requirements.txt > requirements_docker.txt && \
    pip install --no-cache-dir -r requirements_docker.txt

# Copy the rest of the application
COPY . .

# Now install the local package
RUN pip install -e .

# Create directory for GCP credentials
RUN mkdir -p /gcp

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "flask_app/app.py"]
