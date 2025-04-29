#!/bin/bash
# Bash script to set up local GCP environment
# Usage: ./setup_local_gcp.sh /path/to/your/gcp-key.json

# Check if credentials path is provided
if [ -z "$1" ]; then
    echo "Error: Credentials path is required"
    echo "Usage: ./setup_local_gcp.sh /path/to/your/gcp-key.json"
    exit 1
fi

CREDENTIALS_PATH=$(realpath "$1")

# Validate the credentials file
if [ ! -f "$CREDENTIALS_PATH" ]; then
    echo "Error: Credentials file not found: $CREDENTIALS_PATH"
    exit 1
fi

# Set the environment variable for the current session
export GOOGLE_APPLICATION_CREDENTIALS="$CREDENTIALS_PATH"
echo "Environment variable set: GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS"

# Set the CAPSTONE_TEST environment variable for MLflow
export CAPSTONE_TEST="local-development"
echo "Environment variable set: CAPSTONE_TEST=$CAPSTONE_TEST"

# Activate the virtual environment if it exists
VENV_PATH="./capstone/bin/activate"
if [ -f "$VENV_PATH" ]; then
    echo "Activating virtual environment..."
    source "$VENV_PATH"
    echo "Virtual environment activated"
fi

# Run the setup script
echo "Running GCP setup script..."
python setup_gcp.py --credentials "$GOOGLE_APPLICATION_CREDENTIALS" --bucket-name "sentiment-analysis-data-20250428"
echo "GCP setup completed"

# Check the GCP bucket
echo "Checking GCP bucket..."
python check_gcp_bucket.py
echo "GCP bucket check completed"

echo "GCP environment setup completed successfully!"
echo "You can now run your pipeline with: dvc repro"
