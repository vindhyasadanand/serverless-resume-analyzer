#!/bin/bash
# Pre-deployment verification script
# Checks if everything is ready for AWS deployment

echo "🔍 Pre-Deployment Verification"
echo "================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

errors=0
warnings=0

# Check 1: Required files
echo "📁 Checking required files..."
required_files=(
    "serverless.yml"
    "wsgi_handler.py"
    "app.py"
    "resume_parser.py"
    "analyzer_simple.py"
    "database.py"
    "database_dynamodb.py"
    "requirements-lambda.txt"
    "package.json"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
    else
        echo -e "  ${RED}✗${NC} $file (MISSING)"
        ((errors++))
    fi
done
echo ""

# Check 2: Node.js and npm
echo "🟢 Checking Node.js and npm..."
if command -v node &> /dev/null; then
    node_version=$(node --version)
    echo -e "  ${GREEN}✓${NC} Node.js $node_version"
else
    echo -e "  ${RED}✗${NC} Node.js not found"
    ((errors++))
fi

if command -v npm &> /dev/null; then
    npm_version=$(npm --version)
    echo -e "  ${GREEN}✓${NC} npm $npm_version"
else
    echo -e "  ${RED}✗${NC} npm not found"
    ((errors++))
fi
echo ""

# Check 3: Serverless Framework
echo "🚀 Checking Serverless Framework..."
if command -v serverless &> /dev/null; then
    sls_version=$(serverless --version | head -n 1)
    echo -e "  ${GREEN}✓${NC} $sls_version"
else
    echo -e "  ${RED}✗${NC} Serverless Framework not installed"
    echo "  Install with: npm install -g serverless"
    ((errors++))
fi
echo ""

# Check 4: npm packages
echo "📦 Checking npm packages..."
if [ -d "node_modules" ]; then
    if [ -d "node_modules/serverless-wsgi" ]; then
        echo -e "  ${GREEN}✓${NC} serverless-wsgi installed"
    else
        echo -e "  ${YELLOW}⚠${NC} serverless-wsgi not found"
        ((warnings++))
    fi
    
    if [ -d "node_modules/serverless-python-requirements" ]; then
        echo -e "  ${GREEN}✓${NC} serverless-python-requirements installed"
    else
        echo -e "  ${YELLOW}⚠${NC} serverless-python-requirements not found"
        ((warnings++))
    fi
else
    echo -e "  ${YELLOW}⚠${NC} node_modules not found - run: npm install"
    ((warnings++))
fi
echo ""

# Check 5: AWS credentials
echo "🔑 Checking AWS credentials..."
if [ -f ~/.aws/credentials ] || [ -n "$AWS_ACCESS_KEY_ID" ]; then
    echo -e "  ${GREEN}✓${NC} AWS credentials found"
else
    echo -e "  ${YELLOW}⚠${NC} AWS credentials not configured"
    echo "  Configure with: serverless config credentials --provider aws --key YOUR_KEY --secret YOUR_SECRET"
    ((warnings++))
fi
echo ""

# Check 6: Python files syntax
echo "🐍 Checking Python files..."
python_files=(
    "app.py"
    "wsgi_handler.py"
    "resume_parser.py"
    "analyzer_simple.py"
    "database_dynamodb.py"
)

for file in "${python_files[@]}"; do
    if [ -f "$file" ]; then
        if python3 -m py_compile "$file" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} $file (syntax OK)"
        else
            echo -e "  ${RED}✗${NC} $file (syntax error)"
            ((errors++))
        fi
    fi
done
echo ""

# Summary
echo "================================"
echo "📊 Verification Summary"
echo "================================"
if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed! Ready to deploy.${NC}"
    echo ""
    echo "To deploy, run:"
    echo "  ./deploy.sh"
    echo "  OR"
    echo "  serverless deploy"
    exit 0
elif [ $errors -eq 0 ]; then
    echo -e "${YELLOW}⚠️  ${warnings} warning(s) found${NC}"
    echo "You can proceed with deployment, but address warnings if possible."
    exit 0
else
    echo -e "${RED}❌ ${errors} error(s) found${NC}"
    echo "Please fix the errors before deploying."
    exit 1
fi
