import numpy as np
import pandas as pd
import pickle
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
import logging
import mlflow
import mlflow.sklearn
import dagshub
import os
import sys

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
# Set up MLflow tracking with error handling
try:
    # Check if CAPSTONE_TEST environment variable is set
    dagshub_token = os.getenv("CAPSTONE_TEST")

    if dagshub_token:
        # Set up MLflow tracking with authentication
        os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
        os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

        # Set tracking URI and initialize DagsHub
        mlflow.set_tracking_uri("https://dagshub.com/jaggusuperhit/capstone.mlflow")
        dagshub.init(repo_owner="jaggusuperhit", repo_name="capstone", mlflow=True)
        print("MLflow tracking set up with DagsHub authentication")
    else:
        # Set up local MLflow tracking
        print("CAPSTONE_TEST environment variable not set. Using local MLflow tracking.")
        mlflow_dir = os.path.join(os.getcwd(), "mlruns")
        os.makedirs(mlflow_dir, exist_ok=True)
        mlflow.set_tracking_uri(f"file://{mlflow_dir}")
        print(f"MLflow tracking set to local directory: {mlflow_dir}")
except Exception as e:
    print(f"Warning: Failed to set up MLflow tracking: {e}")
    print("Continuing without MLflow tracking")
    # Set a flag to indicate that MLflow tracking is not available
    os.environ["MLFLOW_TRACKING_DISABLED"] = "true"
# -------------------------------------------------------------------------------------


def load_model(file_path: str):
    """Load the trained model from a file."""
    try:
        with open(file_path, 'rb') as file:
            model = pickle.load(file)
        logging.info('Model loaded from %s', file_path)
        return model
    except FileNotFoundError:
        logging.error('File not found: %s', file_path)
        raise
    except Exception as e:
        logging.error('Unexpected error occurred while loading the model: %s', e)
        raise

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        logging.info('Data loaded from %s', file_path)
        return df
    except pd.errors.ParserError as e:
        logging.error('Failed to parse the CSV file: %s', e)
        raise
    except Exception as e:
        logging.error('Unexpected error occurred while loading the data: %s', e)
        raise

def evaluate_model(clf, X_test: np.ndarray, y_test: np.ndarray) -> dict:
    """Evaluate the model and return the evaluation metrics."""
    try:
        y_pred = clf.predict(X_test)
        y_pred_proba = clf.predict_proba(X_test)[:, 1]

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred_proba)

        metrics_dict = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'auc': auc
        }
        logging.info('Model evaluation metrics calculated')
        return metrics_dict
    except Exception as e:
        logging.error('Error during model evaluation: %s', e)
        raise

def save_metrics(metrics: dict, file_path: str) -> None:
    """Save the evaluation metrics to a JSON file."""
    try:
        with open(file_path, 'w') as file:
            json.dump(metrics, file, indent=4)
        logging.info('Metrics saved to %s', file_path)
    except Exception as e:
        logging.error('Error occurred while saving the metrics: %s', e)
        raise

def save_model_info(run_id: str, model_path: str, file_path: str) -> None:
    """Save the model run ID and path to a JSON file."""
    try:
        model_info = {'run_id': run_id, 'model_path': model_path}
        with open(file_path, 'w') as file:
            json.dump(model_info, file, indent=4)
        logging.debug('Model info saved to %s', file_path)
    except Exception as e:
        logging.error('Error occurred while saving the model info: %s', e)
        raise

def main():
    try:
        print("Starting model evaluation process...")

        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)

        # Load model
        print("Loading model...")
        clf = load_model('./models/model.pkl')

        # Load test data
        print("Loading test data...")
        test_data = load_data('./data/processed/test_bow.csv')

        X_test = test_data.iloc[:, :-1].values
        y_test = test_data.iloc[:, -1].values
        print(f"Test data shape: X_test {X_test.shape}, y_test {y_test.shape}")

        # Evaluate model
        print("\nEvaluating model...")
        metrics = evaluate_model(clf, X_test, y_test)
        print("Model evaluation metrics:")
        for metric_name, metric_value in metrics.items():
            print(f"  {metric_name}: {metric_value:.4f}")

        # Save metrics
        print("\nSaving metrics...")
        save_metrics(metrics, 'reports/metrics.json')

        # Check if MLflow tracking is disabled
        if os.environ.get("MLFLOW_TRACKING_DISABLED") == "true":
            print("MLflow tracking is disabled. Skipping MLflow logging.")

            # Save model info without run ID
            print("Saving model info without MLflow run ID...")
            save_model_info("local", "model", 'reports/experiment_info.json')

            print("Model evaluation process completed successfully!")
            return

        # If MLflow tracking is enabled, proceed with MLflow logging
        try:
            print("Setting up MLflow experiment...")
            mlflow.set_experiment("my-dvc-pipeline")

            with mlflow.start_run() as run:  # Start an MLflow run
                print(f"MLflow run started with run_id: {run.info.run_id}")

                # Log metrics to MLflow
                print("Logging metrics to MLflow...")
                for metric_name, metric_value in metrics.items():
                    mlflow.log_metric(metric_name, metric_value)

                # Log model parameters to MLflow
                print("Logging model parameters to MLflow...")
                if hasattr(clf, 'get_params'):
                    params = clf.get_params()
                    for param_name, param_value in params.items():
                        mlflow.log_param(param_name, param_value)

                # Log model to MLflow
                print("Logging model to MLflow...")
                mlflow.sklearn.log_model(clf, "model")

                # Save model info
                print("Saving model info...")
                save_model_info(run.info.run_id, "model", 'reports/experiment_info.json')

                # Log the metrics file to MLflow
                print("Logging metrics file to MLflow...")
                mlflow.log_artifact('reports/metrics.json')

                print("Model evaluation process completed successfully with MLflow tracking!")
        except Exception as e:
            logging.error('Failed to complete the MLflow logging: %s', e)
            print(f"Error during MLflow run: {e}")
            print("Continuing without MLflow tracking...")

            # Save model info without run ID
            print("Saving model info without MLflow run ID...")
            save_model_info("local", "model", 'reports/experiment_info.json')

            print("Model evaluation process completed successfully without MLflow tracking!")

    except Exception as e:
        logging.error('Failed to complete the model evaluation process: %s', e)
        print(f"Error during model evaluation: {e}")

if __name__ == '__main__':
    main()