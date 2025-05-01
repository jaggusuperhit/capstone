# Setting Up Docker with Google Cloud Platform

This guide will help you set up Docker to work with Google Container Registry (GCR) for pushing and pulling Docker images.

## Prerequisites

- Docker Desktop installed and running
- A Google Cloud Platform account with a project
- Proper permissions to push/pull images to/from GCR

## Step 1: Install Google Cloud SDK

1. Run the provided PowerShell script to download and install the Google Cloud SDK:

```powershell
.\install_gcloud.ps1
```

2. Follow the installation wizard:
   - Choose the option to add gcloud to your PATH
   - Select the option to install the `docker-credential-gcloud` component
   - Restart your terminal or PowerShell session after installation

3. Initialize gcloud and authenticate:

```powershell
gcloud init
gcloud auth login
```

## Step 2: Configure Docker with GCP

1. Run the provided PowerShell script to configure Docker with GCP:

```powershell
.\configure_docker_gcp.ps1
```

2. This script will:
   - Install the Docker credential helper component
   - Configure Docker to use gcloud as a credential helper
   - Verify the configuration

## Step 3: Test the Configuration

1. Authenticate with GCR:

```powershell
gcloud auth configure-docker
```

2. Try pulling a public image from GCR:

```powershell
docker pull gcr.io/google-samples/hello-app:1.0
```

3. Tag and push an image to your project's GCR:

```powershell
# Tag an existing image
docker tag sentiment-analysis:latest gcr.io/[YOUR-PROJECT-ID]/sentiment-analysis:latest

# Push the image to GCR
docker push gcr.io/[YOUR-PROJECT-ID]/sentiment-analysis:latest
```

## Troubleshooting

### Missing docker-credential-gcloud

If you see an error like "docker-credential-gcloud not found in PATH", make sure:

1. You've installed the Google Cloud SDK with the Docker credential helper component
2. The Google Cloud SDK bin directory is in your PATH
3. You've restarted your terminal after installation

You can manually install the component with:

```powershell
gcloud components install docker-credential-helper
```

### Authentication Issues

If you have authentication issues:

1. Make sure you're logged in:

```powershell
gcloud auth login
```

2. Configure Docker to use gcloud credentials:

```powershell
gcloud auth configure-docker
```

3. Check your Docker configuration file:

```powershell
cat $env:USERPROFILE\.docker\config.json
```

It should contain entries for gcr.io with the gcloud credential helper.

## Additional Resources

- [Google Cloud SDK Documentation](https://cloud.google.com/sdk/docs)
- [Docker Authentication for GCR](https://cloud.google.com/container-registry/docs/advanced-authentication)
- [Google Container Registry Documentation](https://cloud.google.com/container-registry/docs)
