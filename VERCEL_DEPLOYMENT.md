# 🚀 Vercel Deployment Guide

## ✅ Your Code is Now Vercel-Ready!

I've configured your project to work with Vercel's serverless architecture.

---

## 📋 What Was Changed

✅ **api/index.py** - Serverless function entry point
✅ **vercel.json** - Vercel configuration  
✅ **requirements.txt** - Root-level dependencies for Vercel
✅ **frontend/script.js** - Auto-detects API URL (localhost vs production)
✅ **.vercelignore** - Excludes unnecessary files

---

## 🚀 Deploy to Vercel - Step by Step

### **Method 1: Web Interface (Easiest)** ⭐

#### **Step 1: Go to Vercel**
- Visit: https://vercel.com
- Click "Sign Up" or "Log In"
- Choose "Continue with GitHub"

#### **Step 2: Import Repository**
- Click "Add New..." → "Project"
- Find `Raos0nu/AI-powered-Resume-Analyzer`
- Click "Import"

#### **Step 3: Configure Project**
```
Framework Preset: Other
Root Directory: ./
Build Command: (leave empty)
Output Directory: (leave empty)
Install Command: pip install -r requirements.txt
```

#### **Step 4: Environment Variables (Optional)**
Click "Environment Variables" and add:
```
SECRET_KEY = your-secret-key-here
DEBUG = False
```

#### **Step 5: Deploy!**
- Click "Deploy"
- Wait 2-5 minutes for build
- Your app will be live!

#### **Step 6: Get Your URL**
After deployment, you'll get a URL like:
```
https://ai-powered-resume-analyzer.vercel.app
```

---

### **Method 2: Vercel CLI** 🖥️

#### **Install Vercel CLI**
```bash
npm install -g vercel
```

#### **Login to Vercel**
```bash
vercel login
```

#### **Deploy**
```bash
# From project root
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? ai-powered-resume-analyzer
# - Directory? ./ (press Enter)
# - Override settings? No

# For production deployment:
vercel --prod
```

---

## ⚠️ **Important Vercel Limitations**

### **File Upload Limits:**
- ⚠️ **Max request body: 4.5MB** (Hobby plan)
- ⚠️ **Max: 100MB** (Pro plan)
- Your app allows 5MB uploads - works on Hobby plan!

### **Function Timeout:**
- ⚠️ **10 seconds** (Hobby plan)
- ⚠️ **60 seconds** (Pro plan)
- Resume analysis should complete within 5-10 seconds

### **Cold Starts:**
- ⚠️ First request after inactivity may be slow (3-5 seconds)
- Subsequent requests are fast

---

## 🔧 **After First Deployment**

### **1. Test Your App**
Visit your Vercel URL and test:
- ✅ Upload a resume (PDF/DOCX/TXT)
- ✅ Add job description
- ✅ Check ATS scoring
- ✅ Verify skills extraction

### **2. Check the Logs**
If something doesn't work:
- Go to Vercel Dashboard
- Click your project
- Go to "Deployments" → Click latest deployment
- Click "View Function Logs"
- Look for errors

### **3. Add Custom Domain (Optional)**
- Go to Project Settings → Domains
- Add your domain (e.g., resume-analyzer.yourdomain.com)
- Update DNS records as instructed

---

## 🐛 **Troubleshooting Common Issues**

### **Issue: 404 NOT_FOUND**
**Cause:** Vercel can't find the Flask app

**Solution:**
✅ **Already fixed!** The new configuration should work.

**If still happening:**
1. Check `api/index.py` exists
2. Verify `vercel.json` is correct
3. Redeploy: `vercel --prod --force`

---

### **Issue: Import Errors**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
1. Check `requirements.txt` exists in root
2. Verify all dependencies are listed
3. Redeploy

---

### **Issue: File Upload Fails**
```
413 Payload Too Large
```

**Solution:**
- File is > 4.5MB on Hobby plan
- Compress PDF or save as TXT
- Or upgrade to Vercel Pro ($20/month)

---

