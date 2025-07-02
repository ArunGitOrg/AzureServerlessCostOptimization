import os
import json
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(dotenv_path="../.env")

# Read environment variables
BLOB_CONN_STRING = os.getenv("BLOB_CONN_STRING")
CONTAINER_NAME = os.getenv("STORAGE_CONTAINER", "billing-archive")

# Initialize blob client
blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONN_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

def upload_record_to_blob(record):
    blob_name = f"{record['id']}.json"
    data = json.dumps(record)
    container_client.upload_blob(blob_name, data, overwrite=True)
