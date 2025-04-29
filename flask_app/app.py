from flask import Flask, render_template, request
import mlflow
import pickle
import os
import pandas as pd
import numpy as np
from prometheus_client import Counter, Histogram, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
import time
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
import re
import dagshub

import warnings
warnings.simplefilter("ignore", UserWarning)
warnings.filterwarnings("ignore")

def lemmatization(text):
    """Lemmatize the text."""
    lemmatizer = WordNetLemmatizer()
    text = text.split()
    text = [lemmatizer.lemmatize(word) for word in text]
    return " ".join(text)

def remove_stop_words(text):
    """Remove stop words from the text."""
    stop_words = set(stopwords.words("english"))
    text = [word for word in str(text).split() if word not in stop_words]
    return " ".join(text)

def removing_numbers(text):
    """Remove numbers from the text."""
    text = ''.join([char for char in text if not char.isdigit()])
    return text

def lower_case(text):
    """Convert text to lower case."""
    text = text.split()
    text = [word.lower() for word in text]
    return " ".join(text)

def removing_punctuations(text):
    """Remove punctuations from the text."""
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    text = text.replace('؛', "")
    text = re.sub('\s+', ' ', text).strip()
    return text

def removing_urls(text):
    """Remove URLs from the text."""
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

def remove_small_sentences(df):
    """Remove sentences with less than 3 words."""
    for i in range(len(df)):
        if len(df.text.iloc[i].split()) < 3:
            df.text.iloc[i] = np.nan

def normalize_text(text):
    text = lower_case(text)
    text = remove_stop_words(text)
    text = removing_numbers(text)
    text = removing_punctuations(text)
    text = removing_urls(text)
    text = lemmatization(text)

    return text

# MLflow and DagsHub setup
# -------------------------------------------------------------------------------------
try:
    # Convert DAGSHUB_HTTP_TIMEOUT to integer if it exists
    if os.environ.get("DAGSHUB_HTTP_TIMEOUT"):
        try:
            # Remove quotes if present
            timeout_value = os.environ.get("DAGSHUB_HTTP_TIMEOUT").strip('"')
            os.environ["DAGSHUB_HTTP_TIMEOUT"] = str(int(timeout_value))
            print(f"Set DAGSHUB_HTTP_TIMEOUT to {os.environ['DAGSHUB_HTTP_TIMEOUT']}")
        except ValueError:
            print(f"Warning: DAGSHUB_HTTP_TIMEOUT value '{os.environ.get('DAGSHUB_HTTP_TIMEOUT')}' is not a valid integer. Using default.")
            os.environ["DAGSHUB_HTTP_TIMEOUT"] = "30"

    # Set up MLflow tracking URI
    mlflow.set_tracking_uri('https://dagshub.com/jaggusuperhit/capstone.mlflow')
    print("MLflow tracking URI set to: https://dagshub.com/jaggusuperhit/capstone.mlflow")

    # Check for credentials in environment variables
    username = os.environ.get("MLFLOW_TRACKING_USERNAME")
    password = os.environ.get("MLFLOW_TRACKING_PASSWORD")

    if username and password:
        print("Found MLflow tracking credentials in environment variables")

        # Try to initialize DagsHub
        try:
            # Set MLflow tracking username and password
            os.environ["MLFLOW_TRACKING_USERNAME"] = username
            os.environ["MLFLOW_TRACKING_PASSWORD"] = password

            # Initialize DagsHub with explicit parameters
            dagshub.init(
                repo_owner='jaggusuperhit',
                repo_name='capstone',
                mlflow=True
            )
            print("DagsHub initialized successfully")
        except Exception as e:
            print(f"Warning: Failed to initialize DagsHub: {e}")
            print("Continuing without DagsHub integration")
    else:
        # Try to use CAPSTONE_TEST as a fallback
        dagshub_token = os.getenv("CAPSTONE_TEST")
        if dagshub_token:
            os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
            os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token
            print("DagsHub credentials set from CAPSTONE_TEST environment variable")

            try:
                dagshub.init(
                    repo_owner='jaggusuperhit',
                    repo_name='capstone',
                    mlflow=True
                )
                print("DagsHub initialized successfully using CAPSTONE_TEST token")
            except Exception as e:
                print(f"Warning: Failed to initialize DagsHub with CAPSTONE_TEST token: {e}")
                print("Continuing without DagsHub integration")
        else:
            print("No DagsHub credentials found. Continuing without DagsHub integration.")
except Exception as e:
    print(f"Warning: Failed to set up MLflow tracking: {e}")
# -------------------------------------------------------------------------------------


# Initialize Flask app
app = Flask(__name__)

# from prometheus_client import CollectorRegistry

# Create a custom registry
registry = CollectorRegistry()

# Define your custom metrics using this registry
REQUEST_COUNT = Counter(
    "app_request_count", "Total number of requests to the app", ["method", "endpoint"], registry=registry
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "Latency of requests in seconds", ["endpoint"], registry=registry
)
PREDICTION_COUNT = Counter(
    "model_prediction_count", "Count of predictions for each class", ["prediction"], registry=registry
)

# ------------------------------------------------------------------------------------------
# Model and vectorizer setup
model_name = "my_model"
model = None
vectorizer = None

