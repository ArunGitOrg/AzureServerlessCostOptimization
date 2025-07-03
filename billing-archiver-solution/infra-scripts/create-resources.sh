#!/bin/bash

# Load environment variables
set -a
source ../.env
set +a

# Create Resource Group
az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

# # Create Cosmos DB Account            # Uncomment lines related to Cosmos DB if does not already exist
# az cosmosdb create \
#   --name "$COSMOS_ACCOUNT" \
#   --resource-group "$RESOURCE_GROUP" \
#   --locations regionName="$LOCATION" \
#   --default-consistency-level Session

# # Create Cosmos DB SQL Database & Container
# az cosmosdb sql database create \
#   --account-name "$COSMOS_ACCOUNT" \
#   --resource-group "$RESOURCE_GROUP" \
#   --name "$COSMOS_DB"

# az cosmosdb sql container create \
#   --account-name "$COSMOS_ACCOUNT" \
#   --resource-group "$RESOURCE_GROUP" \
#   --database-name "$COSMOS_DB" \
#   --name "$COSMOS_CONTAINER" \
#   --partition-key-path "/recordDate"

# Create Storage Account
az storage account create \
  --name "$STORAGE_ACCOUNT" \
  --resource-group "$RESOURCE_GROUP" \
  --location "$LOCATION" \
  --sku Standard_GRS \
  --kind StorageV2 \
  --access-tier Cool

# Create Storage Container
az storage container create \
  --name billing-archive \
  --account-name "$STORAGE_ACCOUNT"

# Create App Service Plan
az functionapp plan create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$PLAN_NAME" \
  --location "$LOCATION" \
  --number-of-workers 1 \
  --sku Y1 \
  --is-linux

# Create Function App
az functionapp create \
  --name "$FUNCTION_APP" \
  --resource-group "$RESOURCE_GROUP" \
  --plan "$PLAN_NAME" \
  --storage-account "$STORAGE_ACCOUNT" \
  --runtime python \
  --runtime-version 3.10 \
  --functions-version 4 \
  --os-type Linux

# Enable system-assigned managed identity
az functionapp identity assign \
  --name "$FUNCTION_APP" \
  --resource-group "$RESOURCE_GROUP"
