import setuptools
import os
import re
import string
import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

import numpy as np
import mlflow
import mlflow.sklearn
import dagshub
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import scipy.sparse

import warnings
warnings.simplefilter("ignore", UserWarning)
warnings.filterwarnings("ignore")
from dotenv import load_dotenv

# ========================== CONFIGURATION ==========================
CONFIG = {
    "data_path": "notebooks/data.csv",
    "test_size": 0.2,
    "mlflow_tracking_uri": "https://dagshub.com/jaggusuperhit/capstone.mlflow",
    "dagshub_repo_owner": "jaggusuperhit",
    "dagshub_repo_name": "capstone",
    "experiment_name": "Bow vs TfIdf"
}

# ========================== SETUP MLflow & DAGSHUB ==========================
mlflow.set_tracking_uri(CONFIG["mlflow_tracking_uri"])
dagshub.init(repo_owner=CONFIG["dagshub_repo_owner"], repo_name=CONFIG["dagshub_repo_name"], mlflow=True)
mlflow.set_experiment(CONFIG["experiment_name"])

# ========================== TEXT PREPROCESSING ==========================
def lemmatization(text):
    lemmatizer = WordNetLemmatizer()
    return " ".join([lemmatizer.lemmatize(word) for word in text.split()])

def remove_stop_words(text):
    stop_words = set(stopwords.words("english"))
    return " ".join([word for word in text.split() if word not in stop_words])

def removing_numbers(text):
    return ''.join([char for char in text if not char.isdigit()])

def lower_case(text):
    return text.lower()

def removing_punctuations(text):
    return re.sub(f"[{re.escape(string.punctuation)}]", ' ', text)

def removing_urls(text):
    return re.sub(r'https?://\S+|www\.\S+', '', text)

def normalize_text(df):
    try:
        df['review'] = df['review'].apply(lower_case)
        df['review'] = df['review'].apply(remove_stop_words)
        df['review'] = df['review'].apply(removing_numbers)
        df['review'] = df['review'].apply(removing_punctuations)
        df['review'] = df['review'].apply(removing_urls)
        df['review'] = df['review'].apply(lemmatization)
        return df
    except Exception as e:
        print(f"Error during text normalization: {e}")
        raise

# ========================== LOAD & PREPROCESS DATA ==========================
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df = normalize_text(df)
        df = df[df['sentiment'].isin(['positive', 'negative'])]
        df['sentiment'] = df['sentiment'].replace({'negative': 0, 'positive': 1}).infer_objects(copy=False)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        raise

# ========================== FEATURE ENGINEERING ==========================
VECTORIZERS = {
    'BoW': CountVectorizer(),
    'TF-IDF': TfidfVectorizer()
}

ALGORITHMS = {
    'LogisticRegression': LogisticRegression(),
    'MultinomialNB': MultinomialNB(),
    'XGBoost': XGBClassifier(),
    'RandomForest': RandomForestClassifier(),
    'GradientBoosting': GradientBoostingClassifier()
}

