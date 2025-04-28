# register model

import json
import mlflow
import logging
import os
import sys
import dagshub
import warnings

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Now import from src
try:
    from src.logger import logging
except ImportError:
    # If the above import fails, set up basic logging
    logging.basicConfig(
        level=logging.INFO,
        format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

# Suppress warnings
warnings.simplefilter("ignore", UserWarning)
warnings.filterwarnings("ignore")

# Below code block is for production use
# -------------------------------------------------------------------------------------
# Set up DagsHub credentials for MLflow tracking
# dagshub_token = os.getenv("CAPSTONE_TEST")
# if not dagshub_token:
#     raise EnvironmentError("CAPSTONE_TEST environment variable is not set")

# os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
# os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

# dagshub_url = "https://dagshub.com"
# repo_owner = "jaggusuperhit"
# repo_name = "capstone"

# Set up MLflow tracking URI
# mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')
# -------------------------------------------------------------------------------------


# Below code block is for local use
# -------------------------------------------------------------------------------------
mlflow.set_tracking_uri("https://dagshub.com/jaggusuperhit/capstone.mlflow")
dagshub.init(repo_owner="jaggusuperhit", repo_name="capstone", mlflow=True)
# -------------------------------------------------------------------------------------


def load_model_info(file_path: str) -> dict:
    """Load the model info from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            model_info = json.load(file)
        logging.debug('Model info loaded from %s', file_path)
        return model_info
    except FileNotFoundError:
        logging.error('File not found: %s', file_path)
        raise
    except Exception as e:
        logging.error('Unexpected error occurred while loading the model info: %s', e)
        raise

def register_model(model_name: str, model_info: dict):
    """Register the model to the MLflow Model Registry."""
    try:
        model_uri = f"runs:/{model_info['run_id']}/{model_info['model_path']}"

        # Register the model
        model_version = mlflow.register_model(model_uri, model_name)

        # Transition the model to "Staging" stage
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(
            name=model_name,
            version=model_version.version,
            stage="Staging"
        )

        logging.debug(f'Model {model_name} version {model_version.version} registered and transitioned to Staging.')
    except Exception as e:
        logging.error('Error during model registration: %s', e)
        raise

def main():
    try:
        print("Starting model registration process...")

        # Check if reports directory exists
        if not os.path.exists('reports'):
            print("Error: 'reports' directory does not exist. Please run model_evaluation.py first.")
            return

        # Load model info
        model_info_path = 'reports/experiment_info.json'
        print(f"Loading model info from {model_info_path}...")

        try:
            model_info = load_model_info(model_info_path)
            print(f"Model info loaded: Run ID = {model_info['run_id']}, Model Path = {model_info['model_path']}")
        except FileNotFoundError:
            print(f"Error: Model info file not found at {model_info_path}. Please run model_evaluation.py first.")
            return

        # Register model
        model_name = "my_model"
        print(f"Registering model as '{model_name}'...")

        try:
            register_model(model_name, model_info)
            print(f"Model '{model_name}' registered successfully and transitioned to Staging.")
            print("Model registration process completed successfully!")
        except Exception as e:
            logging.error('Error during model registration: %s', e)
            print(f"Error during model registration: {e}")

    except Exception as e:
        logging.error('Failed to complete the model registration process: %s', e)
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
