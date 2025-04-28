import pandas as pd
import logging
from google.cloud import storage
from io import StringIO
import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Now import from src
try:
    from src.logger import logging
except ImportError:
    # If the above import fails, set up basic logging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

class gcp_operations:
    def __init__(self, bucket_name, credentials_path=None):
        """
        Initialize the gcp_operations class with GCP credentials and Cloud Storage bucket details.
        
        Args:
            bucket_name (str): Name of the GCP Cloud Storage bucket
            credentials_path (str, optional): Path to the GCP service account key file.
                If None, will use the GOOGLE_APPLICATION_CREDENTIALS environment variable.
        """
        self.bucket_name = bucket_name
        
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
            
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)
        logging.info(f"Data Ingestion from GCP Cloud Storage bucket '{bucket_name}' initialized")

    def fetch_file_from_gcs(self, file_path):
        """
        Fetches a CSV file from the GCP Cloud Storage bucket and returns it as a Pandas DataFrame.
        
        Args:
            file_path (str): GCS file path (e.g., 'data/data.csv')
            
        Returns:
            pandas.DataFrame: DataFrame containing the CSV data
        """
        try:
            logging.info(f"Fetching file '{file_path}' from GCS bucket '{self.bucket_name}'...")
            blob = self.bucket.blob(file_path)
            content = blob.download_as_text()
            df = pd.read_csv(StringIO(content))
            logging.info(f"Successfully fetched and loaded '{file_path}' from GCS that has {len(df)} records.")
            return df
        except Exception as e:
            logging.exception(f"❌ Failed to fetch '{file_path}' from GCS: {e}")
            return None
    
    def upload_file_to_gcs(self, source_file_path, destination_blob_name):
        """
        Uploads a file to the GCP Cloud Storage bucket.
        
        Args:
            source_file_path (str): Path to the local file to upload
            destination_blob_name (str): Name to give the file in GCS
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logging.info(f"Uploading file '{source_file_path}' to GCS bucket '{self.bucket_name}'...")
            blob = self.bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_path)
            logging.info(f"Successfully uploaded '{source_file_path}' to GCS as '{destination_blob_name}'.")
            return True
        except Exception as e:
            logging.exception(f"❌ Failed to upload '{source_file_path}' to GCS: {e}")
            return False
    
    def upload_dataframe_to_gcs(self, df, destination_blob_name, file_format='csv'):
        """
        Uploads a pandas DataFrame to the GCP Cloud Storage bucket.
        
        Args:
            df (pandas.DataFrame): DataFrame to upload
            destination_blob_name (str): Name to give the file in GCS
            file_format (str): Format to save the DataFrame as ('csv' or 'parquet')
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logging.info(f"Uploading DataFrame to GCS bucket '{self.bucket_name}' as '{destination_blob_name}'...")
            blob = self.bucket.blob(destination_blob_name)
            
            if file_format.lower() == 'csv':
                content = df.to_csv(index=False)
                blob.upload_from_string(content, content_type='text/csv')
            elif file_format.lower() == 'parquet':
                # Create a temporary file
                temp_file = 'temp_dataframe.parquet'
                df.to_parquet(temp_file, index=False)
                
                # Upload the file
                blob.upload_from_filename(temp_file)
                
                # Remove the temporary file
                os.remove(temp_file)
            else:
                raise ValueError(f"Unsupported file format: {file_format}. Use 'csv' or 'parquet'.")
                
            logging.info(f"Successfully uploaded DataFrame with {len(df)} records to GCS as '{destination_blob_name}'.")
            return True
        except Exception as e:
            logging.exception(f"❌ Failed to upload DataFrame to GCS: {e}")
            return False

# Example usage
# if __name__ == "__main__":
#     # Replace these with your actual GCP details
#     BUCKET_NAME = "your-bucket-name"
#     CREDENTIALS_PATH = "path/to/your/service-account-key.json"  # Optional
#     FILE_PATH = "data/data.csv"  # Path inside GCS bucket
#
#     # Initialize with credentials file
#     # gcp = gcp_operations(BUCKET_NAME, CREDENTIALS_PATH)
#     
#     # Or initialize using environment variable (set GOOGLE_APPLICATION_CREDENTIALS)
#     # gcp = gcp_operations(BUCKET_NAME)
#     
#     # Fetch data
#     # df = gcp.fetch_file_from_gcs(FILE_PATH)
#     
#     # if df is not None:
#     #     print(f"Data fetched with {len(df)} records.")
#     #     print(df.head())  # Display first few rows of the fetched DataFrame
