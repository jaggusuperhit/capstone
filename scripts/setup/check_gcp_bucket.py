"""
Script to check GCP bucket contents and upload sample data if needed.
"""
import os
import pandas as pd
from google.cloud import storage
import json

def check_gcp_bucket():
    """Check the contents of the GCP bucket and upload sample data if needed."""
    try:
        # Check if credentials are set
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            print("❌ GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
            print("Please set it to the path of your service account key file.")
            return False
        
        print(f"✅ Using credentials from: {credentials_path}")
        
        # Load GCP config
        try:
            with open('src/connections/gcp_config.json', 'r') as f:
                gcp_config = json.load(f)
            bucket_name = gcp_config['gcp']['bucket_name']
            project_id = gcp_config['gcp']['project_id']
            print(f"✅ Loaded GCP config: Project ID = {project_id}, Bucket = {bucket_name}")
        except Exception as e:
            print(f"❌ Failed to load GCP config: {e}")
            return False
        
        # Initialize the client
        print("Connecting to GCP Cloud Storage...")
        storage_client = storage.Client()
        
        # Get the bucket
        bucket = storage_client.bucket(bucket_name)
        
        # List files in the bucket
        blobs = list(bucket.list_blobs())
        print(f"Found {len(blobs)} files in the bucket:")
        for blob in blobs:
            print(f"  - {blob.name}")
        
        # Check if we need to upload sample data
        if not any(blob.name.startswith('data/') for blob in blobs):
            print("No data files found in the 'data/' directory. Uploading sample data...")
            
            # Create a sample sentiment analysis dataset
            print("Creating sample sentiment dataset...")
            data = {
                'text': [
                    "I love this product, it's amazing!",
                    "This is the worst experience ever.",
                    "The service was okay, nothing special.",
                    "Absolutely fantastic customer support!",
                    "Very disappointed with the quality."
                ],
                'sentiment': [1, 0, 1, 1, 0]  # 1 for positive, 0 for negative
            }
            
            df = pd.DataFrame(data)
            print(f"Created sample dataset with {len(df)} records")
            
            # Save to a temporary CSV file
            temp_file = "temp_sample_data.csv"
            df.to_csv(temp_file, index=False)
            print(f"Saved to temporary file: {temp_file}")
            
            # Upload to GCP
            print(f"Uploading to GCP bucket '{bucket_name}'...")
            
            # Upload to data/raw/
            blob = bucket.blob("data/raw/sample_data.csv")
            blob.upload_from_filename(temp_file)
            print(f"✅ Uploaded to data/raw/sample_data.csv")
            
            # Upload to data/processed/
            blob = bucket.blob("data/processed/sample_data.csv")
            blob.upload_from_filename(temp_file)
            print(f"✅ Uploaded to data/processed/sample_data.csv")
            
            # Clean up temporary file
            os.remove(temp_file)
            print(f"Removed temporary file: {temp_file}")
            
            # List files again to confirm upload
            blobs = list(bucket.list_blobs())
            print(f"Now found {len(blobs)} files in the bucket:")
            for blob in blobs:
                print(f"  - {blob.name}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Checking GCP bucket...")
    check_gcp_bucket()
