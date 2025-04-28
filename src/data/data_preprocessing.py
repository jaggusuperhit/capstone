# data preprocessing

import numpy as np
import pandas as pd
import os
import sys
import re
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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

# Download NLTK resources
nltk.download('wordnet', quiet=True)
nltk.download('stopwords', quiet=True)

def preprocess_text(text):
    """
    Preprocess a single text string.

    Args:
        text (str): The text to preprocess.

    Returns:
        str: The preprocessed text.
    """
    # Initialize lemmatizer and stopwords
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Remove numbers
    text = ''.join([char for char in text if not char.isdigit()])
    # Convert to lowercase
    text = text.lower()
    # Remove punctuations
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    text = text.replace('؛', "")
    text = re.sub(r'\s+', ' ', text).strip()  # Fixed invalid escape sequence
    # Remove stop words
    text = " ".join([word for word in text.split() if word not in stop_words])
    # Lemmatization
    text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])
    return text

def preprocess_data(df):
    """
    Preprocess the data for sentiment analysis.

    Args:
        df (pandas.DataFrame): Input DataFrame with text and sentiment columns

    Returns:
        pandas.DataFrame: Preprocessed DataFrame
    """
    # Make a copy of the DataFrame to avoid modifying the original
    processed_df = df.copy()

    # Convert sentiment labels to binary (1 for positive, 0 for negative)
    if 'sentiment' in processed_df.columns:
        processed_df['sentiment'] = processed_df['sentiment'].replace({'positive': 1, 'negative': 0})

    return processed_df

def preprocess_dataframe(df, col='text'):
    """
    Preprocess a DataFrame by applying text preprocessing to a specific column.

    Args:
        df (pd.DataFrame): The DataFrame to preprocess.
        col (str): The name of the column containing text.

    Returns:
        pd.DataFrame: The preprocessed DataFrame.
    """
    # Make a copy of the DataFrame
    df = df.copy()

    # Apply preprocessing to the specified column
    df[col] = df[col].apply(preprocess_text)

    # Remove small sentences (less than 3 words)
    # df[col] = df[col].apply(lambda x: np.nan if len(str(x).split()) < 3 else x)

    # Drop rows with NaN values
    df = df.dropna(subset=[col])
    logging.info("Data pre-processing completed")
    return df


def main():
    try:
        print("Starting data preprocessing...")

        # Fetch the data from data/raw
        print("Loading data from data/raw...")
        train_data = pd.read_csv('./data/raw/train.csv')
        test_data = pd.read_csv('./data/raw/test.csv')
        logging.info('Data loaded properly')
        print(f"Train data shape: {train_data.shape}, Test data shape: {test_data.shape}")

        # Display sample data
        print("Sample train data before preprocessing:")
        print(train_data.head(2))

        # Transform the data
        print("\nPreprocessing train data...")
        train_processed_data = preprocess_dataframe(train_data, 'review')
        print("\nPreprocessing test data...")
        test_processed_data = preprocess_dataframe(test_data, 'review')

        print("\nSample train data after preprocessing:")
        print(train_processed_data.head(2))

        print(f"\nProcessed train data shape: {train_processed_data.shape}")
        print(f"Processed test data shape: {test_processed_data.shape}")

        # Store the data inside data/interim
        print("\nSaving processed data...")
        data_path = os.path.join("./data", "interim")
        os.makedirs(data_path, exist_ok=True)

        train_processed_data.to_csv(os.path.join(data_path, "train_processed.csv"), index=False)
        test_processed_data.to_csv(os.path.join(data_path, "test_processed.csv"), index=False)

        logging.info('Processed data saved to %s', data_path)
        print(f"Processed data saved to {data_path}")
        print("Data preprocessing completed successfully!")
    except Exception as e:
        logging.error('Failed to complete the data transformation process: %s', e)
        print(f"Error: {e}")

if __name__ == '__main__':
    main()