# PowerShell script to set up GCP credentials

param(
    [Parameter(Mandatory=$true)]
    [string]$CredentialsPath
)

# Validate the credentials file
if (-not (Test-Path $CredentialsPath)) {
    Write-Error "Credentials file not found: $CredentialsPath"
    exit 1
}

# Get the absolute path
$absolutePath = (Resolve-Path $CredentialsPath).Path

# Set the environment variable for the current session
$env:GOOGLE_APPLICATION_CREDENTIALS = $absolutePath
Write-Host "Environment variable set: GOOGLE_APPLICATION_CREDENTIALS=$env:GOOGLE_APPLICATION_CREDENTIALS" -ForegroundColor Green

# Set the CAPSTONE_TEST environment variable if not already set
if (-not $env:CAPSTONE_TEST) {
    $env:CAPSTONE_TEST = "local-development"
    Write-Host "Environment variable set: CAPSTONE_TEST=$env:CAPSTONE_TEST" -ForegroundColor Green
}

# Verify gcloud auth
Write-Host "Activating service account..."
try {
    gcloud auth activate-service-account --key-file=$env:GOOGLE_APPLICATION_CREDENTIALS
    Write-Host "Service account activated successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error activating service account: $_" -ForegroundColor Red
    Write-Host "Please make sure gcloud CLI is installed and in your PATH." -ForegroundColor Yellow
    exit 1
}

# Configure Docker to use gcloud as a credential helper
Write-Host "Configuring Docker to use gcloud as a credential helper..."
try {
    gcloud auth configure-docker
    Write-Host "Docker configured successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error configuring Docker: $_" -ForegroundColor Red
    exit 1
}

Write-Host "GCP credentials setup completed successfully!" -ForegroundColor Green
Write-Host "You can now create a GKE cluster with: .\scripts\create_gke_cluster.ps1"
