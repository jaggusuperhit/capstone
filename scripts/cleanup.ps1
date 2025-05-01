# PowerShell script to clean up resources

# Clean up minikube resources
Write-Host "Cleaning up minikube resources..."
kubectl delete -f deployment/kubernetes/deployment.yaml
kubectl delete -f deployment/kubernetes/service-monitor.yaml
kubectl delete namespace monitoring

# Clean up Docker images
Write-Host "Cleaning up Docker images..."
docker system prune -f

Write-Host "Cleanup completed successfully!"
