# Azure Billing Record Archiving Solution

## 📝 Directory Structure
billing-archiver-solution/
├── docs/
│   ├── architecture-diagram.png         
│   └── README.md                        
│   └── Assumptions_Exclusions.txt
│   └── README.md    
│
├── infra-scripts/
│   ├── create-resources.sh              
│   ├── assign-permissions.sh            
│   ├── lifecycle-policy.json            
│   └── apply-lifecycle-policy.sh        
│
├── archiver-function/                   
│   ├── __init__.py                      
│   ├── cosmos_utils.py                  
│   ├── blob_utils.py                    
│   ├── function.json                    
│   ├── requirements.txt                 
│   └── local.settings.json              
│
└── dal/                                 
    └── billing_service.py

---

## 📌 Overview
This solution addresses the growing storage costs associated with billing records stored in Azure Cosmos DB. It introduces a simple, automated archiving mechanism using Azure Blob Storage to retain historical records cost-effectively while ensuring all records remain available on demand.

## ✅ Business Objectives Achieved
| Objective                                | Status | Details |
|------------------------------------------|--------|---------|
| Simplicity & Ease of Implementation     | ✅     | Fully script-driven deployment. No DevOps pipelines or third-party tools needed. |
| No Data Loss & No Downtime              | ✅     | Old records are copied to Blob Storage before removal from Cosmos DB. Function runs asynchronously. |
| No Changes to API Contracts             | ✅     | Existing API read/write interfaces remain unchanged. Optional fallback logic added to read from Blob if not found in Cosmos. |

---

## 💡 Problem Statement

- Cosmos DB is optimized for fast, real-time access — but comes at a cost.
- The current database holds over **2 million records**, many older than **90 days**.
- These older records are **rarely accessed**, yet occupy expensive storage and drive up RU consumption.

---

## 🔧 Solution Summary

- **Hot Data (< 90 days)** → Stored in **Azure Cosmos DB**
- **Cold Data (>= 90 days)** → Archived to **Azure Blob Storage**
- **Timer-triggered Azure Function** runs daily, migrating old records.
- Archived data is stored as JSON files and remains queryable.

---

## 🛠️ Key Components

| Component             | Description |
|----------------------|-------------|
| Azure Cosmos DB      | Primary store for active billing records. |
| Azure Blob Storage   | Cost-effective archive for cold billing data. |
| Azure Function       | Daily timer-triggered archiver written in Python. |
| RBAC                 | Uses system-assigned managed identity for secure, scoped access. |
| Lifecycle Policy     | Automatically moves blobs to Archive Tier after 180 days. |

---

## 🚀 Deployment Guide (Manual)

1. **Login to Azure CLI:**
   ```bash
   az login
   ```

2. **Provision resources:**
   ```bash
   bash infra-scripts/create-resources.sh
   ```

3. **Assign permissions to Function App:**
   ```bash
   bash infra-scripts/assign-permissions.sh
   ```

4. **Apply blob lifecycle policy:**
   ```bash
   bash infra-scripts/apply-lifecycle-policy.sh
   ```

5. **Deploy function manually:**
   ```bash
   cd archiver-function
   func azure functionapp publish billing-archiver-func
   ```

---

## 📊 Cost Optimization

| Storage Option     | Cost/TB (Est.) | Usage     |
|--------------------|----------------|-----------|
| Cosmos DB          | $$$$            | Active records (<90 days) |
| Blob (Cool Tier)   | $$              | Archived records |
| Blob (Archive Tier)| $               | Aged-out JSON blobs (>180 days) |

Projected cost savings: **60%–80%** reduction in Cosmos DB storage costs.

---

## 🔐 Security & Compliance

- **Managed Identity** used to access Azure services.
- **Scoped RBAC roles** for Cosmos DB and Blob only.
- **No public access** to Blob Containers.
- **Encrypted at rest**: All data is encrypted by Azure-managed keys.

---

## 📈 Monitoring & Maintenance

- Function App logs available in **Application Insights** (can be enabled).
- Monitor Blob container size via **Azure Storage Metrics**.
- Review and adjust lifecycle policy thresholds if needed.

---
🧩 Purpose of dal/billing_service.py

| Benefit                   | Description                                                                |
| ------------------------- | -------------------------------------------------------------------------- |
| Seamless Data Access      | Archived records are still accessible without breaking existing API logic. |
| No API Changes Needed     | Frontend or consumers don’t need to know where the data comes from.        |
| Cost Optimization Support | Can safely purge old records from Cosmos without losing accessibility.     |
| Business Continuity       | Maintains a consistent user experience even for old billing data.          |

---

## Note: .env file should be in .gitignore.
