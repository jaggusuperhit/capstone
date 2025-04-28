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

1. Create a GCP project and enable the Cloud Storage API.

2. Create a Cloud Storage bucket:

```bash
gsutil mb -l us-central1 gs://your-bucket-name
```

3. Create a service account and download the key file:

   - Go to the GCP Console > IAM & Admin > Service Accounts
   - Create a new service account with Storage Admin permissions
   - Create a key for the service account and download it as JSON

4. Set the environment variable for authentication:

```bash
# On Linux/Mac
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json"

# On Windows PowerShell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your-service-account-key.json"
```

5. Update the GCP configuration in `src/connections/gcp_config.json`:

```json
{
  "gcp": {
    "bucket_name": "your-bucket-name",
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
├── data/               # Data directory
│   ├── raw/            # Raw data
│   ├── interim/        # Preprocessed data
│   └── processed/      # Feature-engineered data
├── models/             # Trained models
├── reports/            # Model evaluation reports
├── src/                # Source code
│   ├── connections/    # Cloud connections
│   ├── data/           # Data processing scripts
│   ├── features/       # Feature engineering scripts
│   ├── logger/         # Logging configuration
│   ├── model/          # Model training and evaluation scripts
│   └── visualization/  # Visualization utilities
├── dvc.yaml            # DVC pipeline configuration
├── params.yaml         # Pipeline parameters
└── README.md           # Project documentation
```

## MLflow Tracking

The project uses MLflow for experiment tracking. You can view the experiments at:
https://dagshub.com/jaggusuperhit/capstone.mlflow/
