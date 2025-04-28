# data ingestion
import numpy as np
import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

import os
import sys
from sklearn.model_selection import train_test_split
import yaml
import logging

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Now import from src
try:
    from src.logger import logging
    from src.connections import gcp_connection
except ImportError:
    # If the above import fails, set up basic logging
    logging.basicConfig(
        level=logging.INFO,
        format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def load_params(params_path: str) -> dict:
    """Load parameters from a YAML file."""
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logging.debug('Parameters retrieved from %s', params_path)
        return params
    except FileNotFoundError:
        logging.error('File not found: %s', params_path)
        raise
    except yaml.YAMLError as e:
        logging.error('YAML error: %s', e)
        raise
    except Exception as e:
        logging.error('Unexpected error: %s', e)
        raise

def load_data(data_url: str) -> pd.DataFrame:
    """Load data from a CSV file or URL."""
    try:
        # Check if the URL is a GitHub URL and convert to raw if needed
        if 'github.com' in data_url and '/blob/' in data_url:
            # Convert GitHub URL to raw content URL
            raw_url = data_url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
            logging.info('Converting GitHub URL to raw URL: %s', raw_url)
            data_url = raw_url

        # Try to load the data with different options to handle potential issues
        try:
            df = pd.read_csv(data_url)
        except pd.errors.ParserError:
            # If standard parsing fails, try with more flexible options
            logging.info('Standard parsing failed, trying with more flexible options')
            # Use on_bad_lines='skip' instead of error_bad_lines=False (deprecated)
            df = pd.read_csv(data_url, on_bad_lines='skip')

        logging.info('Data loaded from %s', data_url)
        return df
    except pd.errors.ParserError as e:
        logging.error('Failed to parse the CSV file: %s', e)
        raise
    except Exception as e:
        logging.error('Unexpected error occurred while loading the data: %s', e)
        raise

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the data."""
    try:
        # df.drop(columns=['tweet_id'], inplace=True)
        logging.info("pre-processing...")
        final_df = df[df['sentiment'].isin(['positive', 'negative'])]
        final_df['sentiment'] = final_df['sentiment'].replace({'positive': 1, 'negative': 0})
        logging.info('Data preprocessing completed')
        return final_df
    except KeyError as e:
        logging.error('Missing column in the dataframe: %s', e)
        raise
    except Exception as e:
        logging.error('Unexpected error during preprocessing: %s', e)
        raise

def save_data(train_data: pd.DataFrame, test_data: pd.DataFrame, data_path: str) -> None:
    """Save the train and test datasets."""
    try:
        raw_data_path = os.path.join(data_path, 'raw')
        os.makedirs(raw_data_path, exist_ok=True)
        train_data.to_csv(os.path.join(raw_data_path, "train.csv"), index=False)
        test_data.to_csv(os.path.join(raw_data_path, "test.csv"), index=False)
        logging.debug('Train and test data saved to %s', raw_data_path)
    except Exception as e:
        logging.error('Unexpected error occurred while saving the data: %s', e)
        raise

def main():
    try:
        print("Starting data ingestion process...")

        # Load parameters
        try:
            params = load_params(params_path='params.yaml')
            test_size = params['data_ingestion']['test_size']
            print(f"Using test_size={test_size} from params.yaml")
        except Exception as e:
            print(f"Failed to load parameters: {e}. Using default test_size=0.2")
            test_size = 0.2

        # Try to load data from GCP if credentials are available
        try:
            # Check if GCP credentials are set
            if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
                print("Loading data from GCP Cloud Storage...")
                # Replace with your actual GCP bucket name
                gcp = gcp_connection.gcp_operations("your-bucket-name")
                df = gcp.fetch_file_from_gcs("data/data.csv")
                if df is not None:
                    print(f"Data loaded successfully from GCP. Shape: {df.shape}")
                else:
                    raise Exception("Failed to load data from GCP")
            else:
                # Fallback to GitHub if GCP credentials are not available
                print("GCP credentials not found. Loading data from GitHub...")
                df = load_data(data_url="https://github.com/jaggusuperhit/capstone/blob/main/notebooks/data.csv")
                print(f"Data loaded successfully from GitHub. Shape: {df.shape}")
        except Exception as e:
            print(f"Error loading data from GCP: {e}. Falling back to GitHub...")
            df = load_data(data_url="https://github.com/jaggusuperhit/capstone/blob/main/notebooks/data.csv")
            print(f"Data loaded successfully from GitHub. Shape: {df.shape}")

        print("Sample data:")
        print(df.head())

        print("Preprocessing data...")
        final_df = preprocess_data(df)
        print(f"Preprocessing complete. Shape: {final_df.shape}")

        print("Splitting data into train and test sets...")
        train_data, test_data = train_test_split(final_df, test_size=test_size, random_state=42)
        print(f"Train data shape: {train_data.shape}, Test data shape: {test_data.shape}")

        print("Saving data...")
        save_data(train_data, test_data, data_path='./data')

        # Upload processed data to GCP if credentials are available
        try:
            if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
                print("Uploading processed data to GCP Cloud Storage...")
                gcp = gcp_connection.gcp_operations("your-bucket-name")

                # Create temporary CSV files
                train_temp_path = "train_temp.csv"
                test_temp_path = "test_temp.csv"
                train_data.to_csv(train_temp_path, index=False)
                test_data.to_csv(test_temp_path, index=False)

                # Upload to GCP
                gcp.upload_file_to_gcs(train_temp_path, "processed/train.csv")
                gcp.upload_file_to_gcs(test_temp_path, "processed/test.csv")

                # Clean up temporary files
                os.remove(train_temp_path)
                os.remove(test_temp_path)

                print("Data successfully uploaded to GCP Cloud Storage")
        except Exception as e:
            print(f"Warning: Could not upload data to GCP: {e}")

        print("Data ingestion process completed successfully!")
    except Exception as e:
        logging.error('Failed to complete the data ingestion process: %s', e)
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
