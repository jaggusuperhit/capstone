# PowerShell script to install the Docker credential helper for gcloud

# Check if gcloud is installed
if (-not (Get-Command "gcloud" -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Google Cloud SDK (gcloud) is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please run the install_gcloud.ps1 script first and restart your terminal." -ForegroundColor Red
    exit 1
}

# Install the Docker credential helper component
Write-Host "Installing docker-credential-gcloud component..."
gcloud components install docker-credential-helper

# Check if the component was installed successfully
$gcloudRoot = (gcloud info --format="value(installation.sdk_root)")
$credentialHelperPath = Join-Path $gcloudRoot "bin\docker-credential-gcloud.exe"

if (Test-Path $credentialHelperPath) {
    Write-Host "docker-credential-gcloud was installed successfully at: $credentialHelperPath" -ForegroundColor Green
    
    # Add the directory to PATH for the current session
    $env:PATH = "$env:PATH;$(Join-Path $gcloudRoot 'bin')"
    Write-Host "Added $(Join-Path $gcloudRoot 'bin') to PATH for current session" -ForegroundColor Green
    
    # Configure Docker to use gcloud as a credential helper
    Write-Host "Configuring Docker to use gcloud as a credential helper..."
    gcloud auth configure-docker gcr.io,us-docker.pkg.dev --quiet
    
    Write-Host "`nTo add the directory permanently to your PATH, run:" -ForegroundColor Yellow
    Write-Host "setx PATH `"%PATH%;$(Join-Path $gcloudRoot 'bin' -replace '\\', '\\')`"" -ForegroundColor Cyan
} else {
    Write-Host "Error: docker-credential-gcloud was not installed correctly." -ForegroundColor Red
    Write-Host "Please try installing it manually with: gcloud components install docker-credential-helper" -ForegroundColor Red
}

# Verify Docker configuration
$dockerConfigPath = "$env:USERPROFILE\.docker\config.json"
if (Test-Path $dockerConfigPath) {
    Write-Host "`nDocker configuration file exists at: $dockerConfigPath" -ForegroundColor Green
    Write-Host "Content of Docker config.json:"
    Get-Content $dockerConfigPath | Out-String | Write-Host
} else {
    Write-Host "`nWarning: Docker configuration file not found at: $dockerConfigPath" -ForegroundColor Yellow
    Write-Host "You may need to run: gcloud auth configure-docker" -ForegroundColor Yellow
}

Write-Host "`nTo test the configuration, try:" -ForegroundColor Green
Write-Host "docker pull gcr.io/google-samples/hello-app:1.0" -ForegroundColor Cyan
