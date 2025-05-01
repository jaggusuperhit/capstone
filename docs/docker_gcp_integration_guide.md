# Docker Integration with Google Cloud Platform

This guide provides detailed instructions for setting up Docker to work with Google Cloud Platform (GCP) for your sentiment analysis project.

## Overview

To push Docker images to Google Container Registry (GCR), you need:

1. Google Cloud SDK (gcloud CLI) installed
2. Docker Desktop installed
3. The Docker credential helper for gcloud
4. Proper authentication configured

## Step 1: Install Google Cloud SDK

### Windows Installation

1. Run the provided PowerShell script to download and install the Google Cloud SDK:

```powershell
.\install_gcloud.ps1
```

2. Follow the installation wizard:
   - Choose the option to add gcloud to your PATH
   - Select the option to install the `docker-credential-gcloud` component
   - Restart your terminal or PowerShell session after installation

3. Alternatively, download the installer directly from [Google Cloud SDK Downloads](https://cloud.google.com/sdk/docs/install)

### Verify Installation

After installation, verify that gcloud is installed correctly:

```powershell
gcloud --version
```

If the command is not found, you can use the provided batch file to add gcloud to your PATH:

```cmd
.\add-gcloud-to-path.bat
```

## Step 2: Install Docker Credential Helper

The Docker credential helper allows Docker to use your GCP credentials when pushing or pulling images from GCR.

1. Run the provided PowerShell script:

```powershell
.\install_docker_credential_helper.ps1
```

2. This script will:
   - Install the Docker credential helper component
   - Add it to your PATH for the current session
   - Configure Docker to use gcloud as a credential helper

3. Alternatively, you can install it manually:

```powershell
gcloud components install docker-credential-helper
gcloud auth configure-docker
```

## Step 3: Authenticate with GCP

1. Initialize gcloud and authenticate:

```powershell
gcloud init
gcloud auth login
```

2. Set your project:

```powershell
gcloud config set project sentiment-analysis-project
```

3. Configure Docker to use gcloud credentials:

```powershell
gcloud auth configure-docker
```

## Step 4: Build and Push Docker Images

### Building Your Docker Image

Build your Docker image using the Dockerfile in the deployment directory:

```powershell
docker build -t sentiment-analysis:latest -f deployment/Dockerfile .
```

### Tagging for GCR

Tag your image for GCR:

```powershell
docker tag sentiment-analysis:latest gcr.io/[YOUR-PROJECT-ID]/sentiment-analysis:latest
```

Replace `[YOUR-PROJECT-ID]` with your actual GCP project ID.

### Pushing to GCR

Push your image to GCR:

```powershell
docker push gcr.io/[YOUR-PROJECT-ID]/sentiment-analysis:latest
```

## Step 5: Verify in GCP Console

1. Open the GCP Console: [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Navigate to Container Registry
3. Verify that your image has been pushed successfully

## Troubleshooting

### Common Issues

#### "docker-credential-gcloud not found in PATH"

This error occurs when Docker can't find the credential helper. To fix:

1. Make sure the Google Cloud SDK bin directory is in your PATH
2. Run the `install_docker_credential_helper.ps1` script
3. Restart your terminal or PowerShell session

#### Authentication Issues

If you have authentication issues:

1. Make sure you're logged in:

```powershell
gcloud auth login
```

2. Check your Docker configuration file:

```powershell
cat $env:USERPROFILE\.docker\config.json
```

It should contain entries for gcr.io with the gcloud credential helper.

#### Permission Issues

If you get permission denied errors when pushing to GCR:

1. Make sure you have the necessary permissions in your GCP project
2. Verify that you're authenticated with the correct account:

```powershell
gcloud auth list
```

## CI/CD Integration

Your GitHub Actions workflow is already configured to use GCP authentication for Docker. The relevant section is:

```yaml
# Configure Docker to use gcloud as a credential helper
- name: Configure Docker for GCP
  if: steps.check-gcp-creds.outputs.gcp_creds_available == 'true'
  run: |
    gcloud auth configure-docker gcr.io,us-docker.pkg.dev --quiet

# Build and push Docker image to Google Container Registry
- name: Build Docker image
  if: steps.check-gcp-creds.outputs.gcp_creds_available == 'true'
  run: |
    docker build -t gcr.io/${{ secrets.GCP_PROJECT_ID }}/${{ secrets.GCR_REPOSITORY }}:latest .

- name: Push Docker image to GCR
  if: steps.check-gcp-creds.outputs.gcp_creds_available == 'true'
  run: |
    docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/${{ secrets.GCR_REPOSITORY }}:latest
```

Make sure you have the following secrets configured in your GitHub repository:
- `GCP_SA_KEY`: Your GCP service account key JSON
- `GCP_PROJECT_ID`: Your GCP project ID
- `GCR_REPOSITORY`: The name of your repository in GCR (e.g., "sentiment-analysis")

## Additional Resources

- [Google Cloud SDK Documentation](https://cloud.google.com/sdk/docs)
- [Docker Authentication for GCR](https://cloud.google.com/container-registry/docs/advanced-authentication)
- [Google Container Registry Documentation](https://cloud.google.com/container-registry/docs)
- [GitHub Actions with GCP](https://github.com/google-github-actions/setup-gcloud)
