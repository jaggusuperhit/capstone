import os
from dagshub.common import config

# Increase timeout to 60 seconds
os.environ['DAGSHUB_HTTP_TIMEOUT'] = '60'

from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='mlops',
    author='jaggusuperhit',
    license='MIT',
)

