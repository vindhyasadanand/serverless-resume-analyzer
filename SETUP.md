# Local Setup Guide

Complete instructions for setting up and running the Resume Analyzer locally.

## Prerequisites

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **Git** ([Download](https://git-scm.com/))

Verify installations:
```bash
python3 --version  # Should be 3.11 or higher
node --version     # Should be 18 or higher
npm --version      # Should be 9 or higher
```

---

## Quick Start (5 Minutes)

### 1. Clone Repository
```bash
cd ~/Desktop
git clone <your-repo-url>
cd serverless_res_analyzer
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLP model
python -m spacy download en_core_web_sm

# Run backend server
python app.py
```

Backend should now be running at **http://localhost:5000**

### 3. Frontend Setup (New Terminal)
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend should now be running at **http://localhost:5173**

### 4. Test the Application

1. Open http://localhost:5173 in your browser
2. Upload a sample resume (PDF/TXT/DOCX)
3. Paste a job description
4. Click "Analyze Resume"
5. View results!

---

## Detailed Setup

### Backend Configuration

#### Install Dependencies Individually (if requirements.txt fails):
```bash
pip install Flask==3.0.0
pip install Flask-CORS==4.0.0
pip install PyMuPDF==1.23.8
pip install python-docx==1.1.0
pip install scikit-learn==1.3.2
pip install spacy==3.7.2
pip install nltk==3.8.1
pip install numpy==1.26.2
pip install pandas==2.1.4
pip install python-dotenv==1.0.0
pip install werkzeug==3.0.1
python -m spacy download en_core_web_sm
```

#### Test Backend:
```bash
curl http://localhost:5000
# Should return: {"status": "online", ...}
```

#### Backend Endpoints:
- `GET /` - Health check
- `POST /api/analyze` - Analyze resume
- `GET /api/history` - Get all analyses
- `GET /api/analysis/:id` - Get specific analysis
- `DELETE /api/analysis/:id` - Delete analysis
- `GET /api/stats` - Get statistics

### Frontend Configuration

#### Install Dependencies:
```bash
npm install react react-dom axios recharts
npm install -D vite @vitejs/plugin-react tailwindcss postcss autoprefixer
```

#### Initialize Tailwind (if needed):
```bash
npx tailwindcss init -p
```

#### Test Frontend:
Open http://localhost:5173 - should see the UI

---

## Project Structure

```
serverless_res_analyzer/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── resume_parser.py       # PDF/DOCX parsing
│   ├── analyzer.py            # NLP analysis engine
│   ├── database.py            # SQLite database handler
│   ├── requirements.txt       # Python dependencies
│   ├── uploads/               # Temp file storage (auto-created)
│   └── resume_analyzer.db     # SQLite database (auto-created)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React app
│   │   ├── components/       # React components
│   │   │   ├── UploadForm.jsx
│   │   │   ├── ResultsDisplay.jsx
│   │   │   └── History.jsx
│   │   └── services/
│   │       └── api.js        # API client
│   ├── package.json
│   └── vite.config.js
│
├── README.md                  # Project overview
├── SETUP.md                   # This file
├── DEPLOYMENT.md              # Cloud deployment guide
└── .gitignore
```

---

## Creating Sample Resume

For testing, create a sample resume `sample_resume.txt`:

```text
John Doe
john.doe@email.com | (555) 123-4567

EDUCATION
Bachelor of Science in Computer Science
University of Technology, 2020-2024
GPA: 3.8/4.0

SKILLS
Programming: Python, JavaScript, Java, C++
Web Development: React, Node.js, Flask, Django
Cloud: AWS (Lambda, S3, DynamoDB), Docker
Data Science: Machine Learning, NLP, Pandas, scikit-learn
Databases: PostgreSQL, MongoDB, Redis
Tools: Git, Linux, REST APIs

EXPERIENCE
Software Engineering Intern
Tech Company Inc. | June 2023 - August 2023
- Developed REST APIs using Flask and Python
- Implemented machine learning models for text classification
- Worked with AWS Lambda and S3 for serverless deployment
- Collaborated using Git and Agile methodologies

PROJECTS
Resume Analyzer (Current)
- Built serverless application using AWS Lambda, S3, DynamoDB
- Implemented NLP-based resume parsing using spaCy and scikit-learn
- Created React frontend with modern UI/UX

E-commerce Website
- Full-stack web application using React and Node.js
- Implemented user authentication and payment processing
- Deployed on AWS with CI/CD pipeline
```

Sample Job Description:
```text
We are seeking a Python Developer with the following qualifications:

Required Skills:
- Strong programming skills in Python
- Experience with Flask or Django web frameworks
- Knowledge of AWS services (Lambda, S3, DynamoDB)
- Understanding of machine learning and NLP concepts
- Proficiency with REST API development
- Experience with React for frontend development

Preferred Qualifications:
- Bachelor's degree in Computer Science or related field
- Experience with Docker and containerization
- Knowledge of scikit-learn and data science tools
- Familiarity with Agile development methodologies

Responsibilities:
- Develop and maintain serverless applications
- Build machine learning models for various use cases
- Collaborate with cross-functional teams
- Write clean, maintainable code
```

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 <PID>
```

#### 2. Python Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

#### 3. spaCy Model Missing
```bash
python -m spacy download en_core_web_sm
```

#### 4. CORS Errors
Ensure backend is running on port 5000 and frontend on 5173.
Check `backend/app.py` has `CORS(app)` enabled.

#### 5. Database Issues
```bash
# Delete and recreate database
rm backend/resume_analyzer.db
# Backend will auto-create on next run
```

#### 6. npm Install Fails
```bash
# Clear npm cache
npm cache clean --force
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## Development Tips

### Backend Development

**Hot Reload:**
Flask runs with debug mode by default. Changes auto-reload.

**View Database:**
```bash
sqlite3 backend/resume_analyzer.db
# SQLite commands:
.tables                    # List tables
SELECT * FROM analyses;    # View all analyses
.exit                      # Exit
```

**Add New Endpoint:**
```python
@app.route('/api/your-endpoint', methods=['GET'])
def your_function():
    return jsonify({'message': 'Hello!'})
```

### Frontend Development

**Vite Hot Module Replacement:**
Changes appear instantly in browser.

**Add New Component:**
```javascript
// src/components/NewComponent.jsx
import { useState } from 'react'

function NewComponent() {
  return <div>Your component</div>
}

export default NewComponent
```

**Test API Calls:**
```javascript
import { analyzeResume } from './services/api'

const result = await analyzeResume(file, jobDesc)
console.log(result)
```

---

## Running Tests

### Backend Tests (Manual):
```bash
# Test health endpoint
curl http://localhost:5000

# Test analyze endpoint (with sample files)
curl -X POST http://localhost:5000/api/analyze \
  -F "resume=@sample_resume.pdf" \
  -F "job_description=Python Developer..."

# Test history
curl http://localhost:5000/api/history
```

### Frontend Tests:
Open browser DevTools (F12) → Console for React errors.

---

## Environment Variables

### Backend (optional):
Create `backend/.env`:
```bash
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_PATH=resume_analyzer.db
MAX_FILE_SIZE=5242880
```

### Frontend (optional):
Create `frontend/.env`:
```bash
VITE_API_URL=http://localhost:5000
```

---

## Performance Optimization

### Backend:
- Use production-grade server (Gunicorn):
  ```bash
  pip install gunicorn
  gunicorn -w 4 -b 0.0.0.0:5000 app:app
  ```

### Frontend:
- Build for production:
  ```bash
  npm run build
  npm run preview  # Test production build
  ```

---

## Next Steps

1. ✅ Run locally and test all features
2. ✅ Customize UI colors/branding
3. ✅ Add more NLP features
4. ✅ Deploy to cloud (see DEPLOYMENT.md)
5. ✅ Set up CI/CD pipeline

---

## Getting Help

**Issues?**
- Check logs in terminal
- Inspect browser console (F12)
- Review error messages carefully
- Ensure all dependencies installed
- Verify Python 3.11+ and Node 18+

**Documentation:**
- Flask: https://flask.palletsprojects.com/
- React: https://react.dev/
- scikit-learn: https://scikit-learn.org/
- spaCy: https://spacy.io/

---

**Happy coding! 🚀**






