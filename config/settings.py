"""
Configuration settings for Clinical AI Multi-Agent System
"""
import os
from typing import Dict, Any

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCmoWNMeDk4DWy2MgFWYVcWsx43GIMydzk")

# Qdrant Configuration
QDRANT_CLUSTER_ID = "d7bccdb6-4a7b-4e8b-b425-cf76b3221537"
QDRANT_ENDPOINT = "https://d7bccdb6-4a7b-4e8b-b425-cf76b3221537.europe-west3-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkN2JjY2RiNi00YTdiLTRlOGItYjQyNS1jZjc2YjMyMjE1MzcifQ.Iz8")

# Model Configuration
OPENAI_MODEL = "gpt-4-turbo-preview"
GEMINI_MODEL = "gemini-pro"
VERTEX_AI_MODEL = "gemini-1.5-pro"

# Embedding Configuration
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIMENSION = 3072  # For text-embedding-3-large
SPARSE_EMBEDDING_DIMENSION = 512  # For BM25 sparse vectors

# Vector Store Configuration
VECTOR_STORE = {
    "dense_collection": "clinical_dense_embeddings",
    "sparse_collection": "clinical_sparse_embeddings",
    "hybrid_collection": "clinical_hybrid_search"
}

# Data Modalities
DATA_MODALITIES = {
    "medical_imaging": {
        "types": ["X-ray", "MRI", "CT", "Ultrasound", "Scanned Reports"],
        "format": ["DICOM", "PNG", "JPG", "PDF"],
        "agent": "vision_agent"
    },
    "audio": {
        "types": ["Patient Voice", "Doctor Notes", "Feedback"],
        "format": ["WAV", "MP3", "M4A"],
        "agent": "speech_agent"
    },
    "text": {
        "types": ["Clinical Notes", "Prescriptions", "Discharge Summary"],
        "format": ["TXT", "PDF", "DOCX"],
        "agent": "nlp_agent"
    },
    "timeseries": {
        "types": ["ECG", "Heart Rate", "Blood Pressure", "Oxygen Saturation", "Temperature", "Wearable IoT"],
        "format": ["CSV", "JSON"],
        "agent": "timeseries_agent"
    }
}

# Language Support for TTS
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "hi": "Hindi",
    "pt": "Portuguese",
    "zh": "Chinese (Mandarin)",
    "ja": "Japanese"
}

# Safety & Ethics Configuration
SAFETY_CONFIG = {
    "hallucination_threshold": 0.7,
    "bias_detection": True,
    "evidence_required": True,
    "confidence_threshold": 0.65
}

# Temporal Search Configuration
TEMPORAL_CONFIG = {
    "enable_timeline_analysis": True,
    "time_window_days": 90,
    "similarity_decay": True
}

# Database Configuration (for audit trail and patient records)
DATABASE_CONFIG = {
    "type": "postgresql",  # Change to sqlite for local development
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "clinical_ai"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres")
}

# GCP Configuration
GCP_CONFIG = {
    "project_id": os.getenv("GCP_PROJECT_ID", "your-gcp-project"),
    "region": "us-central1",
    "bucket_name": "clinical-ai-data",
    "vertex_ai_endpoint": "us-central1-aiplatform.googleapis.com"
}

# API Configuration
API_CONFIG = {
    "host": "0.0.0.0",
    "port": int(os.getenv("PORT", 8000)),
    "debug": os.getenv("DEBUG", "False").lower() == "true",
    "workers": int(os.getenv("WORKERS", 4))
}

# Agent Configuration
AGENT_CONFIG = {
    "parallel_processing": True,
    "timeout": 300,  # 5 minutes
    "retry_attempts": 3,
    "batch_size": 10
}

# Report Generation
REPORT_CONFIG = {
    "include_evidence": True,
    "include_reasoning": True,
    "include_confidence_scores": True,
    "include_recommendations": True,
    "pdf_format": True,
    "json_format": True
}