# Define a simple fallback model class that implements the predict method
class FallbackSentimentModel:
    """A simple fallback sentiment model that uses basic keyword matching."""

    def __init__(self):
        self.positive_words = set([
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'terrific', 'outstanding', 'superb', 'nice', 'love', 'happy', 'best',
            'awesome', 'brilliant', 'perfect', 'enjoy', 'pleased', 'delighted'
        ])

        self.negative_words = set([
            'bad', 'terrible', 'awful', 'horrible', 'poor', 'disappointing',
            'worst', 'hate', 'dislike', 'sad', 'angry', 'upset', 'annoying',
            'frustrating', 'mediocre', 'inferior', 'useless', 'waste', 'fail'
        ])
        print("Fallback sentiment model initialized")

    def predict(self, X):
        """Predict sentiment based on keyword matching.
        Returns 1 for positive, 0 for negative, based on which sentiment has more matching words.
        """
        if isinstance(X, pd.DataFrame):
            # If input is a DataFrame, convert to text
            text = ' '.join(' '.join(X.values.flatten().astype(str)))
        else:
            # If input is already text
            text = ' '.join(X) if isinstance(X, list) else str(X)

        # Convert to lowercase for matching
        text = text.lower()

        # Count positive and negative words
        positive_count = sum(1 for word in self.positive_words if word in text.split())
        negative_count = sum(1 for word in self.negative_words if word in text.split())

        # Determine sentiment
        if positive_count > negative_count:
            return [1]  # Positive
        else:
            return [0]  # Negative

def get_latest_model_version(model_name):
    client = mlflow.MlflowClient()
    latest_version = client.get_latest_versions(model_name, stages=["Production"])
    if not latest_version:
        latest_version = client.get_latest_versions(model_name, stages=["None"])
    return latest_version[0].version if latest_version else None

# Try to load model from MLflow
try:
    model_version = get_latest_model_version(model_name)
    if model_version:
        model_uri = f'models:/{model_name}/{model_version}'
        print(f"Fetching model from: {model_uri}")
        model = mlflow.pyfunc.load_model(model_uri)
        print("Model loaded successfully from MLflow")
    else:
        print(f"No versions of model '{model_name}' found in MLflow")
        print("Using fallback sentiment model instead")
        model = FallbackSentimentModel()
except Exception as e:
    print(f"Error loading model from MLflow: {e}")
    print("Using fallback sentiment model instead")
    model = FallbackSentimentModel()

# Try to load vectorizer
try:
    vectorizer_path = 'models/vectorizer.pkl'
    if os.path.exists(vectorizer_path):
        vectorizer = pickle.load(open(vectorizer_path, 'rb'))
        print(f"Vectorizer loaded successfully from {vectorizer_path}")
    else:
        print(f"Vectorizer file not found at {vectorizer_path}")
        # Create a simple fallback vectorizer
        from sklearn.feature_extraction.text import CountVectorizer
        print("Creating a simple fallback vectorizer")
        vectorizer = CountVectorizer(max_features=1000)
        # Fit on some sample text to initialize
        vectorizer.fit(["This is a sample text to initialize the vectorizer"])
except Exception as e:
    print(f"Error loading vectorizer: {e}")
    # Create a simple fallback vectorizer
    from sklearn.feature_extraction.text import CountVectorizer
    print("Creating a simple fallback vectorizer")
    vectorizer = CountVectorizer(max_features=1000)
    # Fit on some sample text to initialize
    vectorizer.fit(["This is a sample text to initialize the vectorizer"])

# Check if model and vectorizer are loaded
if model is None or vectorizer is None:
    print("WARNING: Failed to create even fallback models. Prediction functionality will not work.")

# Routes
@app.route("/")
def home():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    start_time = time.time()

    # Check model status for informational purposes
    if model is None or vectorizer is None:
        model_status = "Not Available"
    elif isinstance(model, FallbackSentimentModel):
        model_status = "Using Fallback Keyword Model (MLflow model not found)"
    else:
        model_status = "Using MLflow Model"

    response = render_template("index.html", result=None, error=None, model_status=model_status)
    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start_time)
    return response

@app.route("/predict", methods=["POST"])
def predict():
    REQUEST_COUNT.labels(method="POST", endpoint="/predict").inc()
    start_time = time.time()

    text = request.form["text"]

    # Check if model and vectorizer are available
    if model is None or vectorizer is None:
        error_message = "Model or vectorizer not loaded. Please check server logs."
        REQUEST_LATENCY.labels(endpoint="/predict").observe(time.time() - start_time)
        return render_template("index.html", result=None, error=error_message)

    try:
        # Clean text
        text = normalize_text(text)

        # Check if we're using the fallback model
        is_fallback = isinstance(model, FallbackSentimentModel)

        if is_fallback:
            # For fallback model, we can pass the text directly
            result = model.predict(text)
            prediction = result[0]
            model_type = "Fallback Keyword Model"
        else:
            # For MLflow model, we need to convert to features
            features = vectorizer.transform([text])
            features_df = pd.DataFrame(features.toarray(), columns=[str(i) for i in range(features.shape[1])])
            result = model.predict(features_df)
            prediction = result[0]
            model_type = "MLflow Model"

        # Increment prediction count metric
        PREDICTION_COUNT.labels(prediction=str(prediction)).inc()

        # Measure latency
        REQUEST_LATENCY.labels(endpoint="/predict").observe(time.time() - start_time)

        return render_template("index.html", result=prediction, error=None, model_status=model_type)

    except Exception as e:
        error_message = f"Error during prediction: {str(e)}"
        print(error_message)
        REQUEST_LATENCY.labels(endpoint="/predict").observe(time.time() - start_time)
        return render_template("index.html", result=None, error=error_message)

@app.route("/metrics", methods=["GET"])
def metrics():
    """Expose only custom Prometheus metrics."""
    return generate_latest(registry), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    # app.run(debug=True) # for local use
    app.run(debug=True, host="0.0.0.0", port=5000)  # Accessible from outside Docker