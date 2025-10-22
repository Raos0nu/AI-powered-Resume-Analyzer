# 🚀 How to Run the AI-Powered Resume Analyzer

## ✅ Your Application is Now Running!

### What Just Happened:
1. ✅ Dependencies installed (Flask, scikit-learn, PyPDF2, etc.)
2. ✅ Backend server started in a separate window
3. ✅ Frontend opened in your browser

---

## 🌐 Access URLs

- **Frontend UI:** Open `frontend/index.html` in your browser
  - Or just look for the browser tab that already opened!
  
- **Backend API:** http://localhost:5000
  - Health check: http://localhost:5000/api/v1/health

---

## 📝 How to Use

### Step 1: Prepare Your Files
- Have a resume ready (PDF, DOCX, or TXT format)
- Optionally, copy a job description

### Step 2: Upload Resume
1. Go to the frontend page (should be open in your browser)
2. Click "Choose file" or drag and drop your resume
3. Paste job description (optional but recommended for ATS score)
4. Click "Analyze Resume"

### Step 3: View Results
- Wait 2-5 seconds for analysis
- See your ATS score (0-100)
- Review matching and missing skills
- Read personalized suggestions

---

## 🔍 What You Should See

### Backend Server Window:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
Press CTRL+C to quit
```

### Frontend (Browser):
A beautiful gradient interface with:
- File upload area
- Job description text box
- "Analyze Resume" button

---

## ⚠️ Troubleshooting

### Backend Not Running?

**Check the PowerShell window that opened:**
- Is there an error message?
- Is it showing "Running on http://localhost:5000"?

**If not visible, start manually:**
```powershell
cd backend
python app.py
```

### Frontend Not Opening?

**Open manually:**
1. Navigate to your project folder
2. Double-click `frontend/index.html`
3. Or right-click → Open with → Your browser

### "Could not connect to API" Error?

**Make sure backend is running:**
1. Check if the PowerShell window with the backend is still open
2. Try opening: http://localhost:5000/api/v1/health in your browser
3. You should see: `{"status": "healthy", ...}`

### Port 5000 Already in Use?

**Change the port:**
1. Open `backend/app.py`
2. Find the last line: `app.run(debug=DEBUG, host='0.0.0.0', port=5000)`
3. Change `port=5000` to `port=5001`
4. Update `frontend/script.js` line 2: `const API_URL = 'http://localhost:5001/api/v1';`

---

## 🛑 How to Stop

### Stop Backend:
- Go to the PowerShell window running the backend
- Press `Ctrl + C`
- Or close the window

### Stop Frontend:
- Just close the browser tab

---

## 🎯 Quick Test

### Test the API Manually:

**1. Check Health:**
```powershell
curl http://localhost:5000/api/v1/health
```

**2. Test with a Resume:**
```powershell
# In PowerShell
Invoke-WebRequest -Uri http://localhost:5000/api/v1/analyze `
  -Method POST `
  -Form @{
    resume = Get-Item "path\to\your\resume.pdf"
    job_description = "Looking for Python developer..."
  }
```

---

## 📋 What to Try

### Sample Job Description:
```
We are seeking a talented Software Engineer with expertise in:
- Python programming and Flask framework
- Frontend development with React and JavaScript
- Database management (PostgreSQL, MySQL)
- Cloud platforms (AWS, Docker, Kubernetes)
- Version control with Git
- Agile/Scrum methodologies

Required Skills:
- 2+ years of Python development
- Experience with REST APIs
- Strong problem-solving abilities
- Excellent communication skills
```

### What You'll Get:
- ✅ ATS Score (0-100)
- ✅ Rating (Excellent/Good/Fair/Needs Improvement)
- ✅ Skills breakdown (matching vs missing)
- ✅ Resume format analysis
- ✅ Personalized suggestions
- ✅ Extracted contact info

---

## 💡 Pro Tips

1. **Better Scores:**
   - Always provide a job description
   - Ensure resume has clear sections
   - List all relevant skills
   - Use action verbs

2. **Testing:**
   - Try different resumes
   - Compare scores with/without job descriptions
   - Test various file formats

3. **Development:**
   - Backend auto-reloads on code changes (debug mode)
   - Check console for errors
   - Use browser DevTools to debug frontend

---

## 🎓 Next Steps

1. ✅ Test with your own resume
2. ✅ Try different job descriptions
3. ✅ Improve your resume based on suggestions
4. ✅ Re-analyze and compare scores
5. ✅ Consider deploying to the cloud!

---

## 🆘 Need Help?

### Common Issues:

**Issue:** "ModuleNotFoundError"
**Solution:** Run `pip install -r backend/requirements.txt`

**Issue:** "Port already in use"
**Solution:** Change port in `backend/app.py` (see Troubleshooting above)

**Issue:** "File too large"
**Solution:** Compress your PDF or save as TXT

**Issue:** Frontend can't connect to backend
**Solution:** Ensure backend is running and check browser console

---

## 📚 Documentation

- Full README: [README.md](README.md)
- API Docs: [docs/API.md](docs/API.md)
- Quick Start: [docs/QUICKSTART.md](docs/QUICKSTART.md)
- Architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## ✨ Enjoy!

Your AI-Powered Resume Analyzer is ready to use!

**Happy analyzing!** 🎉

---

**Running into issues?** Check the PowerShell window for error messages or consult the documentation above.

