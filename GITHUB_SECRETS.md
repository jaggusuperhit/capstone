# Setting Up GitHub Secrets for CI/CD

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

### 3. Verify the Secrets

After setting up the secrets, you can verify them by:

1. Going to the "Actions" tab in your GitHub repository
2. Clicking on the "CI Pipeline" workflow
3. Clicking "Run workflow" and selecting the branch you want to run it on
4. Checking the logs to make sure the workflow can access the secrets

## Troubleshooting

If you encounter issues with the GitHub Actions workflow:

1. **Missing Secrets**: Make sure all required secrets are set up in GitHub
2. **Invalid JSON**: Ensure the GCP_SA_KEY contains valid JSON without any extra characters
3. **Permissions**: Make sure the service account has the necessary permissions
4. **Resource Names**: Double-check that all resource names (bucket, cluster, etc.) are correct

## Security Notes

- GitHub secrets are encrypted and only exposed to selected GitHub Actions workflows
- Secrets are not passed to workflows that are triggered by a pull request from a fork
- For security reasons, consider using Workload Identity Federation instead of service account keys for production environments
