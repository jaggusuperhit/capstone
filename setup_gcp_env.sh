#!/bin/bash
# Bash script to set up GCP environment variables

if [ $# -eq 0 ]; then
    echo "Usage: $0 <path-to-credentials-file>"
    exit 1
fi

CREDENTIALS_PATH=$1

# Validate the credentials file
if [ ! -f "$CREDENTIALS_PATH" ]; then
    echo "Credentials file not found: $CREDENTIALS_PATH"
    exit 1
fi

# Set the environment variable for the current session
export GOOGLE_APPLICATION_CREDENTIALS="$CREDENTIALS_PATH"
echo "Environment variable set: GOOGLE_APPLICATION_CREDENTIALS=$CREDENTIALS_PATH"

# Activate the virtual environment if it exists
VENV_PATH="./capstone/bin/activate"
if [ -f "$VENV_PATH" ]; then
    echo "Activating virtual environment..."
    source "$VENV_PATH"
    echo "Virtual environment activated"
fi

# Run the setup script if it exists
SETUP_SCRIPT="./setup_gcp.py"
if [ -f "$SETUP_SCRIPT" ]; then
    echo "Running GCP setup script..."
    python "$SETUP_SCRIPT" --credentials "$CREDENTIALS_PATH" --bucket-name "sentiment-analysis-data-20250428"
    echo "GCP setup completed"
fi

echo "GCP environment setup completed successfully!"
echo "You can now run your pipeline with: dvc repro"
