# PowerShell script to commit and push changes

# Add all changes
git add .

# Commit changes
git commit -m "Fix model_registration.py to handle missing authentication"

# Push changes to the main branch
git push origin main

Write-Host "Changes pushed to the repository. Check the GitHub Actions tab to monitor the CI/CD pipeline."
