# 🚀 AWS Deployment Checklist - FIXED VERSION

## ✅ Issues Fixed

1. ✅ **Created `wsgi_handler.py`** - Lambda entry point
2. ✅ **Added Flask-CORS** to requirements-lambda.txt
3. ✅ **Created `database_dynamodb.py`** - DynamoDB support for Lambda
4. ✅ **Updated `app.py`** - Auto-detects Lambda environment
5. ✅ **Updated `serverless.yml`** - Includes all necessary files
6. ✅ **Added boto3 and scikit-learn** to Lambda requirements
7. ✅ **Created `deploy.sh`** - Automated deployment script

---

## 📋 Pre-Deployment Checklist

### 1. AWS Account Setup ✓
- [ ] Have AWS account (free tier is fine)
- [ ] Have credit card added (for verification, won't be charged)

### 2. Install Serverless Framework
```bash
npm install -g serverless
serverless --version
```

### 3. Configure AWS Credentials

**Option A: Using AWS IAM User (Recommended)**
```bash
# 1. Go to AWS Console: https://console.aws.amazon.com
# 2. Search for "IAM" → "Users" → "Create user"
# 3. Username: serverless-deploy
# 4. Attach policy: AdministratorAccess
# 5. Create access key (CLI type)
# 6. Save the Access Key ID and Secret Access Key

# Configure serverless
serverless config credentials \
  --provider aws \
  --key YOUR_ACCESS_KEY_ID \
  --secret YOUR_SECRET_ACCESS_KEY
```

**Option B: Using AWS CLI**
```bash
# Install AWS CLI
brew install awscli  # macOS

# Configure
aws configure
# Enter: Access Key, Secret Key, Region (us-east-1), Output format (json)
```

### 4. Verify Setup
```bash
cd ~/Desktop/serverless_res_analyzer

# Check serverless plugins
npm list --depth=0

# Should see:
# ├── serverless-python-requirements@6.1.2
# └── serverless-wsgi@3.1.0
```

---

## 🚀 Deployment Steps

### Method 1: Automated Deployment (Recommended)
```bash
./deploy.sh
```

### Method 2: Manual Deployment
```bash
# 1. Install dependencies
npm install

# 2. Deploy to AWS
serverless deploy --verbose

# Wait 3-5 minutes for deployment
```

---

## 🎯 What Gets Deployed

```
AWS Resources Created:
├── Lambda Function (resume-analyzer-dev-api)
├── API Gateway (REST API endpoints)
├── DynamoDB Table (resume-analyzer-dev)
├── S3 Bucket (resume-analyzer-resumes-dev-191371353627)
├── IAM Roles (auto-generated permissions)
└── CloudWatch Logs (for monitoring)

Estimated Monthly Cost: $0 (within free tier)
```

---

## 📝 After Deployment

### Get Your API Endpoint
After successful deployment, you'll see:
```
endpoints:
  ANY - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/{proxy+}
  ANY - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev
```

**Your API URL is:** `https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev`

### Test Your Deployment

**1. Health Check**
```bash
curl https://YOUR_API_URL/health
```

**2. Test with Python**
```python
import requests

api_url = "https://YOUR_API_URL"

# Test health endpoint
response = requests.get(f"{api_url}/health")
print(response.json())
```

**3. View Logs**
```bash
# Real-time logs
serverless logs -f api --tail

# Specific invocation
serverless invoke -f api --log
```

---

## 🔧 Common Issues & Solutions

### Issue 1: "Serverless command not found"
```bash
npm install -g serverless
# Or use npx
npx serverless deploy
```

### Issue 2: "Unable to find credentials"
```bash
# Reconfigure AWS credentials
serverless config credentials \
  --provider aws \
  --key YOUR_ACCESS_KEY \
  --secret YOUR_SECRET_KEY \
  --overwrite
```

### Issue 3: "Package is too large"
The deployment package might be large due to dependencies. This is normal for ML libraries (scikit-learn).
- Lambda allows up to 250MB unzipped
- Your package should be around 100-150MB

If it fails:
```bash
# Use slim package without heavy dependencies
# Remove scikit-learn from requirements-lambda.txt temporarily
```

### Issue 4: "Table already exists"
```bash
# Remove existing deployment first
serverless remove

# Then redeploy
serverless deploy
```

### Issue 5: "Access Denied"
Your IAM user needs these permissions:
- Lambda (create/update functions)
- API Gateway (create/update APIs)
- DynamoDB (create tables)
- S3 (create buckets)
- CloudFormation (stack operations)
- IAM (create roles)

---

## 📊 Monitoring

### View CloudWatch Logs
```bash
# In AWS Console:
1. Go to CloudWatch
2. Log groups
3. Find: /aws/lambda/resume-analyzer-dev-api
```

### Check DynamoDB
```bash
# In AWS Console:
1. Go to DynamoDB
2. Tables
3. Find: resume-analyzer-dev
```

### Check S3 Bucket
```bash
# In AWS Console:
1. Go to S3
2. Find: resume-analyzer-resumes-dev-191371353627
```

---

## 🗑️ Cleanup (Remove Deployment)

```bash
serverless remove

# This will delete:
# - Lambda function
# - API Gateway
# - DynamoDB table (DATA WILL BE LOST!)
# - S3 bucket (must be empty)
# - IAM roles
```

---

## 🎓 Next Steps

1. **Update Frontend**: Point your React/Streamlit frontend to the API URL
2. **Add Custom Domain**: Use Route53 + API Gateway custom domain
3. **Add Authentication**: Implement AWS Cognito or API keys
4. **Monitor Costs**: Set up billing alerts in AWS
5. **Enable HTTPS**: API Gateway provides HTTPS by default

---

## 📞 Getting Help

**Deployment Failed?**
1. Check the error message carefully
2. Look for specific AWS service errors
3. Verify IAM permissions
4. Check CloudFormation stack in AWS Console

**Still Stuck?**
- Check AWS CloudFormation console for stack events
- Review CloudWatch logs for runtime errors
- Verify all files are included in package

---

## ✅ Deployment Success Indicators

You know deployment succeeded when you see:

```
Serverless: Stack update finished...
Service Information
service: resume-analyzer
stage: dev
region: us-east-1
stack: resume-analyzer-dev
resources: 15
api keys: None
endpoints:
  ANY - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/{proxy+}
  ANY - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev
functions:
  api: resume-analyzer-dev-api
```

🎉 **Congratulations! Your serverless resume analyzer is live!**
