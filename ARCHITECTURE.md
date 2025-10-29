# System Architecture Documentation

## Overview

The Resume Analyzer is built using a modern three-tier architecture with a React frontend, Flask backend, and SQLite database. The system follows RESTful API design principles and serverless architecture patterns.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                    (Browser / Client)                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ HTTPS/HTTP
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                      Frontend Layer                          │
│                   React 18 + Vite + Tailwind                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ UploadForm   │  │   Results    │  │   History    │     │
│  │  Component   │  │   Display    │  │  Dashboard   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │           API Service (Axios)                      │    │
│  │  - analyzeResume()  - getHistory()                 │    │
│  │  - getAnalysis()    - deleteAnalysis()             │    │
│  └────────────────────────────────────────────────────┘    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ REST API (JSON)
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                      Backend Layer                           │
│                   Flask 3.0 + Python 3.11                   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              API Gateway (Flask Routes)            │    │
│  │  POST /api/analyze      - Analyze resume           │    │
│  │  GET  /api/history      - Retrieve analyses        │    │
│  │  GET  /api/analysis/:id - Get specific analysis    │    │
│  │  DELETE /api/analysis/:id - Delete analysis        │    │
│  │  GET  /api/stats        - Get statistics           │    │
│  └─────────┬──────────────────────────────────────────┘    │
│            │                                                 │
│  ┌─────────▼────────────────────────────────────────┐      │
│  │         Business Logic Layer                     │      │
│  │                                                   │      │
│  │  ┌──────────────────┐  ┌────────────────────┐   │      │
│  │  │  Resume Parser   │  │   Analyzer Engine  │   │      │
│  │  │                  │  │                    │   │      │
│  │  │ • PDF Extract    │  │ • TF-IDF Vector    │   │      │
│  │  │ • DOCX Parse     │  │ • Cosine Similarity│   │      │
│  │  │ • Text Clean     │  │ • Score Calculate  │   │      │
│  │  │ • Skill Extract  │  │ • Recommendations  │   │      │
│  │  │ • Section ID     │  │ • Breakdown Logic  │   │      │
│  │  └──────────────────┘  └────────────────────┘   │      │
│  └───────────────────────────────────────────────────┘      │
│            │                                                 │
│  ┌─────────▼────────────────────────────────────────┐      │
│  │         Data Access Layer                        │      │
│  │                                                   │      │
│  │  ┌──────────────────────────────────────────┐   │      │
│  │  │      Database Handler (database.py)      │   │      │
│  │  │  • store_analysis()                      │   │      │
│  │  │  • get_analysis()                        │   │      │
│  │  │  • get_all_analyses()                    │   │      │
│  │  │  • delete_analysis()                     │   │      │
│  │  │  • get_statistics()                      │   │      │
│  │  └──────────────────────────────────────────┘   │      │
│  └───────────────────────────────────────────────────┘      │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ SQL Queries
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                     Database Layer                           │
│                   SQLite 3 (resume_analyzer.db)             │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              analyses Table                        │    │
│  │  • id (PRIMARY KEY)                                │    │
│  │  • filename                                        │    │
│  │  • job_description                                 │    │
│  │  • overall_score                                   │    │
│  │  • skills_score, experience_score, education_score │    │
│  │  • matched_skills (JSON)                           │    │
│  │  • missing_skills (JSON)                           │    │
│  │  • recommendations (JSON)                          │    │
│  │  • resume_data (JSON)                              │    │
│  │  • created_at (TIMESTAMP)                          │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Frontend Components

#### App.jsx (Main Container)
- Manages application state
- Handles tab navigation (Analyze / History)
- Coordinates child components

#### UploadForm.jsx
- File upload handling
- Job description input
- Form validation
- API call to backend
- Error display

#### ResultsDisplay.jsx
- Score visualization (pie chart)
- Matched/missing skills display
- Recommendations list
- Color-coded score badges

#### History.jsx
- Fetches analysis history
- Displays statistics cards
- Lists past analyses
- Delete functionality

#### API Service (api.js)
- Axios-based HTTP client
- Centralized API endpoints
- Error handling
- Request/response formatting

---

### 2. Backend Components

#### app.py (API Gateway)
**Responsibilities:**
- Route handling
- Request validation
- File upload management
- Response formatting
- Error handling
- CORS configuration

