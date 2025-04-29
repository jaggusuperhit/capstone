# PowerShell script to set up GCP environment variables
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
$env:GOOGLE_APPLICATION_CREDENTIALS = $CredentialsPath
Write-Host "Environment variable set: GOOGLE_APPLICATION_CREDENTIALS=$CredentialsPath"

# Activate the virtual environment if it exists
$VenvPath = ".\capstone\Scripts\Activate.ps1"
if (Test-Path $VenvPath) {
    Write-Host "Activating virtual environment..."
    & $VenvPath
    Write-Host "Virtual environment activated"
}

# Run the setup script if it exists
$SetupScript = ".\setup_gcp.py"
if (Test-Path $SetupScript) {
    Write-Host "Running GCP setup script..."
    python $SetupScript --credentials $CredentialsPath --bucket-name "sentiment-analysis-data-20250428"
    Write-Host "GCP setup completed"
}

Write-Host "GCP environment setup completed successfully!"
Write-Host "You can now run your pipeline with: dvc repro"
