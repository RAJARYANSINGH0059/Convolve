# How to Deploy on GitHub & GCP

## 📦 GitHub Repository Setup

### 1. Create GitHub Repository

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: Clinical AI Multi-Agent System"

# Create repository on GitHub (via web UI)
# Visit github.com and create new repository

# Add remote and push
git remote add origin https://github.com/YOUR-USERNAME/clinical_ai_multi_agent.git
git branch -M main
git push -u origin main
```

### 2. GitHub Repository Structure

Essential files for GitHub:

```
clinical_ai_multi_agent/
├── .gitignore                 # Ignore venv, .env, __pycache__
├── .github/
│   ├── workflows/
│   │   ├── tests.yml         # CI/CD pipeline
│   │   └── deploy.yml        # Deployment automation
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── README.md                  # Main documentation
├── QUICKSTART.md             # 5-minute setup
├── PROJECT_SUMMARY.md        # Overview
├── DEPLOYMENT_CHECKLIST.md   # Checklist
├── LICENSE                   # MIT License
├── CONTRIBUTING.md           # Contribution guidelines
├── CODE_OF_CONDUCT.md        # Community standards
└── ... (rest of project files)
```

### 3. Create .gitignore

```bash
# Create .gitignore file
cat > .gitignore << 'EOF'
# Virtual environments
venv/
env/
ENV/
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

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Logs
*.log
logs/

# Database
*.db
*.sqlite
*.sqlite3

# Data
/tmp/
/test_data/
*.csv
*.json
*.pkl

# Docker
.docker/

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
temp/
EOF
```

### 4. Create LICENSE

```bash
# Create MIT License file
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 Clinical AI Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
```

### 5. Create CONTRIBUTING.md

```bash
cat > CONTRIBUTING.md << 'EOF'
# Contributing to Clinical AI Multi-Agent System

## Code of Conduct

Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Bugs
1. Check if bug already exists in Issues
2. Provide clear description with steps to reproduce
3. Include Python version, OS, and error traceback
4. Create issue with `bug` label

### Suggesting Features
1. Check if feature already suggested
2. Describe use case and expected behavior
3. Explain why it would be useful
4. Create issue with `enhancement` label

### Pull Requests
1. Fork repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes with clear commit messages
4. Add tests for new functionality
5. Run: `pytest tests/test_integration.py -v`
6. Submit PR with description of changes

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/clinical_ai_multi_agent.git
cd clinical_ai_multi_agent

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov

# Run tests
pytest tests/ -v --cov

# Make changes...
# Commit and push
# Create pull request
```

## Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions
- Keep lines under 100 characters
- Use meaningful variable names

## Testing

- All new features must include tests
- Tests should be in `tests/` directory
- Run `pytest` before submitting PR
- Aim for > 80% code coverage

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🙏
EOF
```

### 6. Create CODE_OF_CONDUCT.md

```bash
cat > CODE_OF_CONDUCT.md << 'EOF'
# Code of Conduct

## Our Commitment

We are committed to providing a welcoming and inclusive environment for all contributors.

## Our Standards

Examples of behavior that contributes to a positive environment:
- Using welcoming and inclusive language
- Being respectful of differing opinions
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior:
- Harassment or discrimination
- Insulting or derogatory comments
- Personal attacks
- Unwelcome sexual attention
- Trolling or inflammatory comments

## Enforcement

Instances of unacceptable behavior should be reported to the project maintainers.

All complaints will be reviewed and investigated promptly and fairly.

EOF
```

---

## 🔄 GitHub CI/CD Pipeline

### Create GitHub Actions Workflow

```bash
mkdir -p .github/workflows
cat > .github/workflows/tests.yml << 'EOF'
name: Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=100 --statistics
    
    - name: Test with pytest
      run: |
        pytest tests/ -v --cov=agents --cov=api --cov=consolidation
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
EOF
```

### Create Deployment Workflow

```bash
cat > .github/workflows/deploy.yml << 'EOF'
name: Deploy to GCP

on:
  push:
    branches: [ main ]
    paths:
      - 'agents/**'
      - 'api/**'
      - 'Dockerfile'
      - 'requirements.txt'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Cloud SDK
      uses: google-github-actions/setup-gcloud@v1
      with:
        service_account_key: ${{ secrets.GCP_SA_KEY }}
        project_id: ${{ secrets.GCP_PROJECT_ID }}
    
    - name: Configure Docker
      run: |
        gcloud auth configure-docker
    
    - name: Build Docker image
      run: |
        docker build -t gcr.io/${{ secrets.GCP_PROJECT_ID }}/clinical-ai:latest .
    
    - name: Push to Container Registry
      run: |
        docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/clinical-ai:latest
    
    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy clinical-ai \
          --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/clinical-ai:latest \
          --platform managed \
          --region us-central1 \
          --memory 4Gi \
          --cpu 2 \
          --set-env-vars OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }} \
          --set-env-vars GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }}
EOF
```

### Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

```
GCP_PROJECT_ID = your-gcp-project-id
GCP_SA_KEY = (paste your service account JSON key)
OPENAI_API_KEY = your-openai-key
GEMINI_API_KEY = your-gemini-key
```

---

## ☁️ GCP Deployment Guide

### 1. Create GCP Project

```bash
# Create new project
gcloud projects create clinical-ai-prod --name="Clinical AI Production"

# Set as active project
gcloud config set project clinical-ai-prod
```

### 2. Enable Required APIs

