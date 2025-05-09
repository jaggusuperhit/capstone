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

## Running the Flask Application

You can run the Flask application locally:

```bash
python flask_app/app.py
```

Or using Docker:

```bash
# Build the Docker image
docker build -t sentiment-analysis:latest -f deployment/Dockerfile .

# Run the Docker container
docker run -d -p 5000:5000 --name sentiment-analysis-app sentiment-analysis:latest
```

The application will be available at http://localhost:5000

## Local Testing with Minikube

### Setting up Minikube

1. Start Minikube:

```bash
minikube start
```

2. Deploy the application to Minikube:

```bash
kubectl apply -f deployment/kubernetes/deployment.yaml
```

3. Set up Prometheus and Grafana for monitoring:

```bash
# Create monitoring namespace
kubectl create namespace monitoring

# Add Prometheus Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install Prometheus and Grafana
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring

# Expose Grafana as NodePort
kubectl patch svc prometheus-grafana -n monitoring -p '{"spec": {"type": "NodePort"}}'

# Expose Prometheus as NodePort
kubectl patch svc prometheus-kube-prometheus-prometheus -n monitoring -p '{"spec": {"type": "NodePort"}}'

# Apply ServiceMonitor for the application
kubectl apply -f deployment/kubernetes/service-monitor.yaml
```

4. Access Grafana:

```bash
# Get Grafana admin password
kubectl get secret prometheus-grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 -d

# Port forward Grafana
kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring
```

Grafana will be accessible at http://localhost:3000 with username `admin` and the password retrieved above.

5. Access Prometheus:

```bash
kubectl port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090 -n monitoring
```

Prometheus will be accessible at http://localhost:9090.

6. Clean up local resources:

```bash
# On Windows PowerShell
.\scripts\cleanup.ps1

# On Linux/Mac
./scripts/cleanup.sh
```

## Deploying to Google Kubernetes Engine (GKE)

1. Create a GKE cluster:

```bash
gcloud container clusters create sentiment-analysis-cluster \
  --region us-central1 \
  --num-nodes 2 \
  --machine-type e2-standard-2
```

2. Deploy the application to GKE:

```bash
# On Windows PowerShell
.\scripts\deploy_to_gke.ps1

# On Linux/Mac
./scripts/deploy_to_gke.sh
```

This script will:

- Build and push the Docker image to Google Container Registry
- Get GKE cluster credentials
- Create Kubernetes secrets
- Apply the deployment and service monitor

## Project Structure

```
├── data/                       # Data directory
│   ├── raw/                    # Raw data
│   ├── interim/                # Preprocessed data
│   └── processed/              # Feature-engineered data
├── deployment/                 # Deployment configurations
│   ├── Dockerfile              # Docker configuration
│   └── kubernetes/             # Kubernetes configurations
│       └── deployment.yaml     # Kubernetes deployment configuration
├── flask_app/                  # Flask web application
│   ├── app.py                  # Main Flask application
│   ├── preprocessing_utility.py # Preprocessing utilities for the app
│   └── templates/              # HTML templates
├── models/                     # Trained models
├── reports/                    # Model evaluation reports
├── scripts/                    # Utility scripts
│   ├── docker/                 # Docker utility scripts
│   ├── setup/                  # Setup scripts for GCP and other environments
│   └── promote_model.py        # Model promotion script
├── src/                        # Source code
│   ├── connections/            # Cloud connections
│   │   ├── gcp_config.json     # GCP configuration
│   │   └── gcp_connection.py   # GCP connection utilities
│   ├── data/                   # Data processing scripts
│   ├── features/               # Feature engineering scripts
│   ├── logger/                 # Logging configuration
│   ├── model/                  # Model training and evaluation scripts
│   └── visualization/          # Visualization utilities
├── tests/                      # Test files
│   ├── test_flask_app.py       # Tests for Flask application
│   └── test_model.py           # Tests for ML model
├── .github/workflows/          # GitHub Actions workflows
│   └── ci.yaml                 # CI/CD pipeline configuration
├── dvc.yaml                    # DVC pipeline configuration
├── params.yaml                 # Pipeline parameters
└── README.md                   # Project documentation
```

## MLflow Tracking

The project uses MLflow for experiment tracking. You can view the experiments at:
https://dagshub.com/jaggusuperhit/capstone.mlflow/
