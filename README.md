# Sentiment Analysis MLOps Pipeline

This project implements a complete MLOps pipeline for sentiment analysis using DVC, MLflow, and Google Cloud Platform.

## Project Overview

The pipeline consists of the following stages:

1. Data Ingestion: Load data from GCP Cloud Storage or GitHub
2. Data Preprocessing: Clean and preprocess text data
3. Feature Engineering: Apply Bag of Words transformation
4. Model Building: Train a Logistic Regression model
5. Model Evaluation: Evaluate model performance
6. Model Registration: Register the model in MLflow

## Setup Instructions

### Prerequisites

- Python 3.8+
- DVC
- MLflow
- Google Cloud SDK

### Installation

1. Clone the repository:

```bash
git clone https://github.com/jaggusuperhit/capstone.git
cd capstone
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Google Cloud Platform Setup

1. Create a GCP project and enable the required APIs:

   - Cloud Storage API
   - Container Registry API
   - Kubernetes Engine API

2. Create a service account with the following permissions:

   - Storage Admin
   - Container Registry Service Agent
   - Kubernetes Engine Admin
   - Artifact Registry Admin

3. Create a key for the service account and download it as JSON:

   - Go to the GCP Console > IAM & Admin > Service Accounts
   - Find your service account and click on it
   - Go to the "Keys" tab and click "Add Key" > "Create new key"
   - Select JSON format and click "Create"
   - Save the key file securely

4. Use the provided setup script to configure your environment:

```bash
# On Windows PowerShell
.\setup_gcp_env.ps1 -CredentialsPath "C:\path\to\your-service-account-key.json"

# On Linux/Mac
chmod +x setup_gcp_env.sh
./setup_gcp_env.sh /path/to/your-service-account-key.json
```

This script will:

- Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
- Create the GCP bucket if it doesn't exist
- Update the GCP configuration in `src/connections/gcp_config.json`

5. Alternatively, you can set up manually:

```bash
# Set environment variable
# On Linux/Mac
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json"

# On Windows PowerShell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your-service-account-key.json"

# Create bucket (if it doesn't exist)
gcloud storage buckets create gs://sentiment-analysis-data-20250428 --location=us-central1

# Update config file
# Edit src/connections/gcp_config.json with your project details
```

The GCP configuration in `src/connections/gcp_config.json` should look like:

```json
{
  "gcp": {
    "bucket_name": "sentiment-analysis-data-20250428",
    "project_id": "your-project-id",
    "region": "us-central1"
  }
}
```

## Running the Pipeline

Run the entire pipeline using DVC:

```bash
dvc repro
```

Or run individual stages:

```bash
dvc repro data_ingestion
dvc repro data_preprocessing
dvc repro feature_engineering
dvc repro model_building
dvc repro model_evaluation
dvc repro model_registration
```

## Project Structure

```
├── data/                       # Data directory
│   ├── raw/                    # Raw data
│   ├── interim/                # Preprocessed data
│   └── processed/              # Feature-engineered data
├── models/                     # Trained models
├── reports/                    # Model evaluation reports
├── src/                        # Source code
│   ├── connections/            # Cloud connections
│   │   ├── gcp_config.json     # GCP configuration
│   │   └── gcp_connection.py   # GCP connection utilities
│   ├── data/                   # Data processing scripts
│   ├── features/               # Feature engineering scripts
│   ├── logger/                 # Logging configuration
│   ├── model/                  # Model training and evaluation scripts
│   └── visualization/          # Visualization utilities
├── flask_app/                  # Flask web application
│   ├── app.py                  # Main Flask application
│   └── templates/              # HTML templates
├── .github/workflows/          # GitHub Actions workflows
│   └── ci.yaml                 # CI/CD pipeline configuration
├── dvc.yaml                    # DVC pipeline configuration
├── params.yaml                 # Pipeline parameters
├── Dockerfile                  # Docker configuration
├── deployment.yaml             # Kubernetes deployment configuration
├── setup_gcp.py                # GCP setup script
├── setup_gcp_env.ps1           # PowerShell setup script
├── setup_gcp_env.sh            # Bash setup script
└── README.md                   # Project documentation
```

## MLflow Tracking

The project uses MLflow for experiment tracking. You can view the experiments at:
https://dagshub.com/jaggusuperhit/capstone.mlflow/
