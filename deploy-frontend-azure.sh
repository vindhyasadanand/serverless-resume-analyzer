#!/bin/bash

# Azure Resume Analyzer - Frontend Deployment Script
# Deploys React frontend to Azure Static Web Apps

set -e

echo "🎨 Azure Static Web Apps Deployment"
echo "===================================="
echo ""

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if deployment-config.txt exists
if [ ! -f "deployment-config.txt" ]; then
    print_warning "Backend not deployed yet. Please run ./deploy-to-azure.sh first!"
    exit 1
fi

# Read backend URL from config
FUNCTION_URL=$(grep "Backend API URL:" deployment-config.txt | cut -d' ' -f4)
print_info "Backend API URL: $FUNCTION_URL"
echo ""

# Update frontend API URL
print_info "Updating frontend API configuration..."
sed -i '' "s|http://localhost:5001|${FUNCTION_URL}|g" frontend/src/services/api.js
print_success "Frontend configured to use: $FUNCTION_URL"
echo ""

# Build frontend
print_info "Building frontend..."
cd frontend
npm install
npm run build
cd ..
print_success "Frontend built successfully"
echo ""

# Instructions for Azure Portal deployment
echo "=========================================="
echo "🌐 Deploy to Azure Static Web Apps"
echo "=========================================="
echo ""
echo "Option 1: Via Azure Portal (Easiest)"
echo "-------------------------------------"
echo "1. Go to: https://portal.azure.com"
echo "2. Click 'Create a resource'"
echo "3. Search 'Static Web Apps'"
echo "4. Click 'Create'"
echo "5. Fill in:"
echo "   - Resource Group: resume-analyzer-rg"
echo "   - Name: resume-analyzer"
echo "   - Plan type: Free"
echo "   - Region: East US 2"
echo ""
echo "6. Deployment Details:"
echo "   - Source: GitHub (or upload dist folder manually)"
echo "   - If GitHub:"
echo "     * Branch: main"
echo "     * Build Presets: React"
echo "     * App location: /frontend"
echo "     * Output location: dist"
echo ""
echo "7. Click 'Review + Create' then 'Create'"
echo ""
echo "Option 2: Upload Built Files"
echo "----------------------------"
echo "1. Your built files are in: frontend/dist/"
echo "2. Go to Azure Portal > Static Web Apps"
echo "3. Upload the dist folder"
echo ""
echo "=========================================="
print_success "Frontend is ready for deployment!"
echo ""
print_info "Your backend is already live at:"
echo "   $FUNCTION_URL"
echo ""

