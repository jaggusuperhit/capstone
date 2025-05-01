# PowerShell script to clean up GKE resources

# Set variables
$PROJECT_ID = "rag-youtube-457803"
$REGION = "us-central1"
$CLUSTER_NAME = "sentiment-analysis-cluster"

# Check if user wants to proceed
Write-Host "WARNING: This will delete all resources in the GKE cluster '$CLUSTER_NAME'." -ForegroundColor Yellow
Write-Host "This action cannot be undone." -ForegroundColor Yellow
$confirmation = Read-Host "Do you want to proceed? (y/n)"
if ($confirmation -ne 'y') {
    Write-Host "Cleanup cancelled." -ForegroundColor Green
    exit 0
}

# Delete Kubernetes resources
Write-Host "Deleting Kubernetes resources..."
kubectl delete -f deployment/kubernetes/deployment.yaml
kubectl delete -f deployment/kubernetes/service-monitor.yaml
kubectl delete secret capstone-secret
kubectl delete secret gcp-sa-key

# Delete the GKE cluster
Write-Host "Deleting GKE cluster '$CLUSTER_NAME'..."
Write-Host "This may take several minutes..."
gcloud container clusters delete $CLUSTER_NAME --region $REGION --project $PROJECT_ID --quiet

Write-Host "Cleanup completed successfully!" -ForegroundColor Green
