# GitHub Deployment Guide - Clinical AI System

## ⚠️ IMPORTANT: Install Git First

Before deploying to GitHub, you need to install Git on your system:

### Option 1: Download & Install Git
1. Go to https://git-scm.com/download/win
2. Download the Windows installer
3. Run the installer and follow the prompts
4. Restart PowerShell after installation

### Option 2: Use Windows Package Manager (If Available)
```powershell
winget install Git.Git
```

---

## 🚀 Once Git is Installed, Deploy to GitHub

Follow these steps in PowerShell:

### Step 1: Navigate to Project Directory
```powershell
cd "C:\Users\rajar\Desktop\EXPERIMENT\agent 2\last attempt\clinical_ai_multi_agent"
```

### Step 2: Create .gitignore (Protect Your API Keys!)
```powershell
# Create .gitignore file
@"
# Environment variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Pycache
.pytest_cache/
.mypy_cache/

# Logs
*.log
logs/
"@ | Out-File -FilePath .gitignore -Encoding UTF8 -Force

Write-Host "✅ .gitignore created" -ForegroundColor Green
```

### Step 3: Create .env.example (Template for Others)
```powershell
# Create .env.example file
@"
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4-turbo

# Google Configuration
GOOGLE_API_KEY=your-google-api-key-here
GOOGLE_MODEL_ID=gemini-pro

# Vertex AI Configuration
VERTEX_PROJECT_ID=your-gcp-project-id
VERTEX_LOCATION=us-central1
VERTEX_MODEL_ID=gemini-1.5-pro

# Qdrant Configuration
QDRANT_ENDPOINT=https://your-cluster.europe-west3-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key-here
QDRANT_CLUSTER_ID=your-cluster-id

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true
"@ | Out-File -FilePath .env.example -Encoding UTF8 -Force

Write-Host "✅ .env.example created" -ForegroundColor Green
```

### Step 4: Initialize Git Repository
```powershell
# Initialize git repo
git init

# Configure git (use your GitHub username and email)
git config user.name "RAJARYANSINGH0059"
git config user.email "your-email@gmail.com"  # Replace with your email

# Add all files (except those in .gitignore)
git add .

# Create initial commit
git commit -m "Initial commit: Clinical AI Multi-Agent System

- 14+ specialized AI agents
- Multi-modal medical data processing
- Qdrant vector database integration
- Multi-LLM reasoning (ChatGPT + Gemini)
- Risk-stratified recommendations
- Production-ready deployment infrastructure"

Write-Host "✅ Git repository initialized" -ForegroundColor Green
```

### Step 5: Add GitHub Remote and Push
```powershell
# Add remote origin
git remote add origin https://github.com/RAJARYANSINGH0059/Convolve.git

# Rename branch to main (GitHub default)
git branch -M main

# Push to GitHub
git push -u origin main

Write-Host "✅ Code pushed to GitHub!" -ForegroundColor Green
Write-Host "Repository: https://github.com/RAJARYANSINGH0059/Convolve" -ForegroundColor Cyan
```

### Step 6: Verify on GitHub
1. Go to https://github.com/RAJARYANSINGH0059/Convolve
2. You should see all your files deployed
3. The .env file should NOT be visible (protected by .gitignore)

---

## 📋 Complete Automated Deployment Script

Save this as `deploy-to-github.ps1` in your project root and run it:

```powershell
# Deploy to GitHub - Clinical AI System
# Run: .\deploy-to-github.ps1

param(
    [string]$GithubUsername = "RAJARYANSINGH0059",
    [string]$GithubRepo = "Convolve",
    [string]$UserEmail = "your-email@gmail.com"  # Edit this!
)

# Navigate to project directory
$projectPath = "C:\Users\rajar\Desktop\EXPERIMENT\agent 2\last attempt\clinical_ai_multi_agent"
Set-Location $projectPath

Write-Host "🚀 Starting GitHub Deployment..." -ForegroundColor Cyan
Write-Host "Repository: $GithubUsername/$GithubRepo" -ForegroundColor Green

# Step 1: Create .gitignore
Write-Host "`n1️⃣ Creating .gitignore..." -ForegroundColor Yellow
$gitignoreContent = @"
# Environment variables
.env
.env.local

# Python
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
build/
develop-eggs/
dist/
*.egg-info/
.installed.cfg
*.egg
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
"@
Set-Content -Path ".gitignore" -Value $gitignoreContent -Encoding UTF8
Write-Host "✅ .gitignore created" -ForegroundColor Green

