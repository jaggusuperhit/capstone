# PowerShell script to download Google Cloud SDK installer
$url = "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
$output = "$env:TEMP\GoogleCloudSDKInstaller.exe"

Write-Host "Downloading Google Cloud SDK installer..."
Invoke-WebRequest -Uri $url -OutFile $output

Write-Host "Download complete. Installer saved to: $output"
Write-Host "Please run the installer manually and follow the on-screen instructions."
Write-Host "After installation, open a new PowerShell window and run 'gcloud init' to initialize the SDK."
