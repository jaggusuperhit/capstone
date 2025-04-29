# Local GCP Setup Guide

This guide explains how to set up Google Cloud Platform (GCP) credentials for local development.

## Prerequisites

1. A Google Cloud Platform account
2. A GCP project with billing enabled
3. The `gcloud` CLI installed (optional but recommended)

## Step 1: Create a Service Account and Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project or create a new one
3. Navigate to "IAM & Admin" > "Service Accounts"
4. Click "CREATE SERVICE ACCOUNT"
5. Give it a name like "sentiment-analysis-local"
6. Grant the following roles:
   - Storage Admin
   - Storage Object Admin
   - Artifact Registry Admin
7. Click "CREATE KEY" and select JSON format
8. Save the key file to your local machine (e.g., `gcp-key.json`)

## Step 2: Set Up Environment Variables

### Windows (PowerShell)

Run the provided PowerShell script:

```powershell
.\setup_local_gcp.ps1 -CredentialsPath "path\to\your\gcp-key.json"
```

### Linux/Mac (Bash)

Run the provided Bash script:

```bash
chmod +x setup_local_gcp.sh
./setup_local_gcp.sh /path/to/your/gcp-key.json
```

## Step 3: Verify the Setup

After running the setup script, it will:

1. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable
2. Set the `CAPSTONE_TEST` environment variable for MLflow
3. Run the GCP setup script to configure the bucket
4. Check the GCP bucket and upload sample data if needed

You should see output confirming that the setup was successful.

## Step 4: Run the DVC Pipeline

Now you can run the DVC pipeline:

```bash
dvc repro
```

This will execute the entire ML pipeline using the GCP bucket for storage.

## Troubleshooting

### Common Issues

1. **Authentication Error**: Make sure the service account key file is valid and has the necessary permissions.
2. **Bucket Not Found**: Verify that the bucket name in the setup script matches your actual GCP bucket.
3. **Missing Dependencies**: Ensure you have all required Python packages installed:
   ```bash
   pip install google-cloud-storage pandas
   ```

### Checking GCP Connection

You can verify your GCP connection by running:

```bash
python check_gcp_bucket.py
```

This will list the contents of your GCP bucket and confirm that your credentials are working correctly.
