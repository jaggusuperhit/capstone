# PowerShell script to configure Docker with Google Cloud

# Check if gcloud is installed
if (-not (Get-Command "gcloud" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Google Cloud SDK (gcloud) is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please run the install_gcloud.ps1 script first and restart your terminal." -ForegroundColor Red
    exit 1
}

# Check if docker is installed
if (-not (Get-Command "docker" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Docker is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Docker Desktop from https://www.docker.com/products/docker-desktop/" -ForegroundColor Red
    exit 1
}

# Install the GCP Docker credential helper component
Write-Host "Installing docker-credential-gcloud component..."
gcloud components install docker-credential-helper

# Configure Docker to use gcloud as a credential helper
Write-Host "Configuring Docker to use gcloud as a credential helper..."
gcloud auth configure-docker gcr.io,us-docker.pkg.dev --quiet

# Verify the configuration
Write-Host "Verifying Docker configuration..."
$dockerConfigPath = "$env:USERPROFILE\.docker\config.json"
if (Test-Path $dockerConfigPath) {
    Write-Host "Docker configuration file exists at: $dockerConfigPath" -ForegroundColor Green
    Write-Host "Content of Docker config.json:"
    Get-Content $dockerConfigPath | Out-String | Write-Host
} else {
    Write-Host "Warning: Docker configuration file not found at: $dockerConfigPath" -ForegroundColor Yellow
}

# Check if docker-credential-gcloud is in PATH
$dockerCredentialGcloud = Get-Command "docker-credential-gcloud" -ErrorAction SilentlyContinue
if ($dockerCredentialGcloud) {
    Write-Host "docker-credential-gcloud is installed at: $($dockerCredentialGcloud.Source)" -ForegroundColor Green
} else {
    Write-Host "Warning: docker-credential-gcloud is not found in PATH." -ForegroundColor Yellow
    Write-Host "You may need to add the Google Cloud SDK bin directory to your PATH." -ForegroundColor Yellow
}

Write-Host "`nConfiguration complete!" -ForegroundColor Green
Write-Host "You can now authenticate with Google Container Registry using:" -ForegroundColor Green
Write-Host "  gcloud auth login" -ForegroundColor Cyan
Write-Host "And then push images to GCR using:" -ForegroundColor Green
Write-Host "  docker push gcr.io/[PROJECT-ID]/[IMAGE]:[TAG]" -ForegroundColor Cyan
