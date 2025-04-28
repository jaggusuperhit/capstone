cd d:/ML-Ops/capstone
& d:/ML-Ops/capstone/capstone/Scripts/Activate.ps1
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\Admin\Downloads\rag-youtube-457803-5f107bcfa28f.json"
Write-Host "Environment variable set: $env:GOOGLE_APPLICATION_CREDENTIALS"
python flask_app/app.py
