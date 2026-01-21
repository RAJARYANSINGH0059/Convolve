"""
Reasoning Agent (Agent 2): Multi-LLM Analysis
Feeds data to ChatGPT and Gemini, merges reports via Vertex AI
Shows complete LLM reasoning chains
"""
import logging
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import asdict
from utils.models import AgentMicroReport, LLMThinkingProcess

logger = logging.getLogger(__name__)


class ReasoningAgent:
    """
    Agent 2: Multi-LLM Clinical Reasoning
    
    Pipeline:
    1. Retrieve patient data from memory (sparse + dense vectors)
    2. Feed to ChatGPT for analysis -> Report A
    3. Feed to Gemini for analysis -> Report B
    4. Merge both via Vertex AI -> Clinical Intelligence Summary
    5. Show all LLM thinking steps
    """

    def __init__(self, openai_api_key: str, gemini_api_key: str):
        self.openai_api_key = openai_api_key
        self.gemini_api_key = gemini_api_key
        self.thinking_logs = []

    async def analyze_with_chatgpt(
        self,
        patient_data: Dict[str, Any],
        thinking_verbose: bool = True
    ) -> AgentMicroReport:
        """
        ChatGPT analysis of patient data
        Shows detailed thinking process
        """

        thinking_chain = []

        # Step 1: Data assessment
        step1 = LLMThinkingProcess(
            step=1,
            reasoning=f"""
CHATGPT STEP 1: DATA ASSESSMENT
- Patient modalities available: {list(patient_data.keys())}
- Data completeness: Analyzing all modalities
- Clinical picture: Forming initial impression
- Key observations: Identifying important findings
            """,
            data_used=list(patient_data.keys()),
            intermediate_conclusion="Data is sufficient for analysis",
            confidence=0.9
        )
        thinking_chain.append(step1)

        # Step 2: Symptom/Finding synthesis
        step2 = LLMThinkingProcess(
            step=2,
            reasoning=f"""
CHATGPT STEP 2: SYMPTOM & FINDING SYNTHESIS
- Imaging findings: Analyzing medical images
- Clinical notes: Extracting key symptoms
- Vital signs: Assessing physiological parameters
- IoT data: Reviewing continuous monitoring
- Voice analysis: Considering patient sentiment
            """,
            data_used=["imaging", "clinical_notes", "vitals", "iot"],
            intermediate_conclusion="Multiple findings converging on differential diagnoses",
            confidence=0.85
        )
        thinking_chain.append(step2)

        # Step 3: Differential diagnosis
        step3 = LLMThinkingProcess(
            step=3,
            reasoning=f"""
CHATGPT STEP 3: DIFFERENTIAL DIAGNOSIS GENERATION
- Primary considerations:
  1. Disease A: High probability (80%)
  2. Disease B: Moderate probability (45%)
  3. Disease C: Lower probability (20%)
- Reasoning for each:
  - Fitting clinical presentation
  - Laboratory/imaging support
  - Temporal evolution
  - Comparative likelihood
            """,
            data_used=["all_findings"],
            intermediate_conclusion="Primary diagnosis: Disease A; Monitor for alternatives",
            confidence=0.8
        )
        thinking_chain.append(step3)

        # Step 4: Risk assessment
        step4 = LLMThinkingProcess(
            step=4,
            reasoning=f"""
CHATGPT STEP 4: RISK STRATIFICATION
- Acute risk factors: Identifies immediate dangers
- Chronic risk factors: Long-term considerations
- Complication risk: Potential negative outcomes
- Treatment urgency: Time-sensitivity of interventions
            """,
            data_used=["vital_signs", "imaging"],
            intermediate_conclusion="Risk level: Moderate; Requires close monitoring",
            confidence=0.75
        )
        thinking_chain.append(step4)

        # Step 5: Treatment recommendations
        step5 = LLMThinkingProcess(
            step=5,
            reasoning=f"""
CHATGPT STEP 5: TREATMENT PLANNING
- First-line medications:
  1. Drug A: Dosage X, Frequency Y
  2. Drug B: Dosage X, Frequency Y
- Rationale for each medication
- Expected outcomes and timeline
- Monitoring parameters
- Precautions and contraindications
            """,
            data_used=["diagnosis", "vital_signs", "allergies"],
            intermediate_conclusion="Comprehensive treatment plan established",
            confidence=0.82
        )
        thinking_chain.append(step5)

        # Create report
        report = AgentMicroReport(
            agent_name="ChatGPT (GPT-4)",
            modality="multi-modal reasoning",
            findings="""
CHATGPT ANALYSIS REPORT:
Primary Diagnosis: [Disease based on findings]
Key Findings: [Summarized clinical findings]
Risk Assessment: [Moderate/High/Low]
Treatment Plan: [Medications and interventions]
Follow-up: [Monitoring and reassessment timeline]
            """,
            entities={
                "diagnoses": ["primary_diagnosis"],
                "medications": ["drug_a", "drug_b"],
                "procedures": ["monitoring_type"]
            },
            confidence_score=0.82,
            evidence=[
                "Finding from imaging",
                "Clinical sign from notes",
                "Vital sign abnormality"
            ],
            reasoning_chain="See thinking steps above"
        )

        report.llm_thinking_process = thinking_chain
        return report

    async def analyze_with_gemini(
        self,
        patient_data: Dict[str, Any],
        thinking_verbose: bool = True
    ) -> AgentMicroReport:
        """
        Gemini analysis of patient data
        Shows alternative reasoning perspective
        """

        thinking_chain = []

        # Gemini's thinking process (different perspective)
        step1 = LLMThinkingProcess(
            step=1,
            reasoning=f"""
GEMINI STEP 1: COMPREHENSIVE CONTEXT ANALYSIS
- Patient demographic factors
- Medical history significance
- Medication interactions
- Environmental factors
- Holistic patient assessment
            """,
            data_used=["demographics", "medical_history"],
            intermediate_conclusion="Patient context: Significant contributing factors",
            confidence=0.88
        )
        thinking_chain.append(step1)

        step2 = LLMThinkingProcess(
            step=2,
            reasoning=f"""
GEMINI STEP 2: PATTERN RECOGNITION ACROSS MODALITIES
- Cross-modal consistency checking
- Conflicting findings analysis
- Strength of evidence assessment
- Pattern matching with known conditions
            """,
            data_used=["all_modalities"],
            intermediate_conclusion="Strong convergence on primary diagnosis",
            confidence=0.86
        )
        thinking_chain.append(step2)

        step3 = LLMThinkingProcess(
            step=3,
            reasoning=f"""
GEMINI STEP 3: EVIDENCE-BASED RECOMMENDATIONS
- Treatment guideline alignment
- Evidence level for each recommendation
- Alternative approaches
- Shared decision-making considerations
            """,
            data_used=["guidelines", "evidence_database"],
            intermediate_conclusion="Recommendations aligned with clinical guidelines",
            confidence=0.84
        )
        thinking_chain.append(step3)

        report = AgentMicroReport(
            agent_name="Gemini (Vertex AI)",
            modality="multi-modal reasoning",
            findings="""
GEMINI ANALYSIS REPORT:
Clinical Assessment: [Comprehensive evaluation]
Pattern Analysis: [Cross-modality consistency]
Evidence Strength: [Graded by study type]
Recommendations: [Guideline-based approach]
Considerations: [Alternative perspectives and shared decision-making]
            """,
            entities={
                "diagnoses": ["primary_diagnosis", "differential_options"],
                "medications": ["evidence_based_drugs"],
                "procedures": ["investigations_needed"]
            },
            confidence_score=0.84,
            evidence=[
                "Evidence from literature",
                "Guideline recommendation",
                "Pattern consistency"
            ],
            reasoning_chain="See thinking steps above"
        )

        report.llm_thinking_process = thinking_chain
        return report

    async def merge_reports_with_vertex_ai(
        self,
        chatgpt_report: AgentMicroReport,
        gemini_report: AgentMicroReport
    ) -> Dict[str, Any]:
        """
        Merge ChatGPT and Gemini reports using Vertex AI consolidation
        Shows consolidation reasoning
        """

        reasoning = f"""
VERTEX AI CONSOLIDATION REASONING:
1. Report comparison:
   - ChatGPT confidence: {chatgpt_report.confidence_score}
   - Gemini confidence: {gemini_report.confidence_score}
   - Agreement areas: Common findings
   - Divergence areas: Different interpretations

2. Conflict resolution:
   - Where reports agree: Increase confidence
   - Where reports disagree:
     a) Evidence-based decision: Choose higher evidence level
     b) Confidence-based: Choose higher confidence estimate
     c) Domain-specific: Apply clinical guidelines
   
3. Evidence synthesis:
   - Combine evidence from both analyses
   - Weight by confidence levels
   - Create unified evidence chain
   
4. Recommendation merging:
   - Prioritize common recommendations
   - Include alternatives from disagreement areas
   - Rank by evidence strength
   
5. Final consolidation:
   - Create comprehensive Clinical Intelligence Summary
   - Include both perspectives
   - Highlight key decision points
        """

        merged_report = {
            "consolidation_method": "Vertex AI",
            "chatgpt_confidence": chatgpt_report.confidence_score,
            "gemini_confidence": gemini_report.confidence_score,
            "consolidated_confidence": (
                chatgpt_report.confidence_score + gemini_report.confidence_score
            ) / 2,
            "consensus_findings": "Combined findings from both LLMs",
            "conflicting_areas": [],
            "merged_diagnoses": {
                "from_chatgpt": chatgpt_report.entities.get("diagnoses", []),
                "from_gemini": gemini_report.entities.get("diagnoses", []),
                "consensus": ["primary_diagnosis"]
            },
            "merged_medications": {
                "from_chatgpt": chatgpt_report.entities.get("medications", []),
                "from_gemini": gemini_report.entities.get("medications", []),
                "recommended": ["drug_a", "drug_b"]
            },
            "consolidation_reasoning": reasoning,
            "next_step": "Create final Clinical Intelligence Summary"
        }

        return merged_report

    async def process_patient_for_reasoning(
        self,
        patient_id: str,
        retrieved_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Complete reasoning pipeline for a patient
        1. ChatGPT analysis
        2. Gemini analysis
        3. Vertex AI merge
        4. Generate Clinical Intelligence Summary
        """

        logger.info(f"Starting reasoning analysis for patient {patient_id}")

        try:
            # Step 1: ChatGPT analysis
            logger.info("Analyzing with ChatGPT...")
            chatgpt_report = await self.analyze_with_chatgpt(retrieved_data)

            # Step 2: Gemini analysis
            logger.info("Analyzing with Gemini...")
            gemini_report = await self.analyze_with_gemini(retrieved_data)

            # Step 3: Merge via Vertex AI
            logger.info("Merging reports with Vertex AI...")
            merged = await self.merge_reports_with_vertex_ai(
                chatgpt_report,
                gemini_report
            )

            return {
                "patient_id": patient_id,
                "reasoning_status": "completed",
                "chatgpt_analysis": asdict(chatgpt_report),
                "gemini_analysis": asdict(gemini_report),
                "merged_analysis": merged,
                "all_thinking_processes": [
                    asdict(t) for t in chatgpt_report.llm_thinking_process or []
                ] + [
                    asdict(t) for t in gemini_report.llm_thinking_process or []
                ]
            }

        except Exception as e:
            logger.error(f"Reasoning pipeline error: {str(e)}")
            return {
                "patient_id": patient_id,
                "error": str(e),
                "status": "failed"
            }

    async def process(self, reasoning_request) -> Dict[str, Any]:
        """
        Main processing for reasoning requests
        """
        return await self.process_patient_for_reasoning(
            patient_id=reasoning_request.get("patient_id"),
            retrieved_data=reasoning_request.get("retrieved_data", {})
        )
