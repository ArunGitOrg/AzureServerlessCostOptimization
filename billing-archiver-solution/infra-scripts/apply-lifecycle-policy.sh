#!/bin/bash

# Load environment variables from .env file
set -a
source ../.env
set +a

# Apply lifecycle policy to the storage account
az storage account management-policy create \
  --account-name "$STORAGE_ACCOUNT" \
  --resource-group "$RESOURCE_GROUP" \
  --policy @lifecycle-policy.json

echo "✅ Lifecycle policy applied successfully."
