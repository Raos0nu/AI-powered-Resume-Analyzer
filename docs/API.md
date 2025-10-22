# 📡 API Documentation

## Overview

The Resume Analyzer API provides RESTful endpoints for analyzing resumes, extracting skills, and calculating ATS compatibility scores.

**Base URL:** `http://localhost:5000/api/v1`

**API Version:** v1

---

## Authentication

Currently, the API does not require authentication. This may change in future versions.

---

## Endpoints

### 1. Root Endpoint

Get API information and available endpoints.

**Request:**
```http
GET /
```

**Response:**
```json
{
  "name": "AI-Powered Resume Analyzer API",
  "version": "1.0.0",
  "description": "Analyze resumes and match against job descriptions with AI-powered insights",
  "endpoints": {
    "POST /api/v1/analyze": "Analyze resume and match with job description",
    "POST /api/v1/extract-skills": "Extract skills from text",
    "GET /api/v1/health": "Health check endpoint"
  },
  "status": "active"
}
```

---

### 2. Health Check

Check if the API service is running properly.

**Request:**
```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000000",
  "service": "Resume Analyzer API"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

### 3. Analyze Resume

Analyze a resume file and optionally match it against a job description to get ATS score and recommendations.

**Request:**
```http
POST /api/v1/analyze
Content-Type: multipart/form-data

resume: [binary file data]
job_description: "Looking for a Python developer with Flask experience..." (optional)
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/v1/analyze \
  -F "resume=@resume.pdf" \
  -F "job_description=We are looking for a Python developer..."
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `resume` | File | Yes | Resume file (PDF, DOCX, or TXT). Max 5MB |
| `job_description` | String | No | Job description text to match against |

**Response (Without Job Description):**
```json
{
  "success": true,
  "resume_info": {
    "filename": "John_Doe_Resume.pdf",
    "word_count": 450,
    "emails": ["john.doe@email.com"],
    "phones": ["(123) 456-7890"],
    "urls": {
      "linkedin": ["https://linkedin.com/in/johndoe"],
      "github": ["https://github.com/johndoe"],
      "portfolio": [],
      "other": []
    }
  },
  "skills": {
    "all_skills": [
      "python",
      "javascript",
      "react",
      "flask",
      "postgresql",
      "docker",
      "git"
    ],
    "categorized_skills": {
      "programming_languages": ["python", "javascript"],
      "web_technologies": ["react", "flask"],
      "databases": ["postgresql"],
      "cloud_devops": ["docker", "git"]
    },
    "total_count": 7
  },
  "resume_preview": "John Doe\nSoftware Engineer\n\nExperience:\n- Developed web applications using Python and Flask..."
}
```

**Response (With Job Description):**
```json
{
  "success": true,
  "resume_info": { /* same as above */ },
  "skills": { /* same as above */ },
  "resume_preview": "...",
  "ats_analysis": {
    "overall_score": 82.5,
    "rating": "Good",
    "breakdown": {
      "skill_match": 85.0,
      "content_similarity": 72.5,
      "format_quality": 90.0,
      "keyword_density": 78.0
    },
    "skills_match": {
      "jd_skills": [
        "python",
        "flask",
        "react",
        "postgresql",
        "docker",
        "kubernetes"
      ],
      "matching_skills": [
        "python",
        "flask",
        "react",
        "postgresql",
        "docker"
      ],
      "missing_skills": [
        "kubernetes"
      ],
      "match_percentage": 83.33
    },
    "format_analysis": {
      "score": 90,
      "issues": [],
      "strengths": [
        "Good resume length",
        "Well-structured with clear sections",
        "Uses bullet points for readability",
        "Uses strong action verbs"
      ]
    },
    "suggestions": [
      "Add these critical skills: kubernetes",
      "Good start! Add more relevant keywords from the job description to improve your score.",
      "Ensure your resume includes quantifiable achievements (e.g., 'improved performance by 30%').",
      "Use action verbs like 'developed', 'implemented', 'optimized', 'led', etc.",
      "Keep your resume to 1-2 pages for better readability."
    ]
  }
}
```

**Status Codes:**
- `200 OK` - Analysis successful
- `400 Bad Request` - Invalid input (no file, wrong format, etc.)
- `413 Payload Too Large` - File exceeds 5MB
- `500 Internal Server Error` - Server error during processing

**Error Response Example:**
```json
{
  "error": "Invalid file type",
  "message": "Supported formats: PDF, DOCX, TXT"
}
```

---

### 4. Extract Skills

Extract technical skills from any text input.

**Request:**
```http
POST /api/v1/extract-skills
Content-Type: application/json

{
  "text": "Experienced Python developer with Flask and Django expertise",
  "categorize": true
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/v1/extract-skills \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Python, JavaScript, React, Docker, AWS",
    "categorize": true
  }'
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | String | Yes | Text to extract skills from |
| `categorize` | Boolean | No | Whether to categorize skills by type (default: false) |

**Response (categorize=false):**
```json
{
  "success": true,
  "skills": [
    "python",
    "flask",
    "django"
  ],
  "count": 3
}
```

**Response (categorize=true):**
```json
{
  "success": true,
  "skills": {
    "programming_languages": ["python"],
    "web_technologies": ["flask", "django"]
  },
  "count": 3
}
```

**Status Codes:**
- `200 OK` - Extraction successful
- `400 Bad Request` - No text provided
- `500 Internal Server Error` - Server error

---

## Data Models

### Resume Info Object

```typescript
{
  filename: string,
  word_count: number,
  emails: string[],
  phones: string[],
  urls: {
    linkedin: string[],
    github: string[],
    portfolio: string[],
    other: string[]
  }
}
```

### Skills Object

```typescript
{
  all_skills: string[],
  categorized_skills: {
    [category: string]: string[]
  },
  total_count: number
}
```

### ATS Analysis Object

```typescript
{
  overall_score: number,        // 0-100
  rating: string,               // "Excellent" | "Good" | "Fair" | "Needs Improvement"
  breakdown: {
    skill_match: number,        // 0-100
    content_similarity: number, // 0-100
    format_quality: number,     // 0-100
    keyword_density: number     // 0-100
  },
  skills_match: {
    jd_skills: string[],
    matching_skills: string[],
    missing_skills: string[],
    match_percentage: number
  },
  format_analysis: {
    score: number,
    issues: string[],
    strengths: string[]
  },
  suggestions: string[]
}
```

---

## Skill Categories

The API recognizes skills in the following categories:

### Programming Languages
`python`, `java`, `javascript`, `typescript`, `c++`, `c#`, `c`, `go`, `rust`, `ruby`, `php`, `swift`, `kotlin`, `scala`, `r`, `matlab`

