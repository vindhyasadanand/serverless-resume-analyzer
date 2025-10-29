#!/bin/bash

# Azure Resume Analyzer - Automated Deployment Script
# This script deploys your Resume Analyzer to Azure

set -e  # Exit on error

echo "🚀 Azure Resume Analyzer Deployment Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    print_error "Azure CLI is not installed!"
    echo "Please run: brew install azure-cli"
    exit 1
fi

# Check if Azure Functions Core Tools is installed
if ! command -v func &> /dev/null; then
    print_error "Azure Functions Core Tools is not installed!"
    echo "Please run: brew tap azure/functions && brew install azure-functions-core-tools@4"
    exit 1
fi

print_success "All required tools are installed!"
echo ""

# Step 1: Login to Azure
print_info "Step 1: Checking Azure login status..."
if ! az account show &> /dev/null; then
    print_warning "Not logged in to Azure. Opening login..."
    az login
else
    print_success "Already logged in to Azure"
    az account show --query "{Subscription:name, ID:id}" -o table
fi
echo ""

# Step 2: Set variables
print_info "Step 2: Setting up deployment variables..."
TIMESTAMP=$(date +%s | cut -c6-13)
RESOURCE_GROUP="resume-analyzer-rg"
LOCATION="eastus"
COSMOS_ACCOUNT="resume-cosmos-${TIMESTAMP}"
STORAGE_ACCOUNT="resumestor${TIMESTAMP}"
FUNCTION_APP="resume-func-${TIMESTAMP}"
STATIC_APP="resume-analyzer"

print_info "Resource Group: $RESOURCE_GROUP"
print_info "Location: $LOCATION"
print_info "Cosmos DB: $COSMOS_ACCOUNT"
print_info "Storage: $STORAGE_ACCOUNT"
print_info "Function App: $FUNCTION_APP"
echo ""

# Step 3: Create Resource Group
print_info "Step 3: Creating resource group..."
if az group show --name $RESOURCE_GROUP &> /dev/null; then
    print_warning "Resource group already exists"
else
    az group create --name $RESOURCE_GROUP --location $LOCATION --output none
    print_success "Resource group created"
fi
echo ""

# Step 4: Create Cosmos DB
print_info "Step 4: Creating Cosmos DB (FREE TIER)..."
print_warning "This may take 3-5 minutes..."
if az cosmosdb show --name $COSMOS_ACCOUNT --resource-group $RESOURCE_GROUP &> /dev/null 2>&1; then
    print_warning "Cosmos DB already exists"
else
    az cosmosdb create \
      --name $COSMOS_ACCOUNT \
      --resource-group $RESOURCE_GROUP \
      --locations regionName=$LOCATION \
      --enable-free-tier true \
      --default-consistency-level Session \
      --output none
    print_success "Cosmos DB created"
fi

# Create database
print_info "Creating database..."
az cosmosdb sql database create \
  --account-name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --name resumeDB \
  --output none 2>/dev/null || print_warning "Database may already exist"

# Create container
print_info "Creating container..."
az cosmosdb sql container create \
  --account-name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --database-name resumeDB \
  --name analyses \
  --partition-key-path "/id" \
  --throughput 400 \
  --output none 2>/dev/null || print_warning "Container may already exist"

print_success "Cosmos DB setup complete"
echo ""

# Step 5: Create Storage Account
print_info "Step 5: Creating Storage Account..."
if az storage account show --name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP &> /dev/null 2>&1; then
    print_warning "Storage account already exists"
else
    az storage account create \
      --name $STORAGE_ACCOUNT \
      --resource-group $RESOURCE_GROUP \
      --location $LOCATION \
      --sku Standard_LRS \
      --output none
    print_success "Storage account created"
fi
echo ""

# Step 6: Get Connection Strings
print_info "Step 6: Getting connection strings..."
COSMOS_CONN=$(az cosmosdb keys list \
  --name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --type connection-strings \
  --query "connectionStrings[0].connectionString" -o tsv)