**Key Functions:**
```python
@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    # 1. Validate request (file + job description)
    # 2. Save file temporarily
    # 3. Parse resume → resume_data
    # 4. Analyze compatibility → analysis_result
    # 5. Store in database → analysis_id
    # 6. Return JSON response
    # 7. Cleanup temp file
```

#### resume_parser.py (Parsing Engine)
**Responsibilities:**
- Multi-format file parsing (PDF, TXT, DOCX)
- Text extraction
- Section identification
- Skill extraction
- Contact info extraction

**Key Classes:**
```python
class ResumeParser:
    def parse_resume(filepath) -> Dict:
        # Extract text based on file type
        # Identify sections (education, experience, skills)
        # Extract skills using keyword matching
        # Extract contact information
        # Return structured data dictionary
```

#### analyzer.py (NLP Engine)
**Responsibilities:**
- TF-IDF vectorization
- Cosine similarity calculation
- Score computation
- Skills matching
- Recommendation generation

**Key Algorithm:**
```python
class ResumeAnalyzer:
    def analyze(resume_data, job_description) -> Dict:
        # 1. Calculate overall similarity (TF-IDF + cosine)
        # 2. Extract job requirements/skills
        # 3. Match resume skills with job skills
        # 4. Calculate category breakdowns
        # 5. Generate personalized recommendations
        # 6. Return comprehensive result dictionary
```

#### database.py (Data Layer)
**Responsibilities:**
- SQLite connection management
- CRUD operations
- Data serialization (JSON)
- Query optimization

**Key Functions:**
```python
class Database:
    def store_analysis(...)     # INSERT new analysis
    def get_analysis(id)        # SELECT by ID
    def get_all_analyses(...)   # SELECT all with limit
    def delete_analysis(id)     # DELETE by ID
    def get_statistics()        # Aggregate queries
```

---

## Data Flow

### Analysis Request Flow

```
1. User uploads resume + job description
         ↓
2. Frontend validates inputs
         ↓
3. Axios sends POST /api/analyze with FormData
         ↓
4. Flask receives request, validates file
         ↓
5. File saved temporarily to backend/uploads/
         ↓
6. ResumeParser.parse_resume(filepath)
   - Extracts text
   - Identifies sections
   - Extracts skills
   → Returns resume_data dict
         ↓
7. ResumeAnalyzer.analyze(resume_data, job_description)
   - Vectorizes texts (TF-IDF)
   - Calculates cosine similarity
   - Matches skills
   - Generates recommendations
   → Returns analysis_result dict
         ↓
8. Database.store_analysis(...)
   - Inserts into SQLite
   → Returns analysis_id
         ↓
9. Temp file deleted
         ↓
10. JSON response sent to frontend
         ↓
11. ResultsDisplay renders visualization
```

### History Request Flow

```
1. User clicks "History" tab
         ↓
2. Frontend calls getHistory()
         ↓
3. Axios sends GET /api/history
         ↓
4. Flask routes to get_history()
         ↓
5. Database.get_all_analyses(limit=50)
   - SELECT * FROM analyses ORDER BY created_at DESC
   → Returns list of analyses
         ↓
6. Database.get_statistics()
   - Aggregate queries (COUNT, AVG, MAX, MIN)
   → Returns stats dict
         ↓
7. JSON response sent to frontend
         ↓
8. History component renders list + stats cards
```

---

## NLP Pipeline Architecture

```
Resume Text Input
      ↓
┌─────────────────────┐
│  Preprocessing      │
│  • Lowercase        │
│  • Remove specials  │
│  • Tokenization     │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  Feature Extraction │
│  • Skills (regex)   │
│  • Education        │
│  • Experience       │
│  • Contact info     │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  Vectorization      │
│  TfidfVectorizer    │
│  • stop_words       │
│  • max_features=500 │
│  • ngram_range(1,2) │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  Similarity Score   │
│  cosine_similarity  │
│  Resume ⟷ Job Desc  │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  Score Calculation  │
│  • Overall (0-100)  │
│  • Skills %         │
│  • Experience %     │
│  • Education %      │
│  • Format %         │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  Recommendations    │
│  • Based on score   │
│  • Missing skills   │
│  • Section gaps     │
└─────────────────────┘
```

---

## Security Considerations

