# Serverless Resume Analyzer

**Project Group 20 - Cloud Computing Course**  
**Team Members:** Keyur Nareshkumar Modi, Naveen John, Vindhya Sadanand Hegde  
**Institution:** [Your University]

## 🎯 Overview

A cloud-based resume analysis system that intelligently matches resumes against job descriptions using advanced NLP techniques. Our system employs TF-IDF vectorization and cosine similarity to produce accurate compatibility scores, helping both recruiters and job seekers.

**Live Demo:** [Add your Azure URL here after deployment]  
**Video Demo:** [Add YouTube link if you create one]

## Features

- 📄 Resume parsing (PDF, TXT, DOCX)
- 🎯 Job description matching using NLP
- 📊 Compatibility scoring with detailed breakdown
- 🔍 Skills, education, and experience extraction
- 💾 Analysis history storage
- 🌐 Modern web interface

## Architecture

### Local Development (No Card Required)
- **Backend**: Python Flask API
- **Storage**: Local filesystem + SQLite
- **Processing**: Python NLP libraries (scikit-learn, PyMuPDF, spaCy)
- **Frontend**: React with Vite

### Free Cloud Deployment Options

#### Option 1: Railway.app (Recommended)
- Backend + Database hosting (500 hrs/month free)
- No card required for initial use
- Easy deployment from GitHub

#### Option 2: Render.com
- Free web services + PostgreSQL
- No card required
- Auto-deploys from Git

#### Option 3: Vercel + Supabase
- Vercel: Frontend + Serverless functions
- Supabase: Database + Storage (500MB free)
- No card required

## Tech Stack

**Backend:**
- Python 3.11
- Flask (REST API) / AWS Lambda
- PyMuPDF (PDF parsing)
- scikit-learn (TF-IDF, cosine similarity)
- spaCy (NLP processing)
- SQLite (local) / DynamoDB (AWS)

**Frontend:**
- React 18
- Vite
- Tailwind CSS
- Axios

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+

### Local Development (5 minutes)

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py  # Runs on http://localhost:5001
```

**Frontend (new terminal):**
```bash
cd frontend
npm install
npm run dev  # Opens http://localhost:5173
```

**Or use the helper scripts:**
```bash
./run_backend.sh   # Terminal 1
./run_frontend.sh  # Terminal 2
```

For detailed setup instructions, see [SETUP.md](SETUP.md)

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | This file - project overview |
| [SETUP.md](SETUP.md) | Local development setup |
| [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md) | AWS deployment guide |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture and design |
| [PROJECT_REPORT.md](PROJECT_REPORT.md) | Complete academic report |
| [ORIGINALITY_STATEMENT.md](ORIGINALITY_STATEMENT.md) | Proof of original work |

## 🎥 Usage

1. **Upload Resume:** PDF, TXT, or DOCX file (up to 5MB)
2. **Enter Job Description:** Paste the job posting text
3. **Analyze:** Click the analyze button
4. **View Results:**
   - Overall compatibility score (0-100%)
   - Category breakdown (Skills, Experience, Education, Format)
   - Matched skills ✅
   - Missing skills ❌
   - Personalized recommendations 💡
5. **Review History:** Check past analyses and statistics

## Project Structure

```
serverless_res_analyzer/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── resume_parser.py       # Resume extraction logic
│   ├── analyzer.py            # NLP scoring engine
│   ├── database.py            # Database operations
│   ├── requirements.txt       # Python dependencies
│   └── uploads/               # Temporary file storage
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── components/       # UI components
│   │   └── services/         # API calls
│   ├── package.json
│   └── vite.config.js
├── serverless.yml             # AWS Lambda configuration
├── wsgi_handler.py            # Lambda function handler
├── AWS_DEPLOYMENT.md          # Complete AWS deployment guide
└── README.md
```

## API Endpoints

- `POST /api/analyze` - Analyze resume against job description
- `GET /api/history` - Get analysis history
- `GET /api/analysis/:id` - Get specific analysis
- `DELETE /api/analysis/:id` - Delete analysis

## ☁️ Cloud Deployment (AWS)

**We deployed to Amazon Web Services using AWS Free Tier.**

**Our Live URLs:**
- Frontend: [Your Frontend URL - after deployment]
- Backend API: [Your API Gateway URL - after deployment]

**AWS Architecture:**
- **AWS Lambda** - Serverless backend compute
- **Amazon API Gateway** - RESTful API endpoints
- **Amazon DynamoDB** - NoSQL database (25GB free)
- **Amazon S3** - Resume file storage (5GB free)

**Cost:** $0/month within AWS Free Tier limits

**Deployment Guide:** See [AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md) for complete instructions.

## 🆓 Alternative Deployment Options

### Deploy to Railway.app (No Card Required)

1. Push code to GitHub
2. Visit railway.app and sign up with GitHub
3. Create new project from repo
4. Railway auto-detects and deploys
5. Add environment variables if needed

### Deploy to Render.com

1. Push code to GitHub
2. Sign up at render.com
3. Create new Web Service
4. Connect GitHub repo
5. Configure build/start commands
6. Deploy!

## NLP Scoring Methodology

1. **Text Extraction**: Parse resume using PyMuPDF and regex
2. **Preprocessing**: Tokenization, lowercasing, stopword removal
3. **Vectorization**: TF-IDF transformation of resume and job description
4. **Similarity**: Cosine similarity calculation
5. **Scoring**: 0-100 scale with category breakdowns (skills, experience, education)

## License

MIT License - Academic Project

## 🎓 Academic Information

**Course:** Cloud Computing  
**Semester:** [Add semester]  
**Grade Target:** Demonstrate understanding of serverless architecture and NLP

### Learning Outcomes Demonstrated:
✅ Serverless computing principles (Azure Functions)  
✅ NoSQL databases (Cosmos DB)  
✅ Cloud storage (Blob Storage)  
✅ REST API design  
✅ NLP and machine learning (TF-IDF, cosine similarity)  
✅ Full-stack development  
✅ DevOps and CI/CD  

## 👥 Team Contributions

**Keyur Nareshkumar Modi** - Backend & NLP Lead
- Flask API design and implementation
- NLP algorithm (TF-IDF, cosine similarity)
- Resume parser and analyzer modules
- Database schema design

**Naveen John** - Cloud Architecture & DevOps
- Azure infrastructure setup
- Deployment strategy and CI/CD
- Cost optimization
- System monitoring and testing

**Vindhya Sadanand Hegde** - Frontend & UI/UX Lead
- React component architecture
- UI/UX design (Tailwind CSS)
- API integration
- Responsive layout design

---

Built with ❤️ for Cloud Computing Course






