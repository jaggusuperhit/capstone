# PowerShell script to deploy the application to Minikube

# Set variables
$IMAGE_NAME = "sentiment-analysis:latest"

# Check if minikube is running
try {
    $minikubeStatus = minikube status
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Starting Minikube..."
        minikube start
    } else {
        Write-Host "Minikube is already running."
    }
} catch {
    Write-Host "Error checking Minikube status: $_" -ForegroundColor Red
    Write-Host "Starting Minikube..."
    minikube start
}

# Set environment variables for local development
$env:CAPSTONE_TEST = "local-development"
Write-Host "Environment variable set: CAPSTONE_TEST=$env:CAPSTONE_TEST" -ForegroundColor Green

# Build the Docker image
Write-Host "Building Docker image..."
docker build -t $IMAGE_NAME -f deployment/Dockerfile .

# Load the image into Minikube
Write-Host "Loading image into Minikube..."
minikube image load $IMAGE_NAME

# Update the deployment file with the correct image
Write-Host "Updating deployment file..."
(Get-Content -Path deployment/kubernetes/deployment.yaml) -replace 'IMAGE_TO_REPLACE', $IMAGE_NAME | Set-Content -Path deployment/kubernetes/deployment.yaml

# Apply the deployment
Write-Host "Applying Kubernetes manifests..."
kubectl apply -f deployment/kubernetes/deployment.yaml

# Wait for the deployment to be ready
Write-Host "Waiting for deployment to be ready..."
kubectl rollout status deployment/sentiment-analysis-app

# Create a service to expose the application
Write-Host "Creating service..."
kubectl apply -f deployment/kubernetes/service-monitor.yaml

# Get the URL to access the application
Write-Host "Getting URL to access the application..."
minikube service sentiment-analysis-service --url

Write-Host "Deployment completed successfully!" -ForegroundColor Green
Write-Host "You can access the application at the URL above." -ForegroundColor Green
