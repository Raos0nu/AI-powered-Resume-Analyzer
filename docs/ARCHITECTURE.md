# 🏗️ Architecture Documentation

## System Overview

The AI-Powered Resume Analyzer is a full-stack web application built with a Flask REST API backend and vanilla JavaScript frontend. The system uses Natural Language Processing (NLP) and Machine Learning techniques to analyze resumes and provide ATS compatibility scores.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Web Browser                            │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │  │
│  │  │ index.html │  │ styles.css │  │   script.js      │   │  │
│  │  │            │  │            │  │  (UI Logic &     │   │  │
│  │  │            │  │            │  │   API Calls)     │   │  │
│  │  └────────────┘  └────────────┘  └──────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────┘
                                │ HTTP/HTTPS
                                │ (REST API)
┌───────────────────────────────▼─────────────────────────────────┐
│                         API LAYER                                │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Flask Application                      │  │
│  │                       (app.py)                            │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  API Endpoints:                                     │  │  │
│  │  │  - POST /api/v1/analyze                            │  │  │
│  │  │  - POST /api/v1/extract-skills                     │  │  │
│  │  │  - GET  /api/v1/health                             │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Middleware & Config                      │  │
│  │  - CORS Handler                                          │  │
│  │  - Error Handler                                         │  │
│  │  - File Upload Validator                                 │  │
│  │  - Config Management (config.py)                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                        │
│                                                                  │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ resume_parser.py│  │   matcher.py     │  │   utils.py   │  │
│  │                 │  │                  │  │              │  │
│  │ - PDF Extract   │  │ - Skill Extract  │  │ - Clean Text │  │
│  │ - DOCX Extract  │  │ - ATS Scoring    │  │ - Validate   │  │
│  │ - TXT Extract   │  │ - Similarity     │  │ - Extract    │  │
│  │ - Metadata      │  │ - Matching       │  │   Metadata   │  │
│  └─────────────────┘  └──────────────────┘  └──────────────┘  │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                         DATA LAYER                               │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │  File System     │  │  scikit-learn    │  │  PyPDF2 /    │  │
│  │  (uploads/)      │  │  (TF-IDF, etc.)  │  │  python-docx │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Client Layer (Frontend)

#### Technologies
- HTML5, CSS3, JavaScript (ES6+)
- No frameworks - pure vanilla JS for simplicity

#### Responsibilities
- User interface rendering
- File upload handling (drag & drop)
- Form validation
- API communication via Fetch API
- Results visualization
- Error handling and user feedback

#### Key Files
- `index.html` - Main page structure
- `styles.css` - Styling with modern CSS (Grid, Flexbox, Animations)
- `script.js` - UI logic, API calls, DOM manipulation

---

### 2. API Layer (Backend)

#### Technologies
- Flask 3.0.0 - Web framework
- Flask-CORS - Cross-origin resource sharing

#### Responsibilities
- Route handling
- Request validation
- Response formatting
- Error handling
- CORS management
- File upload processing

#### Endpoints

**POST /api/v1/analyze**
- Accepts resume file + optional job description
- Returns comprehensive analysis

**POST /api/v1/extract-skills**
- Accepts text input
- Returns extracted skills

**GET /api/v1/health**
- Returns API health status

#### app.py Structure
```python
Flask App Initialization
  ↓
CORS Configuration
  ↓
Route Definitions
  ↓
Request Handlers
  ├── File Validation
  ├── Business Logic Call
  └── Response Formation
  ↓
Error Handlers
  ├── 400 Bad Request
  ├── 404 Not Found
  ├── 413 File Too Large
  └── 500 Internal Error
```

---

### 3. Business Logic Layer

#### A. Resume Parser (resume_parser.py)

**Purpose:** Extract text from various file formats

**Functions:**
```python
extract_text_from_pdf(path)      # PDF processing
extract_text_from_docx(path)     # DOCX processing
extract_text_from_txt(path)      # TXT processing
extract_text_from_file(path)     # Main dispatcher
extract_resume_metadata(text)     # Extract email, phone, URLs
```

**Dependencies:**
- PyPDF2 - PDF text extraction
- python-docx - DOCX file parsing

---

#### B. Matcher (matcher.py)

**Purpose:** Skill extraction, matching, and ATS scoring

**Core Algorithm:**

