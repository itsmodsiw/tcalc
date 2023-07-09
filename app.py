import os
from flask import Flask
from google.cloud import storage

app = Flask(__name__)

# Retrieve the JSON key file path from the environment variable
json_key_path = os.environ.get('JSON_KEY_PATH')

# Authenticate with the service account
storage_client = storage.Client.from_service_account_json(json_key_path)
