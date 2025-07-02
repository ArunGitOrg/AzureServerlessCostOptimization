import os
import json
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(dotenv_path="../.env")

# Cosmos DB configuration
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_ID = os.getenv("COSMOS_DB", "BillingDB")
CONTAINER_ID = os.getenv("COSMOS_CONTAINER", "Records")

# Blob Storage configuration
BLOB_CONN_STRING = os.getenv("BLOB_CONN_STRING")
BLOB_CONTAINER = os.getenv("STORAGE_CONTAINER", "billing-archive")

# Initialize Cosmos DB client
cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
cosmos_db = cosmos_client.get_database_client(DATABASE_ID)
cosmos_container = cosmos_db.get_container_client(CONTAINER_ID)

# Initialize Blob Storage client
blob_client = BlobServiceClient.from_connection_string(BLOB_CONN_STRING)
blob_container = blob_client.get_container_client(BLOB_CONTAINER)

def get_billing_record(record_id, partition_key):
    try:
        # Try Cosmos DB first
        return cosmos_container.read_item(item=record_id, partition_key=partition_key)
    except Exception:
        # Fallback to Blob Storage
        try:
            blob = blob_container.get_blob_client(f"{record_id}.json")
            data = blob.download_blob().readall()
            return json.loads(data)
        except Exception as e:
            raise ValueError(f"Record {record_id} not found in Cosmos DB or Blob. Error: {e}")
