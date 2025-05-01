# PowerShell script to deploy the application to Google Kubernetes Engine (GKE)

# Set variables
$PROJECT_ID = "rag-youtube-457803"
$REGION = "us-central1"
$CLUSTER_NAME = "sentiment-analysis-cluster"
$REPOSITORY = "sentiment-analysis-app"
$IMAGE_NAME = "gcr.io/${PROJECT_ID}/${REPOSITORY}:latest"

# Build the Docker image
Write-Host "Building Docker image..."
docker build -t $IMAGE_NAME -f deployment/Dockerfile .

# Push the Docker image to Google Container Registry
Write-Host "Pushing Docker image to GCR..."
docker push $IMAGE_NAME

# Get GKE credentials
Write-Host "Getting GKE credentials..."
gcloud container clusters get-credentials $CLUSTER_NAME --region $REGION --project $PROJECT_ID

# Create Kubernetes secrets
Write-Host "Creating Kubernetes secrets..."
kubectl create secret generic capstone-secret `
  --from-literal=CAPSTONE_TEST=$env:CAPSTONE_TEST `
  --from-literal=GOOGLE_APPLICATION_CREDENTIALS=/app/gcp-key.json `
  --dry-run=client -o yaml | kubectl apply -f -

# Create GCP service account key secret
Write-Host "Creating GCP service account key secret..."
if (-not $env:GOOGLE_APPLICATION_CREDENTIALS -or -not (Test-Path $env:GOOGLE_APPLICATION_CREDENTIALS)) {
    Write-Host "Warning: GOOGLE_APPLICATION_CREDENTIALS is not set or file does not exist." -ForegroundColor Yellow
    Write-Host "Skipping creation of GCP service account key secret." -ForegroundColor Yellow
} else {
    # Copy the credentials file to a temporary location with the name key.json
    $tempKeyPath = [System.IO.Path]::GetTempFileName() -replace ".tmp", ".json"
    Copy-Item -Path $env:GOOGLE_APPLICATION_CREDENTIALS -Destination $tempKeyPath -Force

    # Create the secret
    kubectl create secret generic gcp-sa-key `
      --from-file=key.json=$tempKeyPath `
      --dry-run=client -o yaml | kubectl apply -f -

    # Clean up the temporary file
    Remove-Item -Path $tempKeyPath -Force

    Write-Host "GCP service account key secret created successfully!" -ForegroundColor Green
}

# Update the deployment file with the correct image
Write-Host "Updating deployment file..."
(Get-Content -Path deployment/kubernetes/deployment.yaml) -replace 'IMAGE_TO_REPLACE', $IMAGE_NAME | Set-Content -Path deployment/kubernetes/deployment.yaml

# Apply the deployment
Write-Host "Applying Kubernetes manifests..."
kubectl apply -f deployment/kubernetes/deployment.yaml
kubectl apply -f deployment/kubernetes/service-monitor.yaml

Write-Host "Deployment completed successfully!"