### Web Technologies
`react`, `angular`, `vue`, `node.js`, `express`, `django`, `flask`, `fastapi`, `html`, `css`, `scss`, `sass`, `tailwind`, `bootstrap`, `jquery`, `webpack`, `redux`, `next.js`, `nuxt.js`

### Databases
`sql`, `mysql`, `postgresql`, `mongodb`, `redis`, `cassandra`, `dynamodb`, `oracle`, `sqlite`, `mariadb`, `elasticsearch`

### Cloud & DevOps
`aws`, `azure`, `gcp`, `docker`, `kubernetes`, `jenkins`, `terraform`, `ansible`, `ci/cd`, `github actions`, `gitlab ci`, `circleci`, `linux`, `unix`, `shell scripting`, `bash`

### Data Science & AI
`tensorflow`, `pytorch`, `keras`, `scikit-learn`, `pandas`, `numpy`, `nlp`, `spacy`, `nltk`, `machine learning`, `deep learning`, `computer vision`, `opencv`, `data analysis`, `data visualization`, `matplotlib`, `seaborn`, `plotly`, `tableau`, `power bi`

### Tools & Frameworks
`git`, `github`, `gitlab`, `bitbucket`, `jira`, `agile`, `scrum`, `rest api`, `graphql`, `microservices`, `testing`, `junit`, `pytest`, `selenium`, `postman`, `swagger`

### Security & Networking
`networking`, `cybersecurity`, `penetration testing`, `scapy`, `wireshark`, `nmap`, `oauth`, `jwt`, `ssl/tls`, `firewall`

---

## Rate Limiting

Currently, there are no rate limits. In production, consider implementing rate limiting to prevent abuse.

**Recommended limits for production:**
- 100 requests per hour per IP
- 1000 requests per day per IP

---

## CORS

Cross-Origin Resource Sharing (CORS) is enabled for all API routes with the following configuration:

- **Allowed Origins:** `*` (all origins)
- **Allowed Methods:** `GET`, `POST`, `OPTIONS`
- **Allowed Headers:** All

For production, restrict allowed origins to your frontend domain.

---

## Error Handling

All errors follow this consistent format:

```json
{
  "error": "Error Type",
  "message": "Human-readable error description"
}
```

### Common Errors

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 400 | Bad Request | Invalid input parameters |
| 413 | File Too Large | Uploaded file exceeds 5MB |
| 404 | Not Found | Endpoint does not exist |
| 500 | Internal Server Error | Unexpected server error |

---

## Best Practices

### 1. File Upload
- Always validate file size client-side before uploading
- Supported formats: PDF, DOCX, TXT
- Maximum file size: 5MB
- Use descriptive filenames

### 2. Job Description
- Provide complete job descriptions for better analysis
- Include required skills, qualifications, and responsibilities
- Minimum 100 characters recommended

### 3. Error Handling
- Always check response status codes
- Handle errors gracefully in your application
- Display user-friendly error messages

### 4. Performance
- Typical response time: 2-5 seconds
- Larger files may take longer to process
- Implement loading indicators in UI

---

## Code Examples

### JavaScript (Fetch API)

```javascript
// Analyze resume
async function analyzeResume(file, jobDescription) {
  const formData = new FormData();
  formData.append('resume', file);
  if (jobDescription) {
    formData.append('job_description', jobDescription);
  }

  try {
    const response = await fetch('http://localhost:5000/api/v1/analyze', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Analysis failed:', error);
    throw error;
  }
}

// Extract skills
async function extractSkills(text, categorize = false) {
  try {
    const response = await fetch('http://localhost:5000/api/v1/extract-skills', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text, categorize })
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Skill extraction failed:', error);
    throw error;
  }
}
```

### Python (requests)

```python
import requests

# Analyze resume
def analyze_resume(file_path, job_description=None):
    url = 'http://localhost:5000/api/v1/analyze'
    
    with open(file_path, 'rb') as f:
        files = {'resume': f}
        data = {}
        if job_description:
            data['job_description'] = job_description
        
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        return response.json()

# Extract skills
def extract_skills(text, categorize=False):
    url = 'http://localhost:5000/api/v1/extract-skills'
    payload = {
        'text': text,
        'categorize': categorize
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

# Usage
result = analyze_resume('resume.pdf', 'Looking for Python developer...')
print(f"ATS Score: {result['ats_analysis']['overall_score']}")
```

---

## Changelog

### Version 1.0.0 (Current)
- Initial API release
- Resume analysis endpoint
- Skill extraction endpoint
- ATS scoring algorithm
- Multi-format file support (PDF, DOCX, TXT)
- Health check endpoint

---

## Support

For issues, questions, or feature requests:
- GitHub Issues: [Project Issues](https://github.com/yourusername/AI-powered-Resume-Analyzer/issues)
- Email: your.email@example.com

---

**Last Updated:** January 2024