```
ATS Score Calculation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Score = Σ (Component Score × Weight)

Components:
├── Skill Match (40% weight)
│   └── (Matching Skills / JD Skills) × 100
│
├── Keyword Density (30% weight)
│   └── (Keyword Count / Total Words) × 1000
│
├── Content Similarity (20% weight)
│   └── TF-IDF Cosine Similarity × 100
│
└── Format Quality (10% weight)
    └── Resume Structure Analysis
```

**Functions:**
```python
extract_skills(text, categorize)       # Extract technical skills
calculate_skill_match_score()          # Match percentage
calculate_content_similarity()         # TF-IDF similarity
analyze_resume_format()                # Format quality
calculate_ats_score()                  # Overall ATS score
```

**Skill Database:**
- 100+ technical skills across 7 categories
- Programming languages
- Web technologies
- Databases
- Cloud & DevOps
- Data Science & AI
- Tools & frameworks
- Security & networking

---

#### C. Utils (utils.py)

**Purpose:** Utility functions for validation and processing

**Functions:**
```python
allowed_file()              # File type validation
validate_file_size()        # Size validation
clean_text()                # Text normalization
extract_email()             # Email extraction
extract_phone()             # Phone extraction
extract_urls()              # URL extraction
calculate_keyword_density() # Keyword analysis
generate_suggestions()      # AI suggestions
```

---

### 4. Data Layer

#### File Storage
- **Location:** `backend/uploads/`
- **Files:** Temporarily stored uploaded resumes
- **Naming:** UUID + original filename
- **Cleanup:** Can be configured (currently preserved)

#### ML Libraries
- **scikit-learn:** TF-IDF vectorization, cosine similarity
- **Text Processing:** Regular expressions for pattern matching

---

## Data Flow

### Resume Analysis Flow

```
User uploads resume + job description
        ↓
Frontend validates file (type, size)
        ↓
POST /api/v1/analyze
        ↓
Backend validates request
        ↓
Save file to uploads/
        ↓
extract_text_from_file()
        ↓
Parse resume text (PyPDF2/python-docx)
        ↓
extract_resume_metadata()
        ↓
extract_skills(resume_text)
        ↓
┌───────────────────────┐
│ If Job Description:   │
│   extract_skills(jd)  │
│   calculate_ats_score │
│   - TF-IDF similarity │
│   - Skill matching    │
│   - Format analysis   │
│   - Suggestions       │
└───────────────────────┘
        ↓
Format JSON response
        ↓
Return to frontend
        ↓
Display results with animations
        ↓
User reviews and improves resume
```

---

## Algorithm Details

### TF-IDF Similarity

**Purpose:** Measure semantic similarity between resume and job description

**Process:**
1. Tokenize both documents
2. Remove stop words
3. Calculate term frequency (TF)
4. Calculate inverse document frequency (IDF)
5. Generate TF-IDF vectors
6. Calculate cosine similarity

**Formula:**
```
TF-IDF(t,d) = TF(t,d) × IDF(t)

where:
  TF(t,d) = frequency of term t in document d
  IDF(t) = log(N / df(t))
  N = total documents
  df(t) = documents containing term t

Cosine Similarity = (A · B) / (||A|| × ||B||)
```

---

### Skill Extraction

**Approach:** Pattern matching with word boundaries

```python
# For each skill in database
pattern = r'\b' + skill.lower() + r'\b'

# Search in normalized text
if re.search(pattern, cleaned_text):
    skills.append(skill)
```

**Advantages:**
- Fast execution
- No ML training required
- Easily customizable
- Language-agnostic

**Limitations:**
- Requires predefined skill list
- May miss variations (e.g., "React.js" vs "ReactJS")

**Future Improvement:**
- Use NLP entity recognition (spaCy)
- Implement fuzzy matching
- Add skill synonyms

---

### Format Analysis

**Criteria Evaluated:**

1. **Word Count** (300-1000 optimal)
2. **Section Presence** (Experience, Education, Skills, Projects)
3. **Bullet Points** (Improves readability)
4. **Action Verbs** (developed, implemented, led, etc.)

**Scoring:**
- Each criterion: 0-25 points
- Total: 0-100 points

---

## Security Considerations

### Current Implementation

✅ **File Type Validation**
- Whitelist: PDF, DOCX, TXT only
- Extension checking

✅ **File Size Limits**
- Max 5MB to prevent DoS

✅ **Input Sanitization**
- Text cleaning and normalization

✅ **Error Handling**
- No sensitive info in error messages

