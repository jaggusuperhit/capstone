# PowerShell script to create a zonal GKE cluster (uses fewer resources)

# Set variables
$PROJECT_ID = "rag-youtube-457803"
$ZONE = "us-central1-a"  # Specific zone instead of region
$CLUSTER_NAME = "sentiment-analysis-cluster"
$MACHINE_TYPE = "e2-small"
$NUM_NODES = 1

# Check if gcloud is installed
try {
    $gcloudVersion = gcloud --version
    Write-Host "gcloud is installed: $gcloudVersion"
} catch {
    Write-Host "Error: gcloud CLI is not installed or not in PATH. Please install Google Cloud SDK." -ForegroundColor Red
    Write-Host "Visit: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

# Check if user is authenticated with gcloud
$authStatus = gcloud auth list --filter=status:ACTIVE --format="value(account)"
if (-not $authStatus) {
    Write-Host "You are not authenticated with gcloud. Please run 'gcloud auth login' first." -ForegroundColor Yellow
    exit 1
}

# Create the GKE cluster
Write-Host "Creating zonal GKE cluster '$CLUSTER_NAME' in zone '$ZONE'..."
Write-Host "This may take several minutes..."

$clusterCreated = $false

try {
    $result = gcloud container clusters create $CLUSTER_NAME `
        --zone $ZONE `
        --num-nodes $NUM_NODES `
        --machine-type $MACHINE_TYPE `
        --disk-type "pd-standard" `
        --disk-size "100" `
        --project $PROJECT_ID
    
    # Check if the cluster was created successfully
    if ($LASTEXITCODE -eq 0) {
        $clusterCreated = $true
        Write-Host "GKE cluster '$CLUSTER_NAME' created successfully!" -ForegroundColor Green
    } else {
        Write-Host "Error creating GKE cluster. Exit code: $LASTEXITCODE" -ForegroundColor Red
        Write-Host "Output: $result" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "Error creating GKE cluster: $_" -ForegroundColor Red
    exit 1
}

# Only proceed if the cluster was created successfully
if ($clusterCreated) {
    # Get credentials for the cluster
    Write-Host "Getting credentials for the cluster..."
    try {
        gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE --project $PROJECT_ID
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Cluster credentials obtained successfully!" -ForegroundColor Green
            Write-Host "Cluster creation and configuration completed successfully!" -ForegroundColor Green
            
            # Create a modified deploy script for zonal cluster
            Write-Host "Creating a zonal deployment script..."
            $deployScript = Get-Content -Path "scripts/deploy_to_gke.ps1"
            $deployScript = $deployScript -replace 'REGION = "us-central1"', 'ZONE = "us-central1-a"'
            $deployScript = $deployScript -replace 'gcloud container clusters get-credentials \$CLUSTER_NAME --region \$REGION --project \$PROJECT_ID', 'gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE --project $PROJECT_ID'
            Set-Content -Path "scripts/deploy_to_gke_zonal.ps1" -Value $deployScript
            
            Write-Host "Zonal deployment script created. You can now deploy your application using: .\scripts\deploy_to_gke_zonal.ps1" -ForegroundColor Green
        } else {
            Write-Host "Error getting cluster credentials. Exit code: $LASTEXITCODE" -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "Error getting cluster credentials: $_" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Skipping credential retrieval as cluster creation failed." -ForegroundColor Yellow
    exit 1
}
