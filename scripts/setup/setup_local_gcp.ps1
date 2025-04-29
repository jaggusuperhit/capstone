# PowerShell script to set up local GCP environment
# Usage: .\setup_local_gcp.ps1 -CredentialsPath "path\to\your\gcp-key.json"

param(
    [Parameter(Mandatory=$true)]
    [string]$CredentialsPath
)

# Validate the credentials file
if (-not (Test-Path $CredentialsPath)) {
    Write-Error "Credentials file not found: $CredentialsPath"
    exit 1
}

# Set the environment variable for the current session
$env:GOOGLE_APPLICATION_CREDENTIALS = (Resolve-Path $CredentialsPath).Path
Write-Host "Environment variable set: GOOGLE_APPLICATION_CREDENTIALS=$env:GOOGLE_APPLICATION_CREDENTIALS"

# Set the CAPSTONE_TEST environment variable for MLflow
$env:CAPSTONE_TEST = "local-development"
Write-Host "Environment variable set: CAPSTONE_TEST=$env:CAPSTONE_TEST"

# Activate the virtual environment if it exists
$VenvPath = ".\capstone\Scripts\Activate.ps1"
if (Test-Path $VenvPath) {
    Write-Host "Activating virtual environment..."
    & $VenvPath
    Write-Host "Virtual environment activated"
}

# Run the setup script
Write-Host "Running GCP setup script..."
python setup_gcp.py --credentials $env:GOOGLE_APPLICATION_CREDENTIALS --bucket-name "sentiment-analysis-data-20250428"
Write-Host "GCP setup completed"

# Check the GCP bucket
Write-Host "Checking GCP bucket..."
python check_gcp_bucket.py
Write-Host "GCP bucket check completed"

Write-Host "GCP environment setup completed successfully!"
Write-Host "You can now run your pipeline with: dvc repro"
