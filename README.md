# Clinical AI Multi-Agent System - Complete Deployment Guide

## Overview

A production-ready multi-agent clinical intelligence system with 14+ specialized agents processing medical data across 4 modalities (Images, Audio, Text, Time-Series), powered by multi-LLM reasoning (ChatGPT + Gemini) and advanced vector search (Qdrant).

**Key Features:**
- ✅ 14 specialized medical AI agents (parallel processing)
- ✅ Multi-modal data ingestion (Images, Audio, Text, Time-Series)
- ✅ Multi-LLM reasoning with complete thinking chains
- ✅ Qdrant hybrid vector search (dense + sparse embeddings)
- ✅ Doctor feedback loop with memory reinforcement
- ✅ Multi-language support (8 languages via Google Cloud TTS)
- ✅ Clinical Intelligence Summary (CIS) generation
- ✅ Risk-stratified recommendations with disease trajectory prediction
- ✅ HIPAA-ready audit trails
- ✅ Cloud-native deployment (GCP, Kubernetes, Docker)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Configuration](#configuration)
4. [Running the System](#running-the-system)
5. [Testing](#testing)
6. [API Documentation](#api-documentation)
7. [Deployment to GCP](#deployment-to-gcp)
8. [Kubernetes Deployment](#kubernetes-deployment)
9. [Troubleshooting](#troubleshooting)
10. [Architecture Overview](#architecture-overview)

---

## Prerequisites

### Required Software
- **Python 3.11+** (download from [python.org](https://www.python.org/downloads/))
- **Docker** (download from [docker.com](https://www.docker.com/products/docker-desktop))
- **GCP Account** with the following enabled:
  - Cloud Run
  - Vertex AI
  - Cloud Text-to-Speech
  - Container Registry
  - Service Account with appropriate roles

### Required API Keys
1. **OpenAI API Key** - For ChatGPT analysis
   - Get from: https://platform.openai.com/api-keys
   - Model: gpt-4-turbo-preview
   
2. **Google Gemini API Key** - For alternative LLM perspective
   - Get from: https://makersuite.google.com/app/apikey
   - Model: gemini-pro

3. **Qdrant Vector Database**
   - Hosted instance: https://cloud.qdrant.io
   - Free tier: 4GB storage, 2 collections
   - Or self-hosted Docker instance

### System Requirements
- **CPU**: 2+ cores
- **RAM**: 4GB+ (8GB+ recommended for multi-patient processing)
- **Storage**: 10GB+ for test data and embeddings
- **Internet**: For API calls to OpenAI, Gemini, Qdrant, Google Cloud

---

## Local Development Setup

### Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/clinical_ai_multi_agent.git
cd clinical_ai_multi_agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python -c "import fastapi, qdrant_client, openai; print('All dependencies installed!')"
```

### Step 3: Create Configuration Files

Create a `.env` file in the project root:

```bash
# .env file
OPENAI_API_KEY=your-openai-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here
QDRANT_ENDPOINT=https://your-cluster.europe-west3-0.gcp.cloud.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key-here
QDRANT_CLUSTER_ID=your-cluster-id

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/gcp-service-account.json
GCP_PROJECT_ID=your-gcp-project-id
GCP_REGION=us-central1

# Model Configuration
OPENAI_MODEL=gpt-4-turbo-preview
GEMINI_MODEL=gemini-pro
VERTEX_AI_MODEL=gemini-1.5-pro

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=False
```

### Step 4: Update Configuration

Edit `config/settings.py` to match your environment:

```python
# config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str = "your-key"
    GEMINI_API_KEY: str = "your-key"
    QDRANT_ENDPOINT: str = "https://cluster.qdrant.io"
    QDRANT_API_KEY: str = "your-key"
    
    # Other configurations...
    class Config:
        env_file = ".env"
```

---

## Configuration

### Qdrant Setup

```python
# Initialize Qdrant client
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(
    url="https://your-cluster.europe-west3-0.gcp.cloud.qdrant.io",
    api_key="your-api-key"
)

# Create collection for medical embeddings
client.recreate_collection(
    collection_name="medical_records",
    vectors_config=VectorParams(size=3072, distance=Distance.COSINE),  # Dense embeddings
    sparse_vectors_config=SparseVectorParams(
        index=SparseIndexParams(on_disk=True)
    )
)
```

### Google Cloud Setup

```bash
# Authenticate with GCP
gcloud auth login
gcloud config set project YOUR-PROJECT-ID

# Create service account
gcloud iam service-accounts create clinical-ai \
    --display-name="Clinical AI System"

# Grant necessary roles
gcloud projects add-iam-policy-binding YOUR-PROJECT-ID \
    --member=serviceAccount:clinical-ai@YOUR-PROJECT-ID.iam.gserviceaccount.com \
    --role=roles/aiplatform.user

gcloud projects add-iam-policy-binding YOUR-PROJECT-ID \
    --member=serviceAccount:clinical-ai@YOUR-PROJECT-ID.iam.gserviceaccount.com \
    --role=roles/texttospeech.agent

# Create and download key
gcloud iam service-accounts keys create key.json \
    --iam-account=clinical-ai@YOUR-PROJECT-ID.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/key.json
```

---

## Running the System

### Development Server

```bash
# Start FastAPI development server
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Server will be available at: http://localhost:8000
# API docs: http://localhost:8000/docs
# Alternative docs: http://localhost:8000/redoc
```

### Docker Container (Local)

```bash
# Build Docker image
docker build -t clinical-ai:latest .

# Run container
docker run -p 8000:8000 \
    -e OPENAI_API_KEY=$OPENAI_API_KEY \
    -e GEMINI_API_KEY=$GEMINI_API_KEY \
    -e QDRANT_ENDPOINT=$QDRANT_ENDPOINT \
    -e QDRANT_API_KEY=$QDRANT_API_KEY \
    clinical-ai:latest

# Check logs
docker logs -f <container-id>
```

---

## Testing

### Generate Test Data

```bash
# Create synthetic test data (10 patients)
python tests/test_data_generator.py

# Generated files stored in: /tmp/clinical_ai_test_data/
# - patient_PT-01_clinical_note.txt
# - patient_PT-01_vitals.json
# - patient_PT-01_metadata.json
# ... (10 patients total)
```

### Run Integration Tests

```bash
# Run comprehensive test suite
python -m pytest tests/test_integration.py -v

# Expected output:
# - Agent 1 Ingestion Tests: ✓ PASSED
# - Agent 2 Reasoning Tests: ✓ PASSED
# - Agent 3 Feedback Tests: ✓ PASSED
# - Consolidation Tests: ✓ PASSED
# - TTS & Export Tests: ✓ PASSED
# - API Endpoint Tests: ✓ PASSED
```

### Test a Complete Workflow

```bash
# Test end-to-end from data ingestion to report generation
python -c "
import asyncio
from tests.test_data_generator import TestDataGenerator, EndToEndTestSuite

async def main():
    suite = EndToEndTestSuite('/tmp/clinical_ai_test_data')
    results = await suite.run_comprehensive_test()
    print('Test Results:', results)

asyncio.run(main())
"
```

---

## API Documentation

### Health Check

```bash
# Check if system is running
curl http://localhost:8000/health

# Response:
# { "status": "ok", "timestamp": "2024-01-20T10:30:00Z" }
```

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

# Response:
# {
#   "patient_id": "PT-001",
#   "created_at": "2024-01-20T10:30:00Z"
# }
```

### Ingest Medical Data

```bash
curl -X POST http://localhost:8000/api/ingest/multi-modal \
  -H "Content-Type: multipart/form-data" \
  -F "patient_id=PT-001" \
  -F "clinical_note=@clinical_note.txt" \
  -F "vital_signs=@vitals.csv" \
  -F "medical_image=@xray.png"

# Response:
# {
#   "ingestion_id": "ING-123",
#   "status": "processing",
#   "modalities_detected": ["clinical_text", "vital_signs", "medical_imaging"]
# }
```

### Analyze Patient

```bash
curl -X POST http://localhost:8000/api/analyze/patient \
  -H "Content-Type: application/json" \
  -d '{"patient_id": "PT-001"}'

# Response includes:
# {
#   "clinical_summary": {...},
#   "multi_llm_analysis": {
#     "chatgpt_findings": {...},
#     "gemini_findings": {...},
#     "consolidated": {...}
#   },
#   "recommendations": {
#     "medications": [...],
#     "precautions": [...],
#     "checkup_schedule": [...],
#     "disease_trends": {...}
#   },
#   "risk_assessment": {...}
# }
```

### Generate Narrated Report

```bash
curl -X POST http://localhost:8000/api/narrate/report \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "PT-001",
    "language": "en",
    "audience": "patient"
  }'

# Response includes audio and PDF report
```

### Submit Doctor Feedback

```bash
curl -X POST http://localhost:8000/api/feedback/submit \
  -F "patient_id=PT-001" \
  -F "voice_feedback=@feedback.wav" \
  -F "feedback_type=CORRECT"

# Response:
# {
#   "feedback_id": "FB-123",
#   "confidence_adjustment": 0.20,
#   "memory_reinforced": true
# }
```

---

## Deployment to GCP

### Step 1: Setup GCP Project

```bash
# Create GCP project
gcloud projects create clinical-ai-prod --name="Clinical AI Production"

# Set project
gcloud config set project clinical-ai-prod

# Enable required APIs
gcloud services enable \
    run.googleapis.com \
    aiplatform.googleapis.com \
    texttospeech.googleapis.com \
    containerregistry.googleapis.com \
    cloudbuild.googleapis.com
```

### Step 2: Build and Push Docker Image

```bash
# Set variables
PROJECT_ID=$(gcloud config get-value project)
IMAGE_NAME=clinical-ai:latest
REGISTRY=gcr.io

# Build image
docker build -t ${REGISTRY}/${PROJECT_ID}/clinical-ai:latest .

# Push to Container Registry
docker push ${REGISTRY}/${PROJECT_ID}/clinical-ai:latest
```

### Step 3: Deploy to Cloud Run

```bash
# Deploy container
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

# Output will include service URL
# Service URL: https://clinical-ai-xxxxx.run.app
```

### Step 4: Configure Secrets

```bash
# Create secrets for sensitive data
echo -n "$OPENAI_API_KEY" | gcloud secrets create openai-api-key --data-file=-
echo -n "$GEMINI_API_KEY" | gcloud secrets create gemini-api-key --data-file=-

# Grant Cloud Run access to secrets
gcloud secrets add-iam-policy-binding openai-api-key \
    --member=serviceAccount:PROJECT-ID@appspot.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor
```

---

## Kubernetes Deployment

### Step 1: Create Kubernetes Cluster

```bash
# Create GKE cluster
gcloud container clusters create clinical-ai \
    --zone us-central1-a \
    --num-nodes 3 \
    --machine-type n1-standard-2

# Get credentials
gcloud container clusters get-credentials clinical-ai --zone us-central1-a
```

### Step 2: Deploy Application

```bash
# Apply deployment configuration
kubectl apply -f deployment/k8s-deployment.yaml

# Verify deployment
kubectl get deployments
kubectl get pods
kubectl get services

# Check logs
kubectl logs -f deployment/clinical-ai
```

### Step 3: Setup Ingress

```bash
# Create ingress for external access
kubectl apply -f - << EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: clinical-ai-ingress
spec:
  rules:
  - host: clinical-ai.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: clinical-ai-service
            port:
              number: 8000
EOF

# Get Ingress IP
kubectl get ingress
```

---

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI REST API Layer                    │
│  Endpoints: /api/patients, /api/ingest, /api/analyze, etc    │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     Agent Orchestrator                       │
│  Coordinates parallel processing of 14+ specialized agents   │
└─────────────┬─────────────────────────────────────┬──────────┘
              │                                     │
    ┌─────────▼─────────┐              ┌────────────▼────────┐
    │  Ingestion Agent  │              │ Modality-Specific   │
    │  (Agent 1)        │              │ Analysis Agents     │
    │ • Qdrant Similarity│              │ • Vision Agent      │
    │ • Disease Trends  │              │ • Speech Agent      │
    │ • Medication      │              │ • NLP Agent         │
    │   Patterns        │              │ • TimeSeries Agent  │
    │ • Trajectory      │              │ • 10+ others        │
    │   Prediction      │              │                     │
    └─────────┬─────────┘              └────────────┬────────┘
              │                                     │
    ┌─────────▼──────────────────────────────────────▼────────┐
    │              Embedding Agent                            │
    │  Dense (3072-dim) + Sparse (512-dim) Embeddings        │
    └─────────┬──────────────────────────────────────────────┘
              │
    ┌─────────▼──────────────────────────────────────────────┐
    │              Qdrant Vector Database                     │
    │  Hybrid Search (0.6 dense + 0.4 sparse weighting)      │
    │  Temporal Search with Decay Factors                    │
    └──────────────────────────────────────────────────────┘
              │
    ┌─────────▼──────────────────────────────────────────────┐
    │           Multi-LLM Reasoning Layer                    │
    │  • ChatGPT Analysis (5-step reasoning chain)           │
    │  • Gemini Analysis (alternative perspective)          │
    │  • Vertex AI Consolidation                            │
    └──────────────────────────────────────────────────────┘
              │
    ┌─────────▼──────────────────────────────────────────────┐
    │     Safety & Risk Assessment Layer                     │
    │  • Hallucination Detection                             │
    │  • Bias Detection                                      │
    │  • Risk Scoring (Acute/Chronic/Complications)        │
    │  • Mortality & Hospitalization Risk                   │
    └──────────────────────────────────────────────────────┘
              │
    ┌─────────▼──────────────────────────────────────────────┐
    │         Master Consolidation Layer                     │
    │  Generates Clinical Intelligence Summary (CIS)         │
    └──────────────────────────────────────────────────────┘
              │
    ┌─────────▼──────────────────────────────────────────────┐
    │      Output Generation & Doctor Feedback              │
    │  • Multi-language TTS (8 languages)                   │
    │  • PDF Report Generation                              │
    │  • Doctor Feedback Loop (Agent 3)                     │
    │  • Audit Trail Creation                               │
    └──────────────────────────────────────────────────────┘
```

### Data Flow

```
Patient Data (Images, Audio, Text, TimeSeries)
    ↓
[Agent 1] Ingestion + Qdrant Similarity Search
    ↓
[Agents 2-13] Parallel Modality-Specific Analysis
    ↓
[Embedding] Dense & Sparse Embeddings
    ↓
[Memory] Store in Qdrant with Hybrid Indexing
    ↓
[Retrieval] Fetch Similar Cases & Context
    ↓
[Agent 2] Multi-LLM Reasoning (ChatGPT + Gemini)
    ↓
[Safety] Hallucination & Bias Detection
    ↓
[Risk] Multi-factor Risk Assessment
    ↓
[Recommendations] Medication, Precautions, Checkups, Trends
    ↓
[Consolidation] Master CIS Generation
    ↓
[TTS/Export] Multi-language Narration + PDF/JSON Export
    ↓
[Agent 3] Doctor Feedback Loop → Memory Reinforcement
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Qdrant Connection Error

```
Error: Failed to connect to Qdrant
```

**Solution:**
```bash
# Verify Qdrant endpoint is accessible
curl https://your-cluster.europe-west3-0.gcp.cloud.qdrant.io/health

# Check API key
echo $QDRANT_API_KEY

# Test with curl
curl -H "api-key: $QDRANT_API_KEY" \
    https://your-cluster.europe-west3-0.gcp.cloud.qdrant.io/health
```

#### Issue 2: OpenAI API Rate Limiting

```
Error: RateLimitError: rate_limit_exceeded
```

**Solution:**
```python
# Implement exponential backoff
import time
import random

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait_time = 2 ** attempt + random.uniform(0, 1)
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

#### Issue 3: Memory Overflow on Large Embeddings

```
Error: MemoryError
```

**Solution:**
```python
# Process in batches
BATCH_SIZE = 10

for i in range(0, len(patients), BATCH_SIZE):
    batch = patients[i:i+BATCH_SIZE]
    # Process batch
    results = asyncio.run(process_batch(batch))
```

#### Issue 4: GCP Credential Issues

```
Error: Could not automatically determine credentials
```

**Solution:**
```bash
# Set explicit credentials path
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Or authenticate directly
gcloud auth application-default login
```

---

## Production Checklist

Before deploying to production:

- [ ] All API keys stored in secure secrets manager (not in .env)
- [ ] HTTPS enabled on all endpoints
- [ ] Database backups configured
- [ ] Monitoring and alerting setup (Cloud Monitoring)
- [ ] Logging configured (Cloud Logging)
- [ ] Rate limiting implemented on API endpoints
- [ ] HIPAA compliance verified
- [ ] Audit trail logging enabled
- [ ] Database encryption enabled
- [ ] Regular security updates scheduled
- [ ] Disaster recovery plan documented
- [ ] Performance tested with production load
- [ ] Cost optimization reviewed

---

## Support & Resources

- **Documentation**: Full API docs at `/docs` endpoint
- **GitHub Issues**: Report bugs on GitHub
- **Community**: Clinical AI Discord community
- **Email**: support@clinicalai.dev

---

## License

MIT License - See LICENSE file for details

---

## Citation

If you use this system in your research, please cite:

```bibtex
@software{clinical_ai_2024,
  title={Clinical AI Multi-Agent System},
  author={Your Team},
  year={2024},
  url={https://github.com/YOUR-USERNAME/clinical_ai_multi_agent}
}
```

---

**Last Updated**: January 2024
**Version**: 1.0.0
