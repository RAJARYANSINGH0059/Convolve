# Clinical AI Multi-Agent System - Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will help you get the Clinical AI system running on your local machine.

---

## Step 1: Prerequisites (1 minute)

### Required:
- **Python 3.11+** - [Download here](https://www.python.org/downloads/)
- **API Keys** (free tier available):
  - OpenAI: https://platform.openai.com/api-keys
  - Gemini: https://makersuite.google.com/app/apikey
  - Qdrant: https://cloud.qdrant.io (sign up free)

### Optional:
- **Docker** - For containerized deployment
- **Git** - For version control

---

## Step 2: Clone and Setup (2 minutes)

### On Windows (PowerShell):
```powershell
# Navigate to your workspace
cd C:\Users\YourUsername\Desktop

# Run the setup script (interactive menu)
.\setup.ps1

# Or automated full setup
.\setup.ps1 -Action full
```

### On macOS/Linux (Terminal):
```bash
# Navigate to your workspace
cd ~/Desktop

# Run the setup script (interactive menu)
./setup.sh

# Or automated full setup
./setup.sh full
```

---

## Step 3: Configure API Keys (1 minute)

1. **Copy template file:**
   ```bash
   cp .env.template .env
   ```

2. **Edit `.env` file with your credentials:**
   ```
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
   GEMINI_API_KEY=your-gemini-api-key
   QDRANT_ENDPOINT=https://your-cluster.qdrant.io
   QDRANT_API_KEY=your-qdrant-api-key
   ```

3. **Save the file** (no restart needed for development server)

---

## Step 4: Run the System (1 minute)

### Start Development Server:

**Windows:**
```powershell
.\setup.ps1 -Action dev
```

**macOS/Linux:**
```bash
./setup.sh dev
```

**Or manually:**
```bash
# Activate virtual environment first
# Windows: venv\Scripts\Activate.ps1
# macOS/Linux: source venv/bin/activate

python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Access the System:
- **Web Dashboard:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

---

## Step 5: Test End-to-End (Optional)

```bash
# Generate synthetic test data (10 patients)
python tests/test_data_generator.py

# Run comprehensive tests
python -m pytest tests/test_integration.py -v
```

---

## 📊 Dashboard Features

### Patient Management
- Create new patient records
- Upload multi-modal medical data (images, audio, text, vital signs)
- View patient history and previous analyses

### Medical Analysis
- **14+ specialized AI agents** process data in parallel
- **Multi-LLM reasoning** (ChatGPT + Gemini)
- **Qdrant vector search** finds similar cases automatically
- Risk-stratified recommendations

### Reports & Export
- View Clinical Intelligence Summary (CIS)
- Download PDF reports
- Generate multi-language audio narration (8 languages)
- Export as JSON for integration

---

## 🔌 API Quick Reference

### Create Patient
```bash
curl -X POST http://localhost:8000/api/patients/create \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 45,
    "gender": "M",
    "mrn": "MRN123456"
  }'
```

### Ingest Medical Data
```bash
curl -X POST http://localhost:8000/api/ingest/multi-modal \
  -F "patient_id=PT-001" \
  -F "clinical_note=@clinical_note.txt" \
  -F "vital_signs=@vitals.csv" \
  -F "medical_image=@xray.png"
```

### Analyze Patient
```bash
curl -X POST http://localhost:8000/api/analyze/patient \
  -H "Content-Type: application/json" \
  -d '{"patient_id": "PT-001"}'
```

### Submit Doctor Feedback
```bash
curl -X POST http://localhost:8000/api/feedback/submit \
  -F "patient_id=PT-001" \
  -F "voice_feedback=@feedback.wav" \
  -F "feedback_type=CORRECT"
```

---

## 🐳 Deploy with Docker

### Build Image:
```bash
docker build -t clinical-ai:latest .
```

### Run Container:
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  -e QDRANT_ENDPOINT=$QDRANT_ENDPOINT \
  -e QDRANT_API_KEY=$QDRANT_API_KEY \
  clinical-ai:latest
```

---

## ☁️ Deploy to GCP Cloud Run

### 1. Authenticate with GCP:
```bash
gcloud auth login
gcloud config set project YOUR-PROJECT-ID
```

### 2. Push Image to Container Registry:
```bash
PROJECT_ID=$(gcloud config get-value project)

docker build -t gcr.io/${PROJECT_ID}/clinical-ai:latest .
docker push gcr.io/${PROJECT_ID}/clinical-ai:latest
```

