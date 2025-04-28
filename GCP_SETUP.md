# GCP Setup for CI/CD Pipeline

This document explains how to set up the required GitHub secrets for the CI/CD pipeline to work with Google Cloud Platform (GCP).

## Required GitHub Secrets

The following secrets need to be set up in your GitHub repository:

1. `GCP_SA_KEY`: The JSON key file for a GCP service account with the necessary permissions
2. `GCP_PROJECT_ID`: Your GCP project ID
3. `GCP_BUCKET_NAME`: The name of your GCP Cloud Storage bucket
4. `GCR_REPOSITORY`: The name of your Google Container Registry repository
5. `GKE_CLUSTER_NAME`: The name of your Google Kubernetes Engine cluster
6. `GKE_ZONE`: The zone where your GKE cluster is located
7. `CAPSTONE_TEST`: Your DagsHub token for MLflow tracking

## Step-by-Step Setup

### 1. Create a GCP Service Account

1. Go to the Google Cloud Console
2. Navigate to IAM & Admin > Service Accounts
3. Click "CREATE SERVICE ACCOUNT"
4. Give it a name like "github-actions"
5. Grant the following roles:
   - Storage Admin
   - Container Registry Service Agent
   - Kubernetes Engine Admin
   - Artifact Registry Admin
6. Click "CREATE KEY" and select JSON format
7. Save the key file securely

### 2. Set Up GitHub Secrets

1. Go to your GitHub repository
2. Navigate to Settings > Secrets and variables > Actions
3. Click "New repository secret"
4. Add the following secrets:

   - Name: `GCP_SA_KEY`
     Value: *The entire content of the JSON key file*

   - Name: `GCP_PROJECT_ID`
     Value: *Your GCP project ID, e.g., "rag-youtube-457803"*

   - Name: `GCP_BUCKET_NAME`
     Value: *Your GCP bucket name, e.g., "sentiment-analysis-data-20250428"*

   - Name: `GCR_REPOSITORY`
     Value: *Your container repository name, e.g., "sentiment-analysis-app"*

   - Name: `GKE_CLUSTER_NAME`
     Value: *Your GKE cluster name, e.g., "sentiment-analysis-cluster"*

   - Name: `GKE_ZONE`
     Value: *Your GKE cluster zone, e.g., "us-central1-a"*

   - Name: `CAPSTONE_TEST`
     Value: *Your DagsHub token*

### 3. Create GKE Cluster (if not already created)

```bash
gcloud container clusters create sentiment-analysis-cluster \
  --zone us-central1-a \
  --num-nodes 2 \
  --machine-type e2-standard-2
```

### 4. Create Container Registry Repository

```bash
gcloud artifacts repositories create sentiment-analysis-app \
  --repository-format=docker \
  --location=us-central1 \
  --description="Sentiment Analysis App Repository"
```

## Verifying the Setup

After setting up all the secrets, push a change to your repository to trigger the CI/CD pipeline. The pipeline should:

1. Authenticate with GCP
2. Run the DVC pipeline
3. Build and push the Docker image to GCR
4. Deploy the application to GKE

You can monitor the progress in the "Actions" tab of your GitHub repository.