### Frontend
- Input sanitization
- File type validation
- File size limits (5MB)
- XSS prevention (React's default escaping)

### Backend
- Secure file upload (werkzeug.secure_filename)
- File type whitelist (PDF, TXT, DOCX only)
- Temporary file cleanup
- SQL injection prevention (parameterized queries)
- CORS configuration
- Error message sanitization

### Database
- No sensitive personal data stored (except emails/phones if in resume)
- SQLite file permissions
- No direct SQL execution from user input

---

## Scalability Considerations

### Current Architecture (Local)
- **Concurrent Users:** 10-20
- **Request Processing:** Synchronous
- **Database:** SQLite (single file)
- **File Storage:** Local filesystem

### Cloud Architecture (Production)

```
┌─────────────────────────────────────┐
│  CDN (Cloudflare / Vercel Edge)    │
│  - Static assets caching           │
└──────────────┬──────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  Load Balancer                       │
│  (Railway / Render auto-scaling)     │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  API Servers (Multiple Instances)    │
│  Flask + Gunicorn (4 workers each)   │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  PostgreSQL Database                 │
│  (Supabase / Render Postgres)        │
└──────────────────────────────────────┘
               +
┌──────────────────────────────────────┐
│  Object Storage (S3 / R2)            │
│  - Resume file archival              │
└──────────────────────────────────────┘
```

### Optimization Strategies

1. **Caching:**
   - Redis for frequently accessed analyses
   - CDN for frontend assets

2. **Async Processing:**
   - Celery + RabbitMQ for long-running analysis
   - WebSocket for real-time updates

3. **Database:**
   - PostgreSQL for better concurrency
   - Indexing on `created_at`, `overall_score`
   - Connection pooling

4. **File Storage:**
   - S3/R2 for resume storage
   - Presigned URLs for direct uploads

---

## Technology Justifications

| Technology | Justification |
|------------|---------------|
| **React** | Component reusability, virtual DOM performance, large ecosystem |
| **Flask** | Lightweight, easy to learn, perfect for REST APIs, Python ML libraries |
| **SQLite** | Zero configuration, portable, perfect for local dev, easy migration |
| **scikit-learn** | Industry-standard ML library, excellent TF-IDF implementation |
| **PyMuPDF** | Fast PDF parsing, accurate text extraction |
| **Tailwind CSS** | Rapid UI development, consistent styling, responsive by default |
| **Vite** | Fast HMR, optimized builds, modern tooling |

---

## API Contract

### POST /api/analyze

**Request:**
```
Content-Type: multipart/form-data

resume: [FILE] (PDF/TXT/DOCX, max 5MB)
job_description: [TEXT] (required)
```

**Response:**
```json
{
  "success": true,
  "analysis_id": 123,
  "score": 78.5,
  "breakdown": {
    "skills": 85.0,
    "experience": 70.0,
    "education": 80.0,
    "format": 90.0
  },
  "matched_skills": ["python", "flask", "aws"],
  "missing_skills": ["kubernetes", "docker"],
  "recommendations": ["Consider adding...", "..."],
  "timestamp": "2025-10-28T12:34:56"
}
```

### GET /api/history

**Response:**
```json
{
  "success": true,
  "count": 10,
  "analyses": [
    {
      "id": 123,
      "filename": "resume.pdf",
      "overall_score": 78.5,
      "breakdown": {...},
      "created_at": "2025-10-28T12:34:56"
    },
    ...
  ]
}
```

---

## Future Architecture Enhancements

1. **Microservices:** Separate parsing, analysis, and storage services
2. **Event-Driven:** Kafka for async processing
3. **Containerization:** Docker + Kubernetes
4. **CI/CD:** GitHub Actions automated testing and deployment
5. **Monitoring:** Prometheus + Grafana
6. **Authentication:** JWT-based user accounts
7. **Rate Limiting:** Protect against abuse

---

## Conclusion

This architecture provides:
- ✅ Separation of concerns (frontend/backend/database)
- ✅ RESTful API design
- ✅ Scalability path from local to cloud
- ✅ Maintainable codebase with clear responsibilities
- ✅ Modern tech stack with strong community support

**Total Components:** 7 main modules, ~3000 lines of code  
**Architecture Pattern:** Three-tier with RESTful API  
**Deployment Ready:** Local, cloud, or containerized






