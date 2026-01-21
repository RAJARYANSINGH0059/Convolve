"""
FastAPI Application: Main entry point for clinical AI system
Endpoints for ingestion, analysis, feedback, and report generation
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import uuid
from datetime import datetime
import asyncio
import os

# Import agents
from agents.ingestion.agent import IngestionAgent
from agents.vision.agent import VisionAgent
from agents.speech.agent import SpeechAgent
from agents.nlp.agent import NLPAgent
from agents.timeseries.agent import TimeSeriesAgent
from agents.embedding.agent import EmbeddingAgent
from agents.memory.agent import MemoryAgent
from agents.retrieval.agent import RetrievalAgent
from agents.reasoning.agent import ReasoningAgent
from agents.safety.agent import SafetyAgent
from agents.risk_intelligence.agent import RiskIntelligenceAgent
from agents.recommendation.agent import RecommendationAgent
from agents.feedback.agent import FeedbackAgent

from consolidation.layer import MasterConsolidationLayer
from utils.tts_narrator import TextToSpeechReportNarrator
from utils.models import PatientRecord, MedicalData, DoctorFeedback
from config.settings import QDRANT_ENDPOINT, QDRANT_API_KEY, QDRANT_CLUSTER_ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Clinical AI Multi-Agent System",
    description="Parallel multi-agent clinical intelligence platform",
    version="1.0.0"
)

# Mount frontend static files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Initialize all agents
ingestion_agent = IngestionAgent()
vision_agent = VisionAgent()
speech_agent = SpeechAgent()
nlp_agent = NLPAgent()
timeseries_agent = TimeSeriesAgent()
embedding_agent = EmbeddingAgent()
memory_agent = MemoryAgent({
    "endpoint": QDRANT_ENDPOINT,
    "api_key": QDRANT_API_KEY,
    "cluster_id": QDRANT_CLUSTER_ID
})
retrieval_agent = RetrievalAgent(memory_agent)
reasoning_agent = ReasoningAgent("", "")
safety_agent = SafetyAgent()
risk_intelligence_agent = RiskIntelligenceAgent()
recommendation_agent = RecommendationAgent()
feedback_agent = FeedbackAgent(speech_agent, memory_agent)
consolidation_layer = MasterConsolidationLayer()
tts_narrator = TextToSpeechReportNarrator("your-gcp-project")

# Register handlers
ingestion_agent.register_handler("medical_imaging", vision_agent)
ingestion_agent.register_handler("audio", speech_agent)
ingestion_agent.register_handler("text", nlp_agent)
ingestion_agent.register_handler("timeseries", timeseries_agent)

# Request/Response Models
class PatientCreateRequest(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    contact: str
    medical_history: Optional[str] = ""

class DataIngestionRequest(BaseModel):
    patient_id: str
    data_items: List[Dict[str, Any]]

class ReportNarrationRequest(BaseModel):
    report_id: str
    language: str
    narrative_type: str = "patient_friendly"

class FeedbackSubmissionRequest(BaseModel):
    report_id: str
    doctor_name: str
    doctor_id: str
    audio_path: str
    feedback_type: str

# API Endpoints

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents_initialized": True
    }

@app.post("/api/patients/create")
async def create_patient(request: PatientCreateRequest) -> Dict[str, Any]:
    """
    Create new patient record
    Returns patient ID for future references
    """
    try:
        patient = PatientRecord(
            first_name=request.first_name,
            last_name=request.last_name,
            date_of_birth=request.date_of_birth,
            gender=request.gender,
            contact=request.contact,
            medical_history=request.medical_history
        )
        
        return {
            "status": "created",
            "patient_id": patient.patient_id,
            "patient_data": patient.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/ingest/multi-modal")
async def ingest_medical_data(request: DataIngestionRequest) -> Dict[str, Any]:
    """
    Ingest medical data across all modalities
    Coordinates parallel processing of images, audio, text, and time-series
    """
    try:
        logger.info(f"Ingesting {len(request.data_items)} items for patient {request.patient_id}")
        
        result = await ingestion_agent.coordinate_parallel_ingestion(
            patient_id=request.patient_id,
            data_items=request.data_items
        )
        
        return {
            "status": "ingestion_completed",
            "patient_id": request.patient_id,
            **result
        }
    except Exception as e:
        logger.error(f"Ingestion error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/analyze/patient")
async def analyze_patient(patient_id: str) -> Dict[str, Any]:
    """
    Complete multi-agent analysis pipeline for patient
    1. Retrieves all data from memory
    2. Feeds to ChatGPT and Gemini
    3. Merges via Vertex AI
    4. Performs safety checks
    5. Generates recommendations
    6. Produces consolidated report
    """
    try:
        logger.info(f"Starting comprehensive analysis for patient {patient_id}")
        
        # Retrieve patient data
        retrieval_result = await retrieval_agent.retrieve_for_reasoning(
            patient_id=patient_id,
            clinical_context="Comprehensive analysis",
            required_modalities=["medical_imaging", "audio", "text", "timeseries"]
        )
        
        # Multi-LLM reasoning
        reasoning_result = await reasoning_agent.process_patient_for_reasoning(
            patient_id=patient_id,
            retrieved_data=retrieval_result
        )
        
        # Safety assessment
        safety_result = await safety_agent.assess_safety(
            reasoning_result.get("merged_analysis", {}),
            {"age": "unknown", "gender": "unknown"}
        )
        
        # Risk assessment
        risk_result = await risk_intelligence_agent.assess_comprehensive_risk(
            patient_id=patient_id,
            vital_signs={},
            lab_values={},
            clinical_findings={},
            patient_history={}
        )
        
        # Generate recommendations
        recommendations = await recommendation_agent.generate_comprehensive_plan(
            patient_id=patient_id,
            diagnoses=[reasoning_result.get("merged_analysis", {}).get("primary_diagnosis", "Unknown")],
            vital_signs={},
            risk_assessment={"risk_level": risk_result.risk_level},
            patient_factors={}
        )
        
        # Master consolidation
        consolidation_result = await consolidation_layer.process_all_agents({
            "patient_id": patient_id,
            "patient_name": "Patient Name",
            "voice_analysis": retrieval_result.get("voice_analysis", {}),
            "nlp_analysis": retrieval_result.get("nlp_analysis", {}),
            "vision_results": retrieval_result.get("modality_data", {}).get("medical_imaging", []),
            "timeseries_results": retrieval_result.get("modality_data", {}).get("timeseries", []),
            "chatgpt_report": reasoning_result.get("chatgpt_analysis", {}),
            "gemini_report": reasoning_result.get("gemini_analysis", {}),
            "risk_assessment": risk_result.__dict__,
            "recommendations": recommendations,
            "safety_assessment": safety_result.__dict__
        })
        
        return {
            "status": "analysis_completed",
            "patient_id": patient_id,
            "analysis_result": consolidation_result,
            "ready_for_narration": True
        }
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/narrate/report")
async def narrate_report(request: ReportNarrationRequest) -> Dict[str, Any]:
    """
    Generate narrated report in selected language
    Supports patient-friendly and medical professional narrations
    """
    try:
        # In production: Retrieve consolidated report from database
        consolidated_report = {}
        clinical_summary = {}
        
        narration_result = await tts_narrator.generate_narrated_report(
            consolidated_report=consolidated_report,
            clinical_summary=clinical_summary,
            selected_language=request.language,
            narrative_type=request.narrative_type
        )
        
        return {
            "status": "narration_completed",
            "report_id": request.report_id,
            **narration_result
        }
        
    except Exception as e:
        logger.error(f"Narration error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/feedback/submit")
async def submit_doctor_feedback(request: FeedbackSubmissionRequest) -> Dict[str, Any]:
    """
    Submit doctor feedback on generated report
    Agent 3: Doctor Feedback Loop
    """
    try:
        # Record feedback
        feedback = await feedback_agent.record_feedback(
            report_id=request.report_id,
            doctor_name=request.doctor_name,
            doctor_id=request.doctor_id,
            audio_path=request.audio_path
        )
        
        # Process feedback
        processing_result = await feedback_agent.process_feedback(
            feedback=feedback,
            original_report={}  # Would be retrieved from database
        )
        
        # Create audit trail
        audit_entry = await feedback_agent.create_audit_trail(
            feedback=feedback,
            processing_result=processing_result
        )
        
        return {
            "status": "feedback_processed",
            "feedback_id": feedback.feedback_id,
            "feedback_type": feedback.feedback_type.value,
            "processing_result": processing_result,
            "audit_recorded": True
        }
        
    except Exception as e:
        logger.error(f"Feedback error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/reports/patient/{patient_id}")
async def get_patient_reports(patient_id: str) -> Dict[str, Any]:
    """
    Retrieve all reports for a patient
    """
    try:
        # In production: Query database
        reports = []
        
        return {
            "patient_id": patient_id,
            "total_reports": len(reports),
            "reports": reports
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/audit/trail/{patient_id}")
async def get_audit_trail(patient_id: str) -> Dict[str, Any]:
    """
    Retrieve audit trail for patient (compliance)
    """
    try:
        audit_trail = memory_agent.get_audit_trail(patient_id)
        
        return {
            "patient_id": patient_id,
            "audit_entries": len(audit_trail),
            "trail": audit_trail
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/export/report/{report_id}")
async def export_report(report_id: str, format: str = "pdf") -> Dict[str, Any]:
    """
    Export report in PDF or JSON format
    """
    try:
        # In production: Retrieve report and generate export
        
        if format == "pdf":
            output_path = f"/tmp/report_{report_id}.pdf"
            result = await tts_narrator.create_pdf_report({}, output_path)
        else:
            result = {"status": "exported", "format": "json"}
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
async def root():
    """Serve dashboard HTML"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "index.html")
    if os.path.exists(frontend_path):
        with open(frontend_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    else:
        # Fallback if HTML not found
        return {
            "name": "Clinical AI Multi-Agent System",
            "version": "1.0.0",
            "description": "Parallel multi-agent architecture for clinical intelligence",
            "status": "API is running but frontend not found",
            "api_docs": "Visit http://localhost:8000/docs for API documentation"
        }

# Run with: uvicorn api.main:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