# ========================== TRAIN & EVALUATE MODELS ==========================
def train_and_evaluate(df):
    # Remove the parent run and use single runs instead
    for algo_name, algorithm in ALGORITHMS.items():
        for vec_name, vectorizer in VECTORIZERS.items():
            print(f"\nStarting: {algo_name} with {vec_name}")
            # Use a single run instead of nested runs
            with mlflow.start_run(run_name=f"{algo_name}_{vec_name}") as run:
                print(f"Run ID: {run.info.run_id}")
                try:
                    # Feature extraction
                    X = vectorizer.fit_transform(df['review'])
                    y = df['sentiment']
                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y, test_size=CONFIG["test_size"], random_state=42
                    )

                    # Explicitly log the metrics
                    mlflow.log_param("vectorizer", vec_name)
                    mlflow.log_param("algorithm", algo_name)
                    mlflow.log_param("test_size", CONFIG["test_size"])

                    # Train model
                    model = algorithm
                    model.fit(X_train, y_train)

                    # Log model parameters
                    log_model_params(algo_name, model)

                    # Evaluate and log metrics immediately after computation
                    y_pred = model.predict(X_test)
                    
                    accuracy = accuracy_score(y_test, y_pred)
                    precision = precision_score(y_test, y_pred)
                    recall = recall_score(y_test, y_pred)
                    f1 = f1_score(y_test, y_pred)
                    
                    print(f"Logging metrics for {algo_name}_{vec_name}...")
                    print(f"Accuracy: {accuracy:.4f}")
                    print(f"Precision: {precision:.4f}")
                    print(f"Recall: {recall:.4f}")
                    print(f"F1 Score: {f1:.4f}")
                    
                    # Log metrics individually
                    mlflow.log_metric("accuracy", accuracy)
                    mlflow.log_metric("precision", precision)
                    mlflow.log_metric("recall", recall)
                    mlflow.log_metric("f1_score", f1)

                    # Log model
                    input_example = X_test[:5].toarray() if scipy.sparse.issparse(X_test) else X_test[:5]
                    mlflow.sklearn.log_model(
                        model, 
                        "model",
                        input_example=input_example,
                        registered_model_name=f"{algo_name}_{vec_name}"
                    )

                except Exception as e:
                    print(f"Error in run {run.info.run_id}: {str(e)}")
                    mlflow.log_param("error", str(e))
                    raise

def log_model_params(algo_name, model):
    """Logs hyperparameters of the trained model to MLflow."""
    params_to_log = {}
    if algo_name == 'LogisticRegression':
        params_to_log["C"] = model.C
    elif algo_name == 'MultinomialNB':
        params_to_log["alpha"] = model.alpha
    elif algo_name == 'XGBoost':
        params_to_log["n_estimators"] = model.n_estimators
        params_to_log["learning_rate"] = model.learning_rate
    elif algo_name == 'RandomForest':
        params_to_log["n_estimators"] = model.n_estimators
        params_to_log["max_depth"] = model.max_depth
    elif algo_name == 'GradientBoosting':
        params_to_log["n_estimators"] = model.n_estimators
        params_to_log["learning_rate"] = model.learning_rate
        params_to_log["max_depth"] = model.max_depth

    mlflow.log_params(params_to_log)

# ========================== EXECUTION ==========================
def validate_config():
    required_env_vars = [
        'MLFLOW_TRACKING_USERNAME',
        'MLFLOW_TRACKING_PASSWORD',
        'DAGSHUB_USER_TOKEN'
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    required_config = [
        "data_path",
        "test_size",
        "mlflow_tracking_uri",
        "dagshub_repo_owner",
        "dagshub_repo_name",
        "experiment_name"
    ]
    
    missing_config = [key for key in required_config if key not in CONFIG]
    if missing_config:
        raise ValueError(f"Missing required configuration keys: {', '.join(missing_config)}")

def verify_mlflow_connection():
    """Verify MLflow connection and configuration"""
    print(f"MLflow Version: {mlflow.__version__}")
    print(f"Tracking URI: {mlflow.get_tracking_uri()}")
    
    try:
        experiment = mlflow.get_experiment_by_name(CONFIG["experiment_name"])
        if experiment is None:
            experiment_id = mlflow.create_experiment(CONFIG["experiment_name"])
            print(f"Created new experiment with ID: {experiment_id}")
        else:
            print(f"Using existing experiment with ID: {experiment.experiment_id}")
            
        # Test logging
        with mlflow.start_run(run_name="connection_test") as run:
            mlflow.log_param("test_param", "test_value")
            mlflow.log_metric("test_metric", 1.0)
            print(f"Successfully logged test metrics to run: {run.info.run_id}")
            
    except Exception as e:
        print(f"MLflow connection test failed: {str(e)}")
        raise

if __name__ == "__main__":
    load_dotenv()
    validate_config()
    verify_mlflow_connection()
    df = load_data(CONFIG["data_path"])
    train_and_evaluate(df)
