# 🚀 AWS Deployment Guide - Resume Analyzer

Complete guide to deploy your Resume Analyzer to AWS using Lambda, DynamoDB, and S3.

---

## ✅ What You'll Deploy

```
Your AWS Architecture:
├── AWS Lambda (Backend API) - FREE 1M requests/month
├── API Gateway (REST endpoints) - FREE 1M requests/month  
├── DynamoDB (Database) - FREE 25GB storage
└── S3 (Resume storage) - FREE 5GB storage

Total Cost: $0/month within free tier
```

---

## 📋 Prerequisites

1. ✅ AWS Account (free tier)
2. ✅ Credit/debit card (for verification, won't charge)
3. ✅ Node.js installed (`node --version`)
4. ✅ Python 3.11 installed

---

## 🎯 Step-by-Step Deployment

### Step 1: Install Serverless Framework

```bash
# Install globally
npm install -g serverless

# Verify installation
serverless --version
```

### Step 2: Configure AWS Credentials

After creating your AWS account:

1. **Go to AWS Console:** https://console.aws.amazon.com
2. **Search for "IAM"** in the search bar
3. Click **"Users"** → **"Create user"**
4. Username: `serverless-deploy`
5. Check **"Provide user access to AWS Management Console"**
6. Click **"Next"**
7. **Permissions:** Attach policies directly
   - Search and select: `AdministratorAccess` (for deployment)
8. Click **"Create user"**
9. **Create Access Key:**
   - Click on the user
   - Go to **"Security credentials"** tab
   - Click **"Create access key"**
   - Choose **"Command Line Interface (CLI)"**
   - Click **"Next"** → **"Create access key"**
   - **SAVE THESE:**
     - Access Key ID
     - Secret Access Key

### Step 3: Configure Serverless

```bash
cd ~/Desktop/serverless_res_analyzer

# Configure AWS credentials
serverless config credentials \
  --provider aws \
  --key YOUR_ACCESS_KEY_ID \
  --secret YOUR_SECRET_ACCESS_KEY
```

### Step 4: Install Serverless Plugins

```bash
# Install required plugins
npm install --save-dev serverless-wsgi serverless-python-requirements
```

### Step 5: Deploy to AWS!

```bash
# Deploy everything
serverless deploy

# This will:
# ✅ Create Lambda function
# ✅ Create API Gateway
# ✅ Create DynamoDB table
# ✅ Create S3 bucket
# ✅ Upload your code
# Takes 3-5 minutes
```

### Step 6: Get Your URL

After deployment succeeds, you'll see:

```
✔ Service deployed to stack resume-analyzer-dev

endpoints:
  ANY - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/{proxy+}
  ANY - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev
```

**Copy that URL!** That's your live backend API! 🎉

---

## 🧪 Test Your Deployment

```bash
# Test the API
curl https://YOUR-API-URL.amazonaws.com/dev/

# Should return:
# {"status":"online","message":"Resume Analyzer API v1.0",...}
```

---

## 🎨 Deploy Frontend to AWS S3 + CloudFront

### Option 1: S3 Static Website

```bash
cd frontend

# Build the frontend
npm run build

# Create S3 bucket for frontend
aws s3 mb s3://resume-analyzer-frontend --region us-east-1

# Configure for static website
aws s3 website s3://resume-analyzer-frontend \
  --index-document index.html \
  --error-document index.html

# Upload built files
aws s3 sync dist/ s3://resume-analyzer-frontend --acl public-read

# Your frontend URL:
# http://resume-analyzer-frontend.s3-website-us-east-1.amazonaws.com
```

### Option 2: Deploy Frontend to Netlify/Vercel (Easier)

Frontend can be on any CDN - AWS backend works with any frontend!

---

## 📊 Monitor Your Application

### View Logs:
```bash
# View Lambda logs
serverless logs -f api -t

# Or in AWS Console:
# CloudWatch → Logs → /aws/lambda/resume-analyzer-dev-api
```

### Check Costs:
```bash
# AWS Console → Billing Dashboard
# Should show $0 within free tier
```

---

## 🔧 Update Your Deployment

After making code changes:

```bash
# Redeploy
serverless deploy

# Or just update function (faster):
serverless deploy function -f api
```

---

## 📝 Environment Variables

Add secrets without putting them in code:

```bash
serverless deploy --param="OPENAI_KEY=your-key-here"
```

---

## 🗑️ Cleanup (After Grading)

To remove everything and avoid any charges:

```bash
serverless remove
```

This deletes:
- ✅ Lambda function
- ✅ API Gateway
- ✅ DynamoDB table
- ✅ S3 bucket
- ✅ CloudWatch logs

---

## 💰 Cost Monitoring

**Free Tier Limits:**
- Lambda: 1M requests/month + 400,000 GB-seconds compute
- DynamoDB: 25GB storage + 25 read/write units
- S3: 5GB storage + 20,000 GET requests
- API Gateway: 1M API calls/month

**Your project usage:** ~100 requests/day = **$0/month** ✅

---

## 🎓 For Your Project Report

### AWS Services Used:

**1. AWS Lambda**
- Serverless compute (Python 3.11)
- Auto-scaling
- Pay-per-execution model

**2. Amazon API Gateway**
- RESTful API endpoints
- CORS enabled
- Request validation

**3. Amazon DynamoDB**
- NoSQL database
- On-demand billing
- Single-table design

**4. Amazon S3**
- Object storage for resumes
- 99.99% durability
- Lifecycle policies

### Architecture Diagram:

```
User → CloudFront/S3 (Frontend)
         ↓
      API Gateway
         ↓
      AWS Lambda (Your Flask App)
         ↓
    ┌────┴────┐
    ↓         ↓
DynamoDB    S3 Bucket
(Metadata) (Files)
```

---

## ✅ Success Checklist

- [ ] AWS account created
- [ ] Serverless framework installed
- [ ] AWS credentials configured
- [ ] `serverless deploy` succeeded
- [ ] API Gateway URL works
- [ ] Frontend can connect to backend
- [ ] DynamoDB storing data
- [ ] S3 storing files

---

## 🆘 Troubleshooting

### Error: "Inaccessible host: `lambda.us-east-1.amazonaws.com'"
**Fix:** Check your AWS credentials
```bash
aws configure list
```

### Error: "CREATE_FAILED"
**Fix:** Check CloudFormation in AWS Console for detailed error

### Error: "Module not found"
**Fix:** Make sure plugins are installed:
```bash
npm install
```

---

## 🎉 You're Live on AWS!

After deployment you have:
- ✅ Production-grade serverless backend
- ✅ Auto-scaling infrastructure
- ✅ Pay-per-use pricing ($0 for your usage)
- ✅ AWS in your resume! 

**Congratulations!** 🚀

