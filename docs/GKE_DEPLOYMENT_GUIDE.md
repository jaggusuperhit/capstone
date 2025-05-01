# GKE Deployment Guide

This guide provides step-by-step instructions for deploying the Sentiment Analysis application to Google Kubernetes Engine (GKE).

## Prerequisites

1. Google Cloud SDK (gcloud CLI) installed
2. Docker installed and configured
3. kubectl installed
4. A Google Cloud Platform (GCP) project with billing enabled
5. A GCP service account key file with appropriate permissions

## Step 1: Set Up GCP Credentials

First, set up your GCP credentials by running the provided script:

```powershell
# On Windows PowerShell
.\scripts\setup_gcp_credentials.ps1 -CredentialsPath "path\to\your\credentials.json"
```

```bash
# On Linux/Mac
./scripts/setup_gcp_env.sh /path/to/your/credentials.json
```

This script will:
- Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
- Activate the service account
- Configure Docker to use gcloud as a credential helper

## Step 2: Create a GKE Cluster

Create a GKE cluster using the provided script:

```powershell
# On Windows PowerShell
.\scripts\create_gke_cluster.ps1
```

```bash
# On Linux/Mac
./scripts/create_gke_cluster.sh
```

This script will:
- Create a GKE cluster named "sentiment-analysis-cluster" in the us-central1 region
- Configure kubectl to use the cluster

## Step 3: Deploy the Application

Deploy the application to the GKE cluster:

```powershell
# On Windows PowerShell
.\scripts\deploy_to_gke.ps1
```

```bash
# On Linux/Mac
./scripts/deploy_to_gke.sh
```

This script will:
- Build the Docker image
- Push the image to Google Container Registry (GCR)
- Create Kubernetes secrets
- Apply the deployment and service monitor

## Step 4: Verify the Deployment

Verify that the deployment was successful:

```bash
# Check the deployment status
kubectl get deployments

# Check the pods
kubectl get pods

# Check the service
kubectl get services
```

The service will have an external IP address that you can use to access the application.

## Step 5: Access the Application

Access the application using the external IP address of the service:

```bash
# Get the external IP address
kubectl get service sentiment-analysis-service
```

The application will be available at http://<EXTERNAL-IP>

## Troubleshooting

### Common Issues

1. **GKE Cluster Creation Fails**:
   - Ensure you have sufficient permissions in your GCP project
   - Check that billing is enabled for your GCP project
   - Verify that the Kubernetes Engine API is enabled

2. **Docker Image Push Fails**:
   - Ensure Docker is configured to use gcloud as a credential helper
   - Check that your service account has permissions to push to GCR

3. **Deployment Fails**:
   - Check the pod logs: `kubectl logs <pod-name>`
   - Describe the pod: `kubectl describe pod <pod-name>`

4. **Service Account Key Secret Creation Fails**:
   - Ensure the GOOGLE_APPLICATION_CREDENTIALS environment variable is set correctly
   - Verify that the credentials file exists and is valid

## Cleaning Up

To clean up the resources when you're done:

```powershell
# On Windows PowerShell
.\scripts\cleanup_gke.ps1
```

```bash
# On Linux/Mac
./scripts/cleanup_gke.sh
```

This script will:
- Delete the Kubernetes resources
- Delete the GKE cluster