STORAGE_CONN=$(az storage account show-connection-string \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --query "connectionString" -o tsv)

print_success "Connection strings retrieved"
echo ""

# Step 7: Create Function App
print_info "Step 7: Creating Azure Function App..."
if az functionapp show --name $FUNCTION_APP --resource-group $RESOURCE_GROUP &> /dev/null 2>&1; then
    print_warning "Function App already exists"
else
    az functionapp create \
      --resource-group $RESOURCE_GROUP \
      --consumption-plan-location $LOCATION \
      --runtime python \
      --runtime-version 3.11 \
      --functions-version 4 \
      --name $FUNCTION_APP \
      --storage-account $STORAGE_ACCOUNT \
      --os-type Linux \
      --output none
    print_success "Function App created"
fi
echo ""

# Step 8: Configure Function App Settings
print_info "Step 8: Configuring Function App..."
az functionapp config appsettings set \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --settings \
    "COSMOS_CONNECTION_STRING=$COSMOS_CONN" \
    "STORAGE_CONNECTION_STRING=$STORAGE_CONN" \
    "COSMOS_DATABASE=resumeDB" \
    "COSMOS_CONTAINER=analyses" \
    "PYTHON_ENABLE_WORKER_EXTENSIONS=1" \
  --output none

print_success "Function App configured"
echo ""

# Step 9: Deploy Backend Functions
print_info "Step 9: Deploying backend functions..."
print_warning "This may take 3-5 minutes..."
cd azure-backend

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
python -m spacy download en_core_web_sm > /dev/null 2>&1

# Deploy to Azure
func azure functionapp publish $FUNCTION_APP --build remote --python

deactivate
cd ..
print_success "Backend deployed"
echo ""

# Step 10: Enable CORS
print_info "Step 10: Configuring CORS..."
az functionapp cors add \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --allowed-origins "*" \
  --output none

print_success "CORS configured"
echo ""

# Step 11: Get Function App URL
FUNCTION_URL="https://${FUNCTION_APP}.azurewebsites.net/api"
print_info "Backend API URL: $FUNCTION_URL"
echo ""

# Step 12: Save configuration
print_info "Step 12: Saving deployment configuration..."
cat > deployment-config.txt << EOF
Azure Resume Analyzer - Deployment Configuration
================================================

Resource Group: $RESOURCE_GROUP
Location: $LOCATION

Cosmos DB Account: $COSMOS_ACCOUNT
Storage Account: $STORAGE_ACCOUNT
Function App: $FUNCTION_APP

Backend API URL: $FUNCTION_URL

Deployed: $(date)

Next Steps:
1. Deploy frontend to Azure Static Web Apps
2. Update frontend API URL to: $FUNCTION_URL
3. Test all endpoints

Commands:
- View resources: az resource list --resource-group $RESOURCE_GROUP --output table
- View logs: az functionapp log tail --name $FUNCTION_APP --resource-group $RESOURCE_GROUP
- Delete all: az group delete --name $RESOURCE_GROUP --yes
EOF

print_success "Configuration saved to deployment-config.txt"
echo ""

# Summary
echo "=========================================="
echo "🎉 Backend Deployment Complete!"
echo "=========================================="
echo ""
print_success "Backend API: $FUNCTION_URL"
echo ""
echo "📋 Next Steps:"
echo "1. Deploy frontend (I'll create a script for this)"
echo "2. Test backend endpoints:"
echo "   curl $FUNCTION_URL/stats"
echo ""
echo "3. View all resources:"
echo "   az resource list --resource-group $RESOURCE_GROUP --output table"
echo ""
echo "4. View logs:"
echo "   az functionapp log tail --name $FUNCTION_APP --resource-group $RESOURCE_GROUP"
echo ""
print_info "All configuration saved in: deployment-config.txt"
echo ""
print_warning "Keep this terminal output for reference!"
echo ""

