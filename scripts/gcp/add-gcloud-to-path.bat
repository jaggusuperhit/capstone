@echo off
echo Checking for Google Cloud SDK installation...

set "GCLOUD_PATH=%LOCALAPPDATA%\Google\Cloud SDK\google-cloud-sdk\bin"
if not exist "%GCLOUD_PATH%" (
    set "GCLOUD_PATH=%ProgramFiles(x86)%\Google\Cloud SDK\google-cloud-sdk\bin"
)
if not exist "%GCLOUD_PATH%" (
    set "GCLOUD_PATH=%ProgramFiles%\Google\Cloud SDK\google-cloud-sdk\bin"
)
if not exist "%GCLOUD_PATH%" (
    set "GCLOUD_PATH=%USERPROFILE%\google-cloud-sdk\bin"
)

if not exist "%GCLOUD_PATH%" (
    echo Google Cloud SDK not found in common locations.
    echo Please install Google Cloud SDK first.
    echo Visit: https://cloud.google.com/sdk/docs/install
    exit /b 1
)

echo Found Google Cloud SDK at: %GCLOUD_PATH%
echo Adding to PATH for current session...

set "PATH=%PATH%;%GCLOUD_PATH%"
echo.
echo Google Cloud SDK added to PATH for current session.
echo You can now use 'gcloud' commands in this window.
echo.
echo To add permanently to your PATH, run:
echo   setx PATH "%%PATH%%;%GCLOUD_PATH%"
echo.
echo To verify installation, try:
echo   gcloud --version
