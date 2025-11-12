# 🚀 Deployment Guide - Deploy to Vercel

This guide will help you deploy the Guess the Number game to Vercel so it's publicly accessible.

## Prerequisites

1. **GitHub Account** - Required for Vercel
2. **Vercel Account** - Sign up at vercel.com (free)
3. **Git** - For version control
4. **Code Repository** - Your code on GitHub

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

```bash
# Initialize git (if not already done)
cd "c:\Users\DR ESAN\Documents\ARCIUM GAME\guess-number-game"
git init
git add .
git commit -m "Initial commit: Arcium Game ready for deployment"

# Add remote (replace YOUR_USERNAME and YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/arcium-game.git
git push -u origin main
```

### Step 2: Deploy Frontend to Vercel

**Option A: Using Vercel CLI (Recommended)**

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy frontend
cd web/frontend
vercel

# Follow prompts:
# - Link to existing project? No (create new)
# - Project name: arcium-game-frontend
# - Framework: React
# - Build command: npm run build
# - Output directory: build
```

**Option B: Using GitHub Integration**

1. Go to https://vercel.com/new
2. Click "Import Git Repository"
3. Select your repository
4. Configure:
   - Project name: `arcium-game-frontend`
   - Root directory: `web/frontend`
   - Framework: React
   - Build command: `npm run build`
   - Output directory: `build`
5. Click "Deploy"

**Result**: Your frontend will be deployed to:
```
https://arcium-game-frontend.vercel.app
```

### Step 3: Deploy Backend API to Vercel

**Deploy the Python API**

```bash
# Navigate to API folder
cd web/api

# Deploy with Vercel CLI
vercel

# Follow prompts:
# - Link to existing project? No (create new)
# - Project name: arcium-game-api
# - Framework: Other
```

**Result**: Your API will be deployed to:
```
https://arcium-game-api.vercel.app
```

### Step 4: Connect Frontend to Backend

Update your frontend environment variables:

```bash
# In web/frontend/.env.production
REACT_APP_API_URL=https://arcium-game-api.vercel.app

# In web/frontend/.env.development
REACT_APP_API_URL=http://localhost:5000
```

Redeploy frontend:
```bash
cd web/frontend
vercel --prod
```

### Step 5: Verify Deployment

Test your live game:
1. Visit: `https://arcium-game-frontend.vercel.app`
2. Try all game modes
3. Check console for errors (F12)

---

## 🎯 Full Deployment Flow

### For GitHub → Vercel (Recommended)

```
Your Local Code
    ↓
    git push
    ↓
GitHub Repository
    ↓
Vercel Auto-Detects Changes
    ↓
Vercel Rebuilds & Deploys
    ↓
Your Live Game! 🎉
```

### Step-by-Step Commands

```bash
# 1. Setup Git
git init
git add .
git commit -m "Ready to deploy"

# 2. Add to GitHub
git remote add origin https://github.com/YOUR_USERNAME/arcium-game.git
git push -u origin main

# 3. Deploy Frontend
cd web/frontend
vercel

# 4. Deploy Backend
cd ../api
vercel

# 5. Update Environment Variables in Vercel Dashboard
# (See next section)

# 6. Test
Visit your frontend URL
```

---

## 🔧 Environment Variables Setup

### Frontend (.env files)

Create `web/frontend/.env`:
```
REACT_APP_API_URL=http://localhost:5000
```

Create `web/frontend/.env.production`:
```
REACT_APP_API_URL=https://arcium-game-api.vercel.app
```

### In Vercel Dashboard

1. Go to your frontend project
2. Settings → Environment Variables
3. Add:
   ```
   REACT_APP_API_URL = https://arcium-game-api.vercel.app
   ```
4. Redeploy

---

## 📊 Architecture After Deployment

```
Your Users
    ↓
Frontend (Vercel)
    https://arcium-game-frontend.vercel.app
    ↓
    API Calls
    ↓
Backend API (Vercel)
    https://arcium-game-api.vercel.app
    ↓
Game Logic & Encryption
```

---

## 🐛 Troubleshooting

### Issue: "Failed to connect to API"

**Solution**: 
1. Check `REACT_APP_API_URL` environment variable
2. Verify backend is deployed
3. Check CORS settings in Flask (already configured)

### Issue: "Build failed"

**Solution**:
1. Check `npm install` runs successfully locally
2. Verify `package.json` exists in frontend folder
3. Check Node version compatibility (16+)

### Issue: "Page shows 404"

**Solution**:
1. Verify correct Vercel URL
2. Check deployment status in Vercel dashboard
3. Try redeploying with `vercel --prod`

### Issue: "Python dependencies not installing"

**Solution**:
1. Ensure `requirements.txt` is in correct directory
2. Add `vercel.json` to backend folder
3. Use Python 3.9+ compatible packages

---

## 🚀 Custom Domain (Optional)

### Add Custom Domain

1. In Vercel Dashboard → Project Settings
2. Domains → Add Domain
3. Follow DNS configuration
4. Wait 24 hours for propagation

Example: `https://guessthe-number.your-domain.com`

---

## 🔐 Security & Production

### Recommended Production Setup

1. **Use Environment Secrets** in Vercel
   - Settings → Environment Variables
   - Mark as "Sensitive" for API keys

2. **Enable HTTPS** (automatic with Vercel)

3. **Rate Limiting** (consider adding for production)

4. **Database** (upgrade from memory storage)

### Upgrade from Memory Storage

Current implementation stores games in memory. For production:

```python
# Consider using:
# - Redis (caching)
# - MongoDB (persistent storage)
# - PostgreSQL (relational data)

# Update game_api.py to use database instead of dict
```

---

## 📈 Monitoring & Analytics

### In Vercel Dashboard

1. **Analytics** → View traffic, performance
2. **Deployments** → See deployment history
3. **Logs** → Debug issues
4. **Monitoring** → Performance metrics

---

## 🎉 Success Checklist

- [ ] GitHub repository created
- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Vercel
- [ ] Environment variables configured
- [ ] Frontend connected to backend
- [ ] Game working on live URL
- [ ] All modes tested
- [ ] Custom domain (optional)
- [ ] Monitoring set up
- [ ] Shared with team/users

---

## 📝 After Deployment

### Share Your Game

**Frontend URL**:
```
https://arcium-game-frontend.vercel.app
```

**Share on social media/email**:
```
🎮 Learn about Arcium privacy with our game!
Play: [your-frontend-url]

Commit, Guess, and Reveal - understand 
cryptography through gameplay 🔐
```

### Keep It Updated

```bash
# Make changes locally
git add .
git commit -m "Your changes"
git push

# Vercel automatically redeploys!
```

---

## 🎓 Full Public Access

Your game is now:
- ✅ Publicly accessible on internet
- ✅ Always running (Vercel infrastructure)
- ✅ Auto-scaling (handles traffic)
- ✅ Secure (HTTPS by default)
- ✅ Free tier available
- ✅ Share-able link

**Your Live Game**: Visit your Vercel frontend URL! 🚀

---

## Next Steps

1. **Monitor** your deployment in Vercel dashboard
2. **Share** the link with others
3. **Gather feedback** on the game
4. **Plan improvements** based on usage
5. **Consider upgrading** to paid plan if needed

---

Need more help? Check:
- https://vercel.com/docs
- https://create-react-app.dev/docs/deployment/
- Flask documentation

Happy deploying! 🎉