# Step 2: Create .env.example
Write-Host "`n2️⃣ Creating .env.example..." -ForegroundColor Yellow
$envExampleContent = @"
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4-turbo

# Google Configuration
GOOGLE_API_KEY=your-google-api-key-here
GOOGLE_MODEL_ID=gemini-pro

# Qdrant Configuration
QDRANT_ENDPOINT=https://your-cluster.europe-west3-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key-here
QDRANT_CLUSTER_ID=your-cluster-id

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true
"@
Set-Content -Path ".env.example" -Value $envExampleContent -Encoding UTF8
Write-Host "✅ .env.example created" -ForegroundColor Green

# Step 3: Initialize Git
Write-Host "`n3️⃣ Initializing Git repository..." -ForegroundColor Yellow
git init
git config user.name $GithubUsername
git config user.email $UserEmail
Write-Host "✅ Git initialized" -ForegroundColor Green

# Step 4: Add and Commit
Write-Host "`n4️⃣ Adding files and creating commit..." -ForegroundColor Yellow
git add .
git commit -m "Initial commit: Clinical AI Multi-Agent System

- 14+ specialized AI agents
- Multi-modal medical data processing
- Qdrant vector database integration
- Multi-LLM reasoning (ChatGPT + Gemini)
- Risk-stratified recommendations
- Production-ready deployment infrastructure
- API with 8 endpoints
- Web dashboard
- Comprehensive documentation"

Write-Host "✅ Files committed" -ForegroundColor Green

# Step 5: Add Remote and Push
Write-Host "`n5️⃣ Adding GitHub remote and pushing..." -ForegroundColor Yellow
$repoUrl = "https://github.com/$GithubUsername/$GithubRepo.git"
git remote add origin $repoUrl
git branch -M main
git push -u origin main

Write-Host "`n✅ Deployment Complete!" -ForegroundColor Green
Write-Host "🌐 Your repository: $repoUrl" -ForegroundColor Cyan
```

---

## 🔐 Security Notes

### ✅ What Gets Deployed:
- All source code (agents, API, utilities)
- Configuration templates (.env.example)
- Documentation (README, guides, etc.)
- Tests and test data
- Docker files
- Setup scripts

### ❌ What Does NOT Get Deployed:
- Your .env file (protected by .gitignore)
- API keys and sensitive credentials
- Virtual environment (venv/)
- Python cache files
- IDE settings

### 🔒 If You Accidentally Pushed .env:
```powershell
# Remove from git history
git rm --cached .env
git commit -m "Remove .env file from tracking"
git push origin main

# Regenerate your API keys immediately!
```

---

## 📝 After Deployment

### Update Your GitHub Repository Settings:
1. Go to https://github.com/RAJARYANSINGH0059/Convolve
2. Click "Settings" → "About"
3. Add description: "Clinical AI Multi-Agent System for Medical Intelligence"
4. Add topics: `ai`, `clinical`, `medical-intelligence`, `multi-agent`, `fastapi`

### Add README.md to GitHub:
The README.md is already in your project and will be displayed on GitHub homepage.

### Enable GitHub Pages (Optional):
1. Settings → Pages
2. Select "main" branch
3. Your documentation will be available at: https://rajaryansingh0059.github.io/Convolve

---

## 🚀 After Push - What's Next?

### 1. Clone on Another Machine:
```powershell
git clone https://github.com/RAJARYANSINGH0059/Convolve.git
cd Convolve
cp .env.example .env
# Edit .env with your API keys
.\setup.ps1 -Action full
```

### 2. Keep Your Local Repo Updated:
```powershell
git pull origin main
```

### 3. Create a Branch for Development:
```powershell
git checkout -b feature/your-feature-name
# Make changes
git add .
git commit -m "Add your feature"
git push origin feature/your-feature-name
# Create Pull Request on GitHub
```

---

## ✅ Deployment Checklist

Before deploying:
- [ ] Git is installed on your system
- [ ] .gitignore file is created
- [ ] .env.example is created
- [ ] No sensitive data in code
- [ ] All tests pass
- [ ] README.md is complete
- [ ] Documentation is updated

During deployment:
- [ ] Git repository initialized
- [ ] Files added to git
- [ ] Initial commit created
- [ ] Remote origin added
- [ ] Code pushed to GitHub

After deployment:
- [ ] GitHub repository is public
- [ ] README is visible
- [ ] .env file is NOT visible
- [ ] All code is accessible
- [ ] Documentation links work

---

**Next Step: Install Git, then run the deployment script! 🚀**
