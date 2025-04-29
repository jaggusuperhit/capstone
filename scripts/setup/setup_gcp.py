"""
Script to set up GCP for the project.
This script helps with:
1. Setting up the GCP credentials
2. Creating the GCP bucket if it doesn't exist
3. Testing the connection to GCP
"""
import os
import json
import argparse
from google.cloud import storage
from google.oauth2 import service_account

def setup_gcp(credentials_path, project_id=None, bucket_name=None, region=None):
    """Set up GCP for the project."""
    print(f"Setting up GCP with credentials from: {credentials_path}")
    
    # Validate the credentials file
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Credentials file not found: {credentials_path}")
    
    # Load the credentials
    try:
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        if project_id is None:
            with open(credentials_path, 'r') as f:
                creds_json = json.load(f)
                project_id = creds_json.get('project_id')
        
        print(f"Credentials loaded successfully for project: {project_id}")
    except Exception as e:
        raise Exception(f"Failed to load credentials: {e}")
    
    # Set the environment variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    print(f"Environment variable GOOGLE_APPLICATION_CREDENTIALS set to: {credentials_path}")
    
    # Initialize the storage client
    storage_client = storage.Client()
    print("Storage client initialized successfully")
    
    # Check if the bucket exists, create it if it doesn't
    if bucket_name:
        bucket_exists = any(bucket.name == bucket_name for bucket in storage_client.list_buckets())
        
        if bucket_exists:
            print(f"Bucket '{bucket_name}' already exists")
        else:
            print(f"Creating bucket '{bucket_name}' in region '{region or 'us-central1'}'...")
            bucket = storage_client.create_bucket(bucket_name, location=region or "us-central1")
            print(f"Bucket '{bucket_name}' created successfully in {bucket.location}")
        
        # Update the config file
        config = {
            "gcp": {
                "bucket_name": bucket_name,
                "project_id": project_id,
                "region": region or "us-central1"
            }
        }
        
        os.makedirs("src/connections", exist_ok=True)
        with open("src/connections/gcp_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print(f"Config file updated: src/connections/gcp_config.json")
    
    print("GCP setup completed successfully!")
    return True

def main():
    parser = argparse.ArgumentParser(description="Set up GCP for the project")
    parser.add_argument("--credentials", required=True, help="Path to the GCP credentials JSON file")
    parser.add_argument("--project-id", help="GCP project ID (optional, will be read from credentials if not provided)")
    parser.add_argument("--bucket-name", help="GCP bucket name to create or use")
    parser.add_argument("--region", default="us-central1", help="GCP region (default: us-central1)")
    
    args = parser.parse_args()
    
    try:
        setup_gcp(args.credentials, args.project_id, args.bucket_name, args.region)
    except Exception as e:
        print(f"Error setting up GCP: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