### 3. Deploy to Cloud Run:
```bash
gcloud run deploy clinical-ai \
    --image gcr.io/${PROJECT_ID}/clinical-ai:latest \
    --platform managed \
    --region us-central1 \
    --memory 4Gi \
    --cpu 2 \
    --timeout 3600 \
    --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY,GEMINI_API_KEY=$GEMINI_API_KEY \
    --set-env-vars QDRANT_ENDPOINT=$QDRANT_ENDPOINT,QDRANT_API_KEY=$QDRANT_API_KEY \
    --allow-unauthenticated
```

### 4. Access Deployed Service:
The output will include your service URL (e.g., `https://clinical-ai-xxxxx.run.app`)

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Cannot connect to Qdrant"
**Solution:**
1. Verify your Qdrant endpoint is correct
2. Check your API key
3. Test connectivity:
   ```bash
   curl https://your-cluster.qdrant.io/health \
     -H "api-key: YOUR_API_KEY"
   ```

### Issue: "OpenAI API rate limit exceeded"
**Solution:**
- Wait a few minutes and retry
- Consider upgrading your OpenAI plan
- Implement retry logic in your code

### Issue: "Port 8000 already in use"
**Solution:**
```bash
# Use a different port
python -m uvicorn api.main:app --reload --port 8001
```

---

## 📚 System Architecture

```
┌─────────────────────────────────────┐
│   FastAPI REST API (Port 8000)      │
│   • Dashboard: http://localhost     │
│   • API Docs: /docs                 │
└──────────────┬──────────────────────┘
               │
        ┌──────▼──────┐
        │   14 Agents │
        ├─────────────┤
        │ • Agent 1: Ingestion + Qdrant
        │ • Agent 2: Multi-LLM Reasoning
        │ • Agent 3: Doctor Feedback
        │ • Vision, Speech, NLP, TimeSeries
        │ • Safety, Risk, Recommendations
        │ • + 7 more specialized agents
        └──────┬──────┘
               │
        ┌──────▼──────────┐
        │ Qdrant Vector DB │
        │ (Hybrid Search)  │
        └──────┬───────────┘
               │
        ┌──────▼──────────┐
        │ Clinical Summary │
        │ + PDF/TTS Export │
        └──────────────────┘
```

---

## 🎯 Key Features Overview

### Multi-Agent Architecture
- **14+ specialized agents** process medical data in parallel
- Each agent has specific expertise (vision, speech, NLP, time-series, etc.)
- Agents communicate through FastAPI orchestrator

### Advanced Vector Search
- **Qdrant hybrid search** combines dense + sparse embeddings
- Automatically finds similar patient cases
- Extracts disease trends and medication patterns from historical data

### Multi-LLM Reasoning
- **ChatGPT (GPT-4 Turbo)** provides detailed analysis
- **Gemini Pro** offers alternative perspectives
- **Vertex AI** consolidates results intelligently

### Doctor Feedback Loop
- Capture voice feedback from doctors
- Classify feedback as CORRECT, PARTIAL, or WRONG
- Automatically reinforce learning in Qdrant
- Create complete audit trails for compliance

### User-Friendly Output
- **Clinical Intelligence Summary (CIS)** in plain language
- **Multi-language support** (8 languages via Google Cloud TTS)
- **Risk-stratified recommendations** (Critical, High, Moderate, Low)
- **PDF reports** with narration and visualizations

---

## 📖 Learn More

- **Full Documentation:** See [README.md](README.md)
- **API Reference:** Run server and visit `/docs`
- **GitHub Issues:** Report bugs and feature requests
- **Community:** Join our Discord for support

---

## 🚀 Next Steps

1. ✅ Server is running - check dashboard
2. 📁 Upload test patient data
3. 🧠 Run end-to-end analysis
4. 📊 View generated Clinical Intelligence Summary
5. 🎙️ Generate multi-language narration
6. ☁️ Deploy to GCP for production use

---

## 💡 Tips

- **Save API Key in .env:** Don't hardcode credentials
- **Use test data:** Run `test_data_generator.py` to create 10 sample patients
- **Monitor logs:** Watch terminal for insights into agent processing
- **Enable debug mode:** Set `API_DEBUG=true` in .env for verbose logging
- **Backup regularly:** Qdrant stores all your embeddings - don't lose data

---

## Support

- **Documentation:** Full README.md in project root
- **Issues:** GitHub Issues page
- **Email:** support@clinicalai.dev
- **Community:** Discord server (link in README)

---

**Happy analyzing! 🏥🤖**

*Last updated: January 2024*
*Version: 1.0.0*
