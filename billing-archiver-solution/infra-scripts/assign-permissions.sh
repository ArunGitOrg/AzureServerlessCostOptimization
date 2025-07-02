#!/bin/bash

# Load environment variables
set -a
source ../.env
set +a

# Get identity principalId of the Function App
PRINCIPAL_ID=$(az functionapp identity show \
  --name "$FUNCTION_APP" \
  --resource-group "$RESOURCE_GROUP" \
  --query principalId --output tsv)

# Assign Cosmos DB Contributor role
az role assignment create \
  --assignee "$PRINCIPAL_ID" \
  --scope "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.DocumentDB/databaseAccounts/$COSMOS_ACCOUNT" \
  --role "Cosmos DB Account Reader and Data Contributor"

# Assign Blob Storage Contributor role
az role assignment create \
  --assignee "$PRINCIPAL_ID" \
  --scope "/subscriptions/$(az account show --query id -o tsv)/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.Storage/storageAccounts/$STORAGE_ACCOUNT" \
  --role "Storage Blob Data Contributor"
