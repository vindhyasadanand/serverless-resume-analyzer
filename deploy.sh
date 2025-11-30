#!/bin/bash
# Deploy Resume Analyzer to AWS Lambda
# Run this script to deploy your application

set -e  # Exit on error

echo "🚀 Starting deployment to AWS Lambda..."
echo ""

# Step 1: Check prerequisites
echo "📋 Step 1: Checking prerequisites..."
if ! command -v serverless &> /dev/null; then
    echo "❌ Serverless Framework not found. Installing..."
    npm install -g serverless
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js first."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Step 2: Install npm dependencies
echo "📦 Step 2: Installing npm dependencies..."
npm install
echo "✅ Dependencies installed"
echo ""

# Step 3: Verify serverless config
echo "🔍 Step 3: Verifying serverless configuration..."
if [ ! -f "serverless.yml" ]; then
    echo "❌ serverless.yml not found!"
    exit 1
fi

if [ ! -f "wsgi_handler.py" ]; then
    echo "❌ wsgi_handler.py not found!"
    exit 1
fi

echo "✅ Configuration files verified"
echo ""

# Step 4: Package check
echo "📝 Step 4: Validating package..."
if [ ! -f "requirements-lambda.txt" ]; then
    echo "❌ requirements-lambda.txt not found!"
    exit 1
fi

echo "✅ Package validation passed"
echo ""

# Step 5: Deploy
echo "🚀 Step 5: Deploying to AWS..."
echo "This will take 3-5 minutes..."
echo ""

serverless deploy --verbose

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Your API endpoint will be shown above"
echo "🔗 Look for: 'endpoints:' in the output"
echo ""
echo "To test your API:"
echo "  serverless invoke -f api --log"
echo ""
echo "To view logs:"
echo "  serverless logs -f api --tail"
echo ""
echo "To remove deployment:"
echo "  serverless remove"
