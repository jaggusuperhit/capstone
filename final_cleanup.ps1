# PowerShell script for final cleanup of the project

Write-Host "=== Final Project Cleanup Script ==="
Write-Host "This script will remove all unnecessary files and optimize the project for production."

# 1. Remove cleanup scripts
$cleanupScripts = @(
    "cleanup_project.ps1",
    "cleanup_bat_files.ps1",
    "remove_k8s_images.ps1",
    "clean_docker_all.ps1",
    "clean_docker_images.ps1",
    "force_clean_docker_images.ps1"
)

Write-Host "`n=== Removing Cleanup Scripts ==="
foreach ($script in $cleanupScripts) {
    if (Test-Path $script) {
        Write-Host "Removing: $script"
        Remove-Item -Path $script -Force
    }
}

# 2. Remove test and temporary files
Write-Host "`n=== Removing Test and Temporary Files ==="
$testFiles = @(
    "test_gcp_connection.py",
    "test_environment.py",
    "tox.ini",
    "app.py",  # Root app.py (duplicate of flask_app/app.py)
    "token.txt",
    "gke-gcr-puller-key.json",
    "key.json"
)

foreach ($file in $testFiles) {
    if (Test-Path $file) {
        Write-Host "Removing: $file"
        Remove-Item -Path $file -Force
    }
}

# 3. Remove any .env files with credentials (but keep .env.template)
Write-Host "`n=== Removing Environment Files with Credentials ==="
if (Test-Path ".env") {
    Write-Host "Removing: .env (credentials file)"
    Remove-Item -Path ".env" -Force
}

# 4. Remove duplicate script files (keep PowerShell versions for Windows)
Write-Host "`n=== Removing Duplicate Script Files ==="
$duplicateScripts = @(
    "scripts/cleanup.sh",
    "scripts/cleanup_gke.sh",
    "scripts/create_gke_cluster.sh",
    "scripts/deploy_to_gke.sh"
)

foreach ($script in $duplicateScripts) {
    if (Test-Path $script) {
        Write-Host "Removing: $script"
        Remove-Item -Path $script -Force
    }
}

# 5. Remove experimental notebooks
Write-Host "`n=== Removing Experimental Notebooks ==="
$notebooks = @(
    "notebooks/exp-1.ipynb",
    "notebooks/exp-2-bow_vs_tfidf.py",
    "notebooks/exp-3-log_reg-tfidf-hp.py",
    "notebooks/data.csv",
    "notebooks/IMDB.csv"
)

foreach ($notebook in $notebooks) {
    if (Test-Path $notebook) {
        Write-Host "Removing: $notebook"
        Remove-Item -Path $notebook -Force
    }
}

# 6. Clean up Prometheus-Grafana-minikube directory
Write-Host "`n=== Cleaning up Prometheus-Grafana-minikube Directory ==="
if (Test-Path "Prometheus-Grafana-minikube") {
    # Check if it's a git repository
    if (Test-Path "Prometheus-Grafana-minikube/.git") {
        # It's a git repository, properly set it up as a submodule
        Write-Host "Setting up Prometheus-Grafana-minikube as a proper Git submodule..."
        git submodule deinit -f Prometheus-Grafana-minikube
        git rm -f Prometheus-Grafana-minikube
        git submodule add https://github.com/jaggusuperhit/Prometheus-Grafana-minikube.git
    } else {
        # Remove the directory as it's not properly set up
        Remove-Item -Recurse -Force Prometheus-Grafana-minikube
        Write-Host "Removed Prometheus-Grafana-minikube directory"
    }
}

# 7. Remove any temporary files
Write-Host "`n=== Removing Temporary Files ==="
$tempPatterns = @(
    "*.tmp",
    "*.bak",
    "*.swp",
    ".DS_Store",
    "Thumbs.db"
)

foreach ($pattern in $tempPatterns) {
    $tempFiles = Get-ChildItem -Path . -Include $pattern -Recurse -File -ErrorAction SilentlyContinue
    foreach ($file in $tempFiles) {
        Write-Host "Removing temporary file: $($file.FullName)"
        Remove-Item -Path $file.FullName -Force
    }
}

# 8. Clean up __pycache__ directories
Write-Host "`n=== Cleaning up __pycache__ Directories ==="
Get-ChildItem -Path . -Filter "__pycache__" -Recurse -Directory | ForEach-Object {
    Write-Host "Removing: $($_.FullName)"
    Remove-Item -Recurse -Force $_.FullName
}

# 9. Clean up .pyc files
Write-Host "`n=== Cleaning up .pyc Files ==="
Get-ChildItem -Path . -Filter "*.pyc" -Recurse -File | ForEach-Object {
    Write-Host "Removing: $($_.FullName)"
    Remove-Item -Force $_.FullName
}

# 10. Clean up virtual environment if it exists
if (Test-Path "capstone") {
    Write-Host "`n=== Cleaning up Virtual Environment ==="
    Write-Host "Removing virtual environment directory"
    Remove-Item -Recurse -Force "capstone"
}

# 11. Final message
Write-Host "`n=== Final Cleanup Complete ==="
Write-Host "The project has been fully optimized for production."
Write-Host "To remove this final cleanup script, run: Remove-Item -Path final_cleanup.ps1 -Force"
