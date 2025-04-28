import os
from setuptools import find_packages, setup

# Only set environment variables if not in build environment
if 'PIP_REQ_TRACKER' not in os.environ:
    # Increase timeout to 60 seconds
    os.environ['DAGSHUB_HTTP_TIMEOUT'] = '60'

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='Sentiment Analysis MLOps Pipeline',
    author='jaggusuperhit',
    license='MIT',
    install_requires=[
        'numpy>=1.20.0',
        'pandas>=1.3.0',
        'scikit-learn>=1.0.0',
        'nltk>=3.8.1',
        'google-cloud-storage>=2.0.0',
        'google-auth>=2.0.0',
        'google-api-python-client>=2.0.0',
        'dvc>=2.10.0',
        'mlflow>=2.9.0',
        'dagshub>=0.2.0',
        'xgboost>=2.0.0',
        'matplotlib>=3.4.0',
        'seaborn>=0.11.0',
    ],
)

