# Direct deployment script - no image building, just deployment

# Set variables
$PROJECT_ID = "rag-youtube-457803"
$REPOSITORY = "sentiment-analysis-app"
$IMAGE_NAME = "gcr.io/${PROJECT_ID}/${REPOSITORY}:latest"

Write-Host "Starting direct deployment to Kubernetes..." -ForegroundColor Green

# Update the deployment file with the correct image
Write-Host "Updating deployment file with image: $IMAGE_NAME"
(Get-Content -Path deployment/kubernetes/deployment.yaml) -replace 'IMAGE_TO_REPLACE', $IMAGE_NAME | Set-Content -Path deployment/kubernetes/deployment.yaml

# Create Kubernetes secrets
Write-Host "Creating Kubernetes secrets..."
kubectl create secret generic capstone-secret `
  --from-literal=CAPSTONE_TEST="local-development" `
  --from-literal=GOOGLE_APPLICATION_CREDENTIALS="/app/gcp-key.json" `
  --dry-run=client -o yaml | kubectl apply -f -

# Apply the deployment
Write-Host "Applying Kubernetes manifests..."
kubectl apply -f deployment/kubernetes/deployment.yaml
kubectl apply -f deployment/kubernetes/service-monitor.yaml

# Check deployment status
Write-Host "Checking deployment status..."
kubectl get deployments
kubectl get pods
kubectl get services

Write-Host "Deployment completed!" -ForegroundColor Green
Write-Host "To check the status of your pods, run: kubectl get pods" -ForegroundColor Yellow
Write-Host "To get the service URL, run: kubectl get service sentiment-analysis-service" -ForegroundColor Yellow
