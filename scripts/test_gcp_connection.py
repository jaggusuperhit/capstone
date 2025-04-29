"""
Test script to verify GCP connection and credentials.
"""
import os
import json
from google.cloud import storage

def test_gcp_connection():
    """Test connection to GCP Cloud Storage."""
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

        # List buckets
        buckets = list(storage_client.list_buckets())
        print("✅ Successfully connected to GCP Cloud Storage!")
        print(f"Found {len(buckets)} buckets:")
        for bucket in buckets:
            print(f"  - {bucket.name}")

        # Check if our bucket exists
        bucket_exists = any(bucket.name == bucket_name for bucket in buckets)
        if bucket_exists:
            print(f"✅ Bucket '{bucket_name}' exists!")

            # Let's check if we can access the bucket and list its contents
            try:
                bucket = storage_client.bucket(bucket_name)
                blobs = list(bucket.list_blobs())
                print(f"Found {len(blobs)} files in the bucket:")
                for blob in blobs:
                    print(f"  - {blob.name}")

                # Create a test file if the bucket is empty
                if len(blobs) == 0:
                    print("Bucket is empty. Creating a test file...")
                    test_blob = bucket.blob("test.txt")
                    test_blob.upload_from_string("This is a test file to verify GCP connection.")
                    print("✅ Test file created successfully!")
            except Exception as e:
                print(f"❌ Error accessing bucket contents: {e}")
        else:
            print(f"❌ Bucket '{bucket_name}' does not exist. Please create it in the Google Cloud Console.")

        return True
    except Exception as e:
        print(f"❌ Error connecting to GCP: {e}")
        return False

if __name__ == "__main__":
    print("Testing GCP Connection...")
    test_gcp_connection()