### Future Enhancements

🔒 **Authentication**
- JWT tokens
- User sessions

🔒 **Rate Limiting**
- Prevent API abuse
- Per-IP request limits

🔒 **File Scanning**
- Malware detection
- Content validation

🔒 **HTTPS**
- Encrypted communication

---

## Performance Considerations

### Current Performance

**Metrics:**
- Average response time: 2-5 seconds
- File processing: ~1-2 seconds
- Analysis: ~1-2 seconds
- Network: ~1 second

**Bottlenecks:**
- PDF text extraction (largest files)
- TF-IDF vectorization (large texts)

### Optimization Strategies

1. **Caching**
   - Cache skill extraction results
   - Store frequently used TF-IDF vectors

2. **Asynchronous Processing**
   - Background job queue (Celery)
   - Websocket updates

3. **Database**
   - Store analysis history
   - Reduce reprocessing

4. **Code Optimization**
   - Profile with cProfile
   - Optimize regex patterns
   - Use compiled patterns

---

## Scalability

### Current Limitations

- Single-threaded Flask development server
- File system storage (not scalable)
- No load balancing
- No caching layer

### Scaling Strategy

**Horizontal Scaling:**
```
Load Balancer (Nginx)
        ↓
┌───────┴───────┐
│               │
Flask App 1   Flask App 2  (Multiple instances)
│               │
└───────┬───────┘
        ↓
Shared Storage (S3/MinIO)
        ↓
Database (PostgreSQL)
```

**Components:**
- **Load Balancer:** Nginx/HAProxy
- **Application Servers:** Gunicorn/uWSGI
- **File Storage:** S3/MinIO/NFS
- **Database:** PostgreSQL/MongoDB
- **Cache:** Redis/Memcached
- **Queue:** Celery + RabbitMQ

---

## Monitoring & Logging

### Current Logging

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Logs:**
- File uploads
- Analysis requests
- Errors and exceptions

### Production Monitoring

**Metrics to Track:**
- Request rate
- Response times
- Error rates
- File upload sizes
- Analysis success/failure rates

**Tools:**
- **Application:** New Relic, DataDog
- **Infrastructure:** Prometheus + Grafana
- **Logs:** ELK Stack (Elasticsearch, Logstash, Kibana)

---

## Testing Strategy

### Current Tests

**Unit Tests:**
- `test_matcher.py` - Skill extraction, scoring
- `test_utils.py` - Utility functions

**Coverage:**
- Core business logic: ~80%
- API endpoints: Not yet covered

### Future Testing

**Integration Tests:**
- API endpoint testing
- End-to-end workflows

**Performance Tests:**
- Load testing with Locust
- Stress testing

**Security Tests:**
- Penetration testing
- Vulnerability scanning

---

## Deployment

### Development

```bash
cd backend
python app.py
```

Runs on `http://localhost:5000` in debug mode.

### Production Recommendations

**Option 1: Traditional Server**
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Option 2: Docker**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

**Option 3: Cloud Platforms**
- **Heroku:** `git push heroku main`
- **AWS:** Elastic Beanstalk, Lambda
- **Google Cloud:** App Engine, Cloud Run
- **Azure:** App Service

---

## Future Architecture

### Microservices Approach

```
API Gateway
    ↓
┌───────────────────────────────┐
│                               │
Resume Service    Analysis Service
│                               │
Upload & Parse    Skill Matching
Metadata          ATS Scoring
│                               │
└────────┬──────────────────────┘
         ↓
  Shared Database
  (PostgreSQL)
```

**Benefits:**
- Independent scaling
- Technology flexibility
- Better fault isolation
- Easier maintenance

---

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | HTML/CSS/JS | User interface |
| API | Flask 3.0 | REST API |
| ML/NLP | scikit-learn | TF-IDF, similarity |
| File Processing | PyPDF2, python-docx | Text extraction |
| CORS | Flask-CORS | Cross-origin support |
| Testing | unittest | Unit tests |

---

## Conclusion

The current architecture is well-suited for:
- ✅ Development and learning
- ✅ Small to medium user base
- ✅ Demonstration and portfolio

For production at scale, consider:
- 🔄 Database integration
- 🔄 Caching layer
- 🔄 Async processing
- 🔄 Load balancing
- 🔄 Containerization

---

**Document Version:** 1.0  
**Last Updated:** January 2024  
**Maintained By:** Project Team

