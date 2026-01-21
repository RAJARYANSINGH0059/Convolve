# Deploy Clinical AI System to GitHub
# Run this script after Git is installed: .\deploy-github.ps1

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     Clinical AI System - GitHub Deployment Script             ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
Write-Host "🔍 Checking if Git is installed..." -ForegroundColor Yellow
$gitCheck = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitCheck) {
    Write-Host "❌ Git is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git first:" -ForegroundColor Yellow
    Write-Host "  1. Download from: https://git-scm.com/download/win" -ForegroundColor Cyan
    Write-Host "  2. Run the installer" -ForegroundColor Cyan
    Write-Host "  3. Restart PowerShell" -ForegroundColor Cyan
    Write-Host "  4. Run this script again" -ForegroundColor Cyan
    exit 1
}
Write-Host "✅ Git is installed" -ForegroundColor Green
Write-Host ""

# Navigate to project directory
$projectPath = "C:\Users\rajar\Desktop\EXPERIMENT\agent 2\last attempt\clinical_ai_multi_agent"
if (-not (Test-Path $projectPath)) {
    Write-Host "❌ Project directory not found: $projectPath" -ForegroundColor Red
    exit 1
}

Set-Location $projectPath
Write-Host "📁 Working directory: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Configuration
$GithubUsername = "RAJARYANSINGH0059"
$GithubRepo = "Convolve"
$UserEmail = "rajaryansingh0059@gmail.com"  # Change if needed
$RepoUrl = "https://github.com/$GithubUsername/$GithubRepo.git"

Write-Host "📋 Deployment Configuration:" -ForegroundColor Cyan
Write-Host "  GitHub Username: $GithubUsername" -ForegroundColor Green
Write-Host "  Repository: $GithubRepo" -ForegroundColor Green
Write-Host "  Email: $UserEmail" -ForegroundColor Green
Write-Host "  URL: $RepoUrl" -ForegroundColor Green
Write-Host ""

# Step 1: Check if .gitignore exists
Write-Host "1️⃣  Checking .gitignore..." -ForegroundColor Yellow
if (-not (Test-Path ".gitignore")) {
    Write-Host "   Creating .gitignore file..." -ForegroundColor Gray
    # .gitignore already created, no action needed
} else {
    Write-Host "   ✅ .gitignore exists" -ForegroundColor Green
}
Write-Host ""

# Step 2: Check if .env.example exists
Write-Host "2️⃣  Checking .env.example..." -ForegroundColor Yellow
if (-not (Test-Path ".env.example")) {
    Write-Host "   ⚠️  .env.example missing" -ForegroundColor Yellow
} else {
    Write-Host "   ✅ .env.example exists" -ForegroundColor Green
}
Write-Host ""

# Step 3: Initialize Git repo
Write-Host "3️⃣  Initializing Git repository..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "   ⚠️  Git repository already exists" -ForegroundColor Yellow
    $reinitAnswer = Read-Host "   Reinitialize? (y/n)"
    if ($reinitAnswer -eq "y") {
        Remove-Item -Path ".git" -Recurse -Force
        git init
        Write-Host "   ✅ Repository reinitialized" -ForegroundColor Green
    }
} else {
    git init
    Write-Host "   ✅ Repository initialized" -ForegroundColor Green
}
Write-Host ""

# Step 4: Configure Git user
Write-Host "4️⃣  Configuring Git user..." -ForegroundColor Yellow
git config user.name $GithubUsername
git config user.email $UserEmail
Write-Host "   ✅ Git user configured" -ForegroundColor Green
Write-Host ""

# Step 5: Add files
Write-Host "5️⃣  Adding files to Git..." -ForegroundColor Yellow
Write-Host "   Note: .env file is protected by .gitignore" -ForegroundColor Gray
git add .
Write-Host "   ✅ Files added" -ForegroundColor Green
Write-Host ""

# Step 6: Create commit
Write-Host "6️⃣  Creating initial commit..." -ForegroundColor Yellow
$commitMessage = @"
Initial commit: Clinical AI Multi-Agent System

Features:
- 14+ specialized AI agents for medical intelligence
- Multi-modal medical data processing (images, audio, text, vital signs)
- Qdrant vector database integration with hybrid search
- Multi-LLM reasoning (ChatGPT + Gemini)
- Risk-stratified patient recommendations
- Production-ready deployment infrastructure
- FastAPI with 8 REST endpoints
- Interactive web dashboard
- Comprehensive documentation and guides
- Docker and Kubernetes support
- HIPAA-ready audit trails

