# 🚀 Quick Start Guide

Get the AI-Powered Resume Analyzer up and running in 5 minutes!

---

## ⚡ Quick Setup (5 Minutes)

### 1. Download & Install

```bash
# Clone the repository
git clone https://github.com/yourusername/AI-powered-Resume-Analyzer.git
cd AI-powered-Resume-Analyzer

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 2. Start the Server

```bash
cd backend
python app.py
```

You should see:
```
* Running on http://0.0.0.0:5000
* Debug mode: on
```

### 3. Open the Frontend

Open `frontend/index.html` in your web browser, or:

```bash
cd frontend
python -m http.server 8080
```

Then navigate to `http://localhost:8080`

---

## 🎯 First Analysis

1. **Upload a Resume**
   - Click "Choose file" or drag & drop
   - Supported: PDF, DOCX, TXT (max 5MB)

2. **Add Job Description** (Optional)
   - Paste job posting text
   - Get ATS score and skill matching

3. **Click "Analyze Resume"**
   - Wait 2-5 seconds
   - View your results!

---

## 📊 Understanding Your Results

### ATS Score
- **80-100:** Excellent - Great match!
- **70-79:** Good - Minor improvements needed
- **60-69:** Fair - Add missing skills
- **0-59:** Needs Improvement - Major gaps

### Score Breakdown
- **Skills Match (40%)** - How many required skills you have
- **Keyword Density (30%)** - Presence of job keywords
- **Content Similarity (20%)** - Overall text alignment
- **Format Quality (10%)** - Resume structure

### What to Do Next
1. Review missing skills
2. Add relevant skills to your resume
3. Follow the suggestions provided
4. Re-analyze and compare scores

---

## 🛠️ Troubleshooting

### Backend Won't Start

**Problem:** `ModuleNotFoundError: No module named 'flask'`
```bash
# Solution: Install dependencies
pip install -r backend/requirements.txt
```

**Problem:** `Port 5000 is already in use`
```bash
# Solution: Change port in backend/app.py
app.run(debug=DEBUG, host='0.0.0.0', port=5001)  # Use 5001 instead

# Or kill process using port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

### Frontend Can't Connect to API

**Problem:** `Could not connect to the backend API`

**Solution:** 
1. Make sure backend is running on `http://localhost:5000`
2. Check `frontend/script.js` - ensure API_URL is correct
3. Check browser console for CORS errors

### File Upload Fails

**Problem:** `File too large` or `Invalid file type`

**Solution:**
- File must be under 5MB
- Only PDF, DOCX, or TXT formats
- Try compressing your PDF or saving as TXT

### Analysis Takes Too Long

**Possible Causes:**
- Large file size (try smaller file)
- Slow internet connection
- Server overload

**Solutions:**
- Refresh page and try again
- Clear browser cache
- Restart backend server

---

## 💡 Pro Tips

### Get Better Scores
1. ✅ **Match job keywords** - Use exact phrases from job description
2. ✅ **List all relevant skills** - Don't be modest!
3. ✅ **Use action verbs** - "Developed", "Led", "Implemented"
4. ✅ **Add metrics** - "Improved performance by 30%"
5. ✅ **Keep it concise** - 1-2 pages ideal

### Testing the API
```bash
# Test with cURL
curl -X POST http://localhost:5000/api/v1/analyze \
  -F "resume=@path/to/resume.pdf"

# Check API health
curl http://localhost:5000/api/v1/health
```

### Using API Programmatically

See `docs/API.md` for full documentation and code examples in:
- JavaScript/TypeScript
- Python
- cURL

---

## 📚 Next Steps

- [ ] Read full [README.md](../README.md)
- [ ] Check [API Documentation](API.md)
- [ ] Explore the code in `backend/`
- [ ] Try different resumes and job descriptions
- [ ] Customize skill categories in `backend/config.py`
- [ ] Add your own improvements!

---

## 🆘 Getting Help

- **Documentation:** Check README.md and docs/
- **Issues:** Create issue on GitHub
- **Email:** your.email@example.com

---

## 🎓 Learning Resources

Want to understand how it works?

1. **NLP Basics**
   - TF-IDF: [Understanding TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
   - Cosine Similarity: [Text Similarity](https://en.wikipedia.org/wiki/Cosine_similarity)

2. **Flask Framework**
   - [Flask Documentation](https://flask.palletsprojects.com/)
   - [Flask REST API Tutorial](https://flask-restful.readthedocs.io/)

3. **Frontend Development**
   - [Modern JavaScript](https://javascript.info/)
   - [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)

---

**Happy analyzing! 🚀**

Remember: This tool is meant to help optimize your resume, not replace your unique experiences and skills. Use it as a guide to improve your application materials!

