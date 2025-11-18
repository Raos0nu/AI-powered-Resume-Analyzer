# 🚀 Deployment Guide

## Overview

This guide covers deploying the AI-Powered Resume Analyzer to various platforms.

---

## ⭐ **Recommended: Render (FREE)** - Best for Flask Apps

Render is perfect for Flask apps with file uploads and provides:
- ✅ Free tier (750 hours/month)
- ✅ Auto-deploy from GitHub
- ✅ File upload support
- ✅ Easy setup
- ✅ HTTPS included

### **Deploy to Render - Step by Step**

#### **1. Push Latest Code**
```bash
git add .
git commit -m "add deployment config"
git push origin main
```

#### **2. Go to Render**
- Visit: https://render.com
- Sign up / Log in with GitHub

#### **3. Create New Web Service**
- Click "New +" → "Web Service"
- Connect your GitHub repo: `Raos0nu/AI-powered-Resume-Analyzer`
- Click "Connect"

#### **4. Configure Service**
```
Name: resume-analyzer
Region: Choose closest to you
Branch: main
Root Directory: (leave empty)
Runtime: Python 3
Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

#### **5. Environment Variables**
Click "Advanced" → Add Environment Variable:
```
SECRET_KEY = (click "Generate")
DEBUG = False
```

#### **6. Deploy!**
- Click "Create Web Service"
- Wait 5-10 minutes for first build
- Your app will be live at: `https://resume-analyzer-xxxx.onrender.com`

#### **7. Update Frontend**
Once deployed, update `frontend/script.js`:
```javascript
// Change this line:
const API_URL = 'http://localhost:5000/api/v1';

// To your Render URL:
const API_URL = 'https://resume-analyzer-xxxx.onrender.com/api/v1';
```

Then commit and push again.

---

## 🟦 **Alternative: Railway** - Also Great for Flask

Railway is similar to Render and very easy to use.

### **Deploy to Railway**

#### **1. Go to Railway**
- Visit: https://railway.app
- Sign up with GitHub

#### **2. New Project**
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose `Raos0nu/AI-powered-Resume-Analyzer`

#### **3. Configuration**
Railway auto-detects Python. Just add:
```bash
Start Command: cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

#### **4. Environment Variables**
```
SECRET_KEY = your-secret-key
DEBUG = False
```

#### **5. Deploy**
- Click "Deploy"
- Get your URL: `https://xxxx.railway.app`
- Update frontend API_URL

---

## 🟣 **Vercel (Frontend Only) + Render (Backend)**

**Best approach for Vercel:** Host frontend on Vercel, backend on Render.

### **Step 1: Deploy Backend on Render**
Follow Render instructions above.

### **Step 2: Deploy Frontend on Vercel**

#### **Create vercel.json**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

#### **Update Frontend API URL**
In `frontend/script.js`:
```javascript
const API_URL = 'https://your-render-app.onrender.com/api/v1';
```

#### **Deploy to Vercel**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? resume-analyzer-frontend
# - Directory? ./
# - Override settings? No
```

Your frontend will be at: `https://resume-analyzer-frontend.vercel.app`

---

## 🟢 **Heroku (Classic Option)**

Heroku is reliable but requires credit card (even for free tier).

### **Deploy to Heroku**

#### **1. Create Procfile**
Create `Procfile` in root:
```
web: cd backend && gunicorn app:app
```

#### **2. Create runtime.txt**
Create `runtime.txt` in root:
```
python-3.11.9
```

#### **3. Deploy**
```bash
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create resume-analyzer-app

# Add buildpack
heroku buildpacks:set heroku/python

# Set env vars
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Open app
heroku open
```

---

## 🐍 **PythonAnywhere (Simple & Free)**

Good for beginners, but slower than other options.

### **Deploy to PythonAnywhere**

1. Sign up at: https://www.pythonanywhere.com
2. Go to "Web" tab → "Add a new web app"
3. Choose Flask
4. Upload your code via Files tab
5. Configure WSGI file:
```python
import sys
sys.path.append('/home/yourusername/resume-analyzer')
sys.path.append('/home/yourusername/resume-analyzer/backend')

from backend.app import app as application
```
6. Install requirements in Bash console:
```bash
pip install -r backend/requirements.txt
```
7. Reload web app

Your app: `https://yourusername.pythonanywhere.com`

---

## 📋 **Comparison Table**

| Platform | Free Tier | Setup | File Upload | Best For |
|----------|-----------|-------|-------------|----------|
| **Render** | ✅ 750hrs/mo | Easy | ✅ Yes | **Recommended** |
| **Railway** | ✅ $5 credit | Easy | ✅ Yes | Flask apps |
| **Vercel** | ✅ Unlimited | Medium | ❌ No* | Frontend only |
| **Heroku** | ✅ (needs card) | Medium | ✅ Yes | Production apps |
| **PythonAnywhere** | ✅ Limited | Easy | ⚠️ Limited | Beginners |

*Vercel serverless has 50MB limit and other restrictions

---

## 🎯 **Recommended Approach**

### **For Full-Stack (Best):**
```
Backend: Render (Free)
Frontend: Vercel (Free) - points to Render API
```

### **For Simplicity:**
```
Everything on Render (Free)
```

---

## 🔧 **Post-Deployment Checklist**

After deploying:

✅ Test file upload (PDF, DOCX)
✅ Test with job description
✅ Check ATS scoring works
✅ Verify skills extraction
✅ Test on mobile devices
✅ Add deployed URL to GitHub repo
✅ Add to README.md
✅ Share on LinkedIn/Portfolio

---

## 🐛 **Troubleshooting**

### **Backend Not Responding**
- Check logs on platform dashboard
- Verify environment variables set
- Check build command succeeded

### **Frontend Can't Connect**
- Update API_URL in `frontend/script.js`
- Check CORS settings in `backend/app.py`
- Verify backend is running

### **File Upload Fails**
- Check file size < 5MB
- Verify uploads folder exists
- Check platform storage limits

### **Build Fails**
- Check requirements.txt versions
- Verify Python version (3.11+)
- Check logs for specific errors

---

## 🌐 **Custom Domain (Optional)**

### **On Render:**
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS records (provided by Render)

### **On Vercel:**
1. Go to Settings → Domains
2. Add your domain
3. Update DNS (automatic with some providers)

---

## 📝 **After Deployment**

Update your README.md with live demo link:
```markdown
## 🌐 Live Demo

**Try it out:** [https://your-app.onrender.com](https://your-app.onrender.com)
```

Add to your GitHub repo:
1. Settings → Website → Add deployment URL
2. Pin to profile
3. Share on social media!

---

## 🎉 **You're Done!**

Your Resume Analyzer is now live and accessible worldwide! 🌍

**Share it:**
- Add to resume
- LinkedIn post
- Portfolio website
- Job applications

---

**Need help?** Check platform-specific documentation:
- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Vercel Docs](https://vercel.com/docs)
- [Heroku Docs](https://devcenter.heroku.com)

