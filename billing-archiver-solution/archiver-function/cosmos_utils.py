import os
import json
from azure.cosmos import CosmosClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env")

# Load required Cosmos DB credentials from .env
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
DATABASE_ID = os.getenv("COSMOS_DB", "BillingDB")
CONTAINER_ID = os.getenv("COSMOS_CONTAINER", "Records")

# Cosmos DB client setup
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
db = client.get_database_client(DATABASE_ID)
container = db.get_container_client(CONTAINER_ID)

def get_old_records(cutoff_date):
    query = "SELECT * FROM c WHERE c.recordDate < @cutoff"
    items = container.query_items(
        query,
        parameters=[{"name": "@cutoff", "value": cutoff_date.isoformat()}],
        enable_cross_partition_query=True
    )
    return list(items)

def delete_record(record_id, partition_key):
    container.delete_item(record_id, partition_key=partition_key)