### **Issue: Function Timeout**
```
504 Gateway Timeout
```

**Solution:**
- Large file or complex job description
- Try smaller files
- Or upgrade to Vercel Pro (60s timeout)

---

### **Issue: CORS Errors**
```
Access-Control-Allow-Origin missing
```

**Solution:**
Already configured with Flask-CORS. If still happening:
1. Check browser console
2. Verify API URL in `frontend/script.js`
3. Check backend logs

---

## 🎯 **Deployment Checklist**

After successful deployment:

- [ ] Test with sample resume
- [ ] Test with job description  
- [ ] Verify ATS scoring works
- [ ] Test on mobile device
- [ ] Check performance (speed)
- [ ] Monitor function logs
- [ ] Update GitHub repo with Vercel URL
- [ ] Add deployment badge to README
- [ ] Share on LinkedIn/Portfolio

---

## 📊 **Monitoring Your App**

### **Vercel Dashboard**
Monitor:
- Request count
- Function execution time
- Error rate
- Bandwidth usage

### **Free Tier Limits:**
- ✅ 100GB bandwidth/month
- ✅ 100GB-hours serverless function execution
- ✅ Unlimited deployments

---

## 🔄 **Updating Your App**

Every time you push to GitHub:
```bash
git add .
git commit -m "your changes"
git push origin main
```

Vercel automatically:
1. Detects the push
2. Builds your app
3. Deploys to production
4. Updates your URL

**No manual redeployment needed!** 🎉

---

## 💡 **Pro Tips**

### **1. Preview Deployments**
Every pull request gets a preview URL:
- Great for testing before merging
- Automatic preview for each branch

### **2. Environment Variables**
Set different values for production vs preview:
- Development: `DEBUG=True`
- Production: `DEBUG=False`

### **3. Analytics**
Enable Vercel Analytics:
- Dashboard → Analytics → Enable
- Track page views, performance
- Free on Hobby plan!

### **4. Custom Domain**
Make it professional:
- `resume-analyzer.yourdomain.com`
- Free SSL certificate included
- Automatic HTTPS

---

## 🚨 **If Deployment Fails**

### **Check Build Logs:**
1. Go to Vercel Dashboard
2. Click failed deployment
3. Read "Build Logs" tab
4. Look for error messages

### **Common Build Errors:**

**Error: "Could not install requirements"**
- Check `requirements.txt` syntax
- Verify package versions exist

**Error: "No app detected"**
- Check `api/index.py` exists
- Verify imports are correct

**Error: "Module not found"**
- Missing dependency in `requirements.txt`
- Add it and redeploy

---

## 📱 **Alternative: Deploy Frontend Only on Vercel**

If serverless limitations are too restrictive:

### **Option A: Frontend on Vercel + Backend on Render**

**Backend (Render):**
1. Deploy backend to Render (see DEPLOYMENT.md)
2. Get Render URL: `https://resume-analyzer.onrender.com`

**Frontend (Vercel):**
1. Update `frontend/script.js`:
```javascript
const API_URL = 'https://your-render-app.onrender.com/api/v1';
```
2. Deploy only frontend to Vercel
3. Frontend: Fast (Vercel CDN)
4. Backend: Reliable (Render)

**Best of both worlds!** ⚡

---

## ✨ **Success!**

Once deployed successfully:

Your app is at: `https://your-project.vercel.app`

**Share it:**
- [ ] Add to GitHub README
- [ ] Update LinkedIn
- [ ] Add to resume
- [ ] Share with friends!

---

## 🆘 **Need Help?**

- **Vercel Docs:** https://vercel.com/docs
- **Vercel Support:** https://vercel.com/support
- **Project Issues:** Check `api/index.py` and `vercel.json`

---

## 🎉 **You're Live!**

Your Resume Analyzer is now deployed on Vercel! 🚀

**Test it:** Upload a resume and see the magic happen!

**Pro Tip:** Share your Vercel URL on LinkedIn with a post about building an AI-powered project. Recruiters love seeing deployed projects! 💼