```bash
gcloud services enable \
    run.googleapis.com \
    aiplatform.googleapis.com \
    texttospeech.googleapis.com \
    containerregistry.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com
```

### 3. Create Service Account for GCP

```bash
# Create service account
gcloud iam service-accounts create clinical-ai \
    --display-name="Clinical AI Service Account"

# Get email
SERVICE_ACCOUNT=$(gcloud iam service-accounts list \
    --filter="displayName:Clinical" \
    --format='value(email)')

# Grant Cloud Run permissions
gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
    --member=serviceAccount:$SERVICE_ACCOUNT \
    --role=roles/run.admin

# Grant AI Platform permissions
gcloud projects add-iam-policy-binding $(gcloud config get-value project) \
    --member=serviceAccount:$SERVICE_ACCOUNT \
    --role=roles/aiplatform.user

# Create and download key for GitHub Actions
gcloud iam service-accounts keys create key.json \
    --iam-account=$SERVICE_ACCOUNT

# Upload key to GitHub (Settings → Secrets)
cat key.json | jq -r '@base64' | xclip -selection clipboard
```

### 4. Create Secrets in GCP

```bash
# Create secrets for API keys
echo -n "sk-xxxxxxx" | gcloud secrets create openai-api-key --data-file=-
echo -n "xxxxxxx" | gcloud secrets create gemini-api-key --data-file=-
echo -n "xxxxxxx" | gcloud secrets create qdrant-api-key --data-file=-
```

### 5. Deploy to Cloud Run

```bash
# Option 1: Via command line
gcloud run deploy clinical-ai \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 4Gi \
    --cpu 2 \
    --timeout 3600 \
    --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY,GEMINI_API_KEY=$GEMINI_API_KEY

# Option 2: Via Docker image
docker build -t gcr.io/clinical-ai-prod/clinical-ai:latest .
docker push gcr.io/clinical-ai-prod/clinical-ai:latest

gcloud run deploy clinical-ai \
    --image gcr.io/clinical-ai-prod/clinical-ai:latest \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 4Gi \
    --cpu 2
```

### 6. Setup Custom Domain (Optional)

```bash
# Create Cloud Armor security policy (optional)
gcloud compute security-policies create clinical-ai-policy

# Map custom domain
# Go to Cloud Run console → Select service → Manage custom domains
# Add your domain and complete verification
```

### 7. Setup Monitoring

```bash
# View logs
gcloud run logs read clinical-ai --limit 50

# Setup cloud monitoring dashboard
gcloud monitoring dashboards create --config-from-file=monitoring-dashboard.yaml
```

---

## 📊 GitHub Repository Settings

### 1. Enable Branch Protection

Settings → Branches → Add branch protection rule

For `main` branch:
- [x] Require pull request reviews before merging (1 review)
- [x] Require status checks to pass before merging
- [x] Require branches to be up to date before merging
- [x] Include administrators

### 2. Configure Issues

Settings → Features:
- [x] Issues
- [x] Discussions

Templates in `.github/ISSUE_TEMPLATE/`:
- Bug report
- Feature request

### 3. Setup Rulesets (GitHub Advanced)

Go to Rules → New ruleset:
- Require status checks
- Require dismissal of stale reviews
- Restrict commits

---

## 🎯 Deployment Workflow

```
Local Development
    ↓
Create Feature Branch
    ↓
Make Changes + Tests
    ↓
Push to GitHub
    ↓
GitHub Actions Tests (Automated)
    ↓
Create Pull Request
    ↓
Code Review
    ↓
Merge to main
    ↓
GitHub Actions Deploy (Automated)
    ↓
Deploy to Cloud Run
    ↓
Production Live! 🚀
```

---

## 📋 Repository Checklist

Before pushing to GitHub:

- [ ] .gitignore is complete
- [ ] No secrets in code
- [ ] README.md is comprehensive
- [ ] LICENSE file is present (MIT)
- [ ] CONTRIBUTING.md explains how to contribute
- [ ] CODE_OF_CONDUCT.md is clear
- [ ] All tests pass locally
- [ ] Requirements.txt is complete
- [ ] Dockerfile works
- [ ] Documentation is accurate
- [ ] Examples are tested
- [ ] Comments explain complex code

---

## 🚀 First Release Checklist

Before v1.0 release:

- [ ] All features working
- [ ] Tests pass (>80% coverage)
- [ ] Documentation complete
- [ ] Deployment guides tested
- [ ] Security audit passed
- [ ] Performance optimized
- [ ] All issues resolved
- [ ] Create release notes
- [ ] Tag version v1.0.0
- [ ] Publish on PyPI (optional)

```bash
# Create release tag
git tag -a v1.0.0 -m "Initial release: Clinical AI Multi-Agent System"
git push origin v1.0.0
```

---

## 📞 GitHub Collaboration

### Get Help
- Check Issues for similar problems
- Create new Issue if needed
- Participate in Discussions
- Read documentation first

### Report Bug
1. Search existing issues
2. Create issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Error logs/screenshots
   - Python/OS version

### Request Feature
1. Search existing issues
2. Create issue with:
   - Clear description of feature
   - Use case
   - Proposed implementation (if any)
   - Any concerns

### Submit PR
1. Fork repository
2. Create feature branch
3. Make changes
4. Run tests locally
5. Push to GitHub
6. Create PR with description
7. Respond to review comments
8. Merge after approval

---

**Ready to share with the world!** 🌍

Next: Add badges, social links, and community to README