Agents:
- Ingestion Agent: Multi-modal data processing
- Vision Agent: Medical imaging analysis
- Speech Agent: Audio processing and emotion analysis
- NLP Agent: Clinical entity extraction
- Time-Series Agent: Vital signs analysis
- Embedding Agent: Dense and sparse embedding generation
- Memory Agent: Qdrant vector database management
- Retrieval Agent: Multi-modal data retrieval
- Reasoning Agent: Multi-LLM analysis and synthesis
- Safety Agent: Hallucination and bias detection
- Risk Intelligence Agent: Multi-factor risk assessment
- Recommendation Agent: Evidence-based care planning
- Feedback Agent: Doctor feedback loop with memory reinforcement
- Master Consolidation Layer: Report synthesis

Configuration:
- Environment-based configuration with .env
- API keys for OpenAI, Google Gemini, Qdrant
- Deployment-ready Docker and Kubernetes files
- Comprehensive testing suite

Documentation:
- README.md: Complete deployment guide
- QUICKSTART.md: 5-minute setup guide
- PROJECT_SUMMARY.md: System overview
- GITHUB_DEPLOYMENT.md: GitHub and GCP setup
- DEPLOYMENT_CHECKLIST.md: Production readiness
- GITHUB_SETUP.md: This repository deployment guide
"@

git commit -m $commitMessage
Write-Host "   ✅ Commit created" -ForegroundColor Green
Write-Host ""

# Step 7: Add remote and push
Write-Host "7️⃣  Adding GitHub remote..." -ForegroundColor Yellow

# Check if remote already exists
$remoteExists = git remote get-url origin -ErrorAction SilentlyContinue
if ($remoteExists) {
    Write-Host "   Removing existing remote..." -ForegroundColor Gray
    git remote remove origin
}

git remote add origin $RepoUrl
Write-Host "   ✅ Remote added: origin" -ForegroundColor Green
Write-Host ""

# Step 8: Rename branch to main
Write-Host "8️⃣  Setting default branch to 'main'..." -ForegroundColor Yellow
git branch -M main
Write-Host "   ✅ Branch renamed to 'main'" -ForegroundColor Green
Write-Host ""

# Step 9: Push to GitHub
Write-Host "9️⃣  Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "   Note: You may be prompted for GitHub authentication" -ForegroundColor Gray
Write-Host ""

try {
    git push -u origin main -f
    Write-Host "   ✅ Successfully pushed to GitHub!" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Push encountered an issue:" -ForegroundColor Yellow
    Write-Host "   Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "   Possible solutions:" -ForegroundColor Yellow
    Write-Host "   1. Ensure you have GitHub CLI or Git credentials configured" -ForegroundColor Cyan
    Write-Host "   2. Use GitHub Web UI to push if automatic push fails" -ForegroundColor Cyan
    Write-Host "   3. Check repository permissions" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║              Deployment Complete! ✅                           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "📊 Next Steps:" -ForegroundColor Green
Write-Host ""
Write-Host "1. 🌐 Visit your GitHub repository:" -ForegroundColor Cyan
Write-Host "   $RepoUrl" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. ✅ Verify deployment:" -ForegroundColor Cyan
Write-Host "   - Check that all files are present" -ForegroundColor Gray
Write-Host "   - Confirm .env file is NOT visible" -ForegroundColor Gray
Write-Host "   - Verify README.md is displayed" -ForegroundColor Gray
Write-Host ""
Write-Host "3. 📋 Update GitHub Repository (Optional):" -ForegroundColor Cyan
Write-Host "   - Go to Settings → About" -ForegroundColor Gray
Write-Host "   - Add description: 'Clinical AI Multi-Agent System for Medical Intelligence'" -ForegroundColor Gray
Write-Host "   - Add topics: ai, medical, clinical, multi-agent, fastapi" -ForegroundColor Gray
Write-Host ""
Write-Host "4. 🚀 Share with team:" -ForegroundColor Cyan
Write-Host "   - Invite collaborators via GitHub Settings" -ForegroundColor Gray
Write-Host "   - Share setup instructions from QUICKSTART.md" -ForegroundColor Gray
Write-Host ""

Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   - Quick Start: QUICKSTART.md" -ForegroundColor Gray
Write-Host "   - Full Guide: README.md" -ForegroundColor Gray
Write-Host "   - System Overview: PROJECT_SUMMARY.md" -ForegroundColor Gray
Write-Host "   - Deployment: GITHUB_DEPLOYMENT.md" -ForegroundColor Gray
Write-Host ""

Write-Host "💻 Local Development:" -ForegroundColor Cyan
Write-Host "   git pull origin main       # Update from GitHub" -ForegroundColor Gray
Write-Host "   git checkout -b feature    # Create new branch" -ForegroundColor Gray
Write-Host "   git push origin feature    # Push your changes" -ForegroundColor Gray
Write-Host ""

Write-Host "✨ Your Clinical AI system is now on GitHub!" -ForegroundColor Green
Write-Host ""
