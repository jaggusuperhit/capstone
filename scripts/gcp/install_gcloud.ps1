# PowerShell script to download and install Google Cloud SDK

# Create a temporary directory
$tempDir = Join-Path $env:TEMP "gcloud-install"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

# Download the Google Cloud SDK installer
$installerUrl = "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
$installerPath = Join-Path $tempDir "GoogleCloudSDKInstaller.exe"

Write-Host "Downloading Google Cloud SDK installer..."
Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath

# Run the installer
Write-Host "Running Google Cloud SDK installer..."
Write-Host "Please follow the installation wizard and select the option to add gcloud to your PATH."
Write-Host "Also, select the option to install the 'docker-credential-gcloud' component."
Start-Process -FilePath $installerPath -Wait

# Clean up
Remove-Item -Path $tempDir -Recurse -Force

Write-Host "Installation complete. Please restart your terminal or PowerShell session."
Write-Host "After restarting, run 'gcloud init' to configure your Google Cloud SDK."
