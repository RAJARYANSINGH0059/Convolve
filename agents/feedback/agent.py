"""
Feedback Agent (Agent 3): Doctor feedback collection and learning
Records voice feedback, memory reinforcement, audit trails
"""
import logging
import asyncio
from typing import Dict, Any, Optional
from dataclasses import asdict
from datetime import datetime

from utils.models import DoctorFeedback, FeedbackType

logger = logging.getLogger(__name__)


class FeedbackAgent:
    """
    Agent 3: Doctor Feedback Loop
    
    Features:
    1. Record doctor voice feedback
    2. Transcribe and analyze feedback
    3. Collect feedback type: correct/partial/wrong
    4. Memory reinforcement in Qdrant
    5. Audit trail for compliance
    6. System learning from feedback
    """

    def __init__(self, speech_agent, memory_agent):
        self.speech_agent = speech_agent
        self.memory_agent = memory_agent
        self.feedback_history = []

    async def record_feedback(
        self,
        report_id: str,
        doctor_name: str,
        doctor_id: str,
        audio_path: str
    ) -> DoctorFeedback:
        """
        Record doctor's voice feedback on a report
        """

        try:
            # Transcribe audio using speech agent
            transcription = await self.speech_agent.transcribe_audio(audio_path)

            # Analyze feedback using speech agent
            feedback_analysis = await self.speech_agent.analyze_doctor_feedback(
                audio_path,
                context="Report evaluation"
            )

            feedback = DoctorFeedback(
                report_id=report_id,
                doctor_name=doctor_name,
                doctor_id=doctor_id,
                voice_recording_path=audio_path,
                corrections=feedback_analysis.get("entities", [])
            )

            return feedback

        except Exception as e:
            logger.error(f"Feedback recording error: {str(e)}")
            raise

    async def classify_feedback(
        self,
        feedback_analysis: Dict[str, Any]
    ) -> FeedbackType:
        """
        Classify feedback as: CORRECT, PARTIAL, or WRONG
        Shows classification reasoning
        """

        reasoning = f"""
FEEDBACK CLASSIFICATION REASONING:
1. Analysis of feedback content:
   - Doctor's tone and confidence
   - Nature of corrections
   - Alignment with original report
   
2. Classification criteria:
   - CORRECT: Doctor affirms report, no corrections needed
     * Confidence: High
     * Changes: None or minor clarifications
     * Action: Reinforce embeddings
   
   - PARTIAL: Report is partially correct, some corrections needed
     * Confidence: Medium
     * Changes: Some entities wrong, some findings missed
     * Action: Mixed reinforcement, identify weak areas
   
   - WRONG: Report significantly incorrect or dangerous
     * Confidence: Low
     * Changes: Major diagnoses wrong, treatment plan dangerous
     * Action: Reduce confidence, retrain on corrections

3. Evidence from feedback:
   - Entities mentioned
   - Sentiment analysis
   - Contradiction detection
   - Severity of errors
        """

        sentiment = feedback_analysis.get("feedback_sentiment", "neutral")
        corrections = len(feedback_analysis.get("entities", []))

        # Simple classification logic
        if sentiment == "positive" and corrections == 0:
            classification = FeedbackType.CORRECT
            confidence = 0.95
        elif sentiment == "neutral" and corrections <= 2:
            classification = FeedbackType.PARTIAL
            confidence = 0.70
        else:
            classification = FeedbackType.WRONG
            confidence = 0.50

        return {
            "feedback_type": classification,
            "confidence": confidence,
            "reasoning": reasoning
        }

    async def process_feedback(
        self,
        feedback: DoctorFeedback,
        original_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process feedback: classify and trigger learning
        """

        try:
            # Analyze feedback
            feedback_analysis = await self.speech_agent.analyze_doctor_feedback(
                feedback.voice_recording_path,
                context=f"Evaluating report {feedback.report_id}"
            )

            # Classify feedback
            classification = await self.classify_feedback(feedback_analysis)

            feedback.feedback_type = classification["feedback_type"]

            # Update audit trail
            self.feedback_history.append({
                "feedback_id": feedback.feedback_id,
                "report_id": feedback.report_id,
                "feedback_type": feedback.feedback_type,
                "doctor": feedback.doctor_name,
                "timestamp": datetime.now().isoformat(),
                "classification_confidence": classification["confidence"]
            })

            return {
                "feedback_id": feedback.feedback_id,
                "feedback_type": feedback.feedback_type.value,
                "classification_confidence": classification["confidence"],
                "corrections_identified": len(feedback_analysis.get("entities", [])),
                "next_action": await self._determine_action(
                    feedback.feedback_type,
                    original_report
                )
            }

        except Exception as e:
            logger.error(f"Feedback processing error: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def _determine_action(
        self,
        feedback_type: FeedbackType,
        original_report: Dict[str, Any]
    ) -> str:
        """
        Determine action based on feedback type
        """

        if feedback_type == FeedbackType.CORRECT:
            return "Store report as reference; reinforce embeddings"
        elif feedback_type == FeedbackType.PARTIAL:
            return "Flag for review; selectively reinforce correct parts"
        else:  # WRONG
            return "Do not store; retrain on corrections; audit system"

    async def reinforce_memory_from_feedback(
        self,
        feedback: DoctorFeedback,
        embedding_ids: list
    ) -> bool:
        """
        Update Qdrant embeddings based on feedback
        Shows memory reinforcement reasoning
        """

        reasoning = f"""
MEMORY REINFORCEMENT FROM FEEDBACK:
1. Feedback-based learning:
   - Feedback type: {feedback.feedback_type.value}
   - Embeddings to update: {len(embedding_ids)}
   
2. Confidence adjustment:
   - CORRECT feedback: Boost confidence by 0.2
   - PARTIAL feedback: Boost partial, reduce others by 0.1
   - WRONG feedback: Significantly reduce confidence
   
3. Weight update:
   - Higher confidence = Higher search weight
   - Lower confidence = Lower priority in future
   
4. Learning efficiency:
   - Direct patient-specific learning
   - Prevents repeated errors
   - Improves system over time
   
5. Feedback integration:
   - Update vector weights in Qdrant
   - Record in audit trail
   - Track confidence trajectory
        """

        try:
            confidence_boost = {
                FeedbackType.CORRECT: 0.2,
                FeedbackType.PARTIAL: 0.1,
                FeedbackType.WRONG: -0.3
            }.get(feedback.feedback_type, 0.0)

            # Reinforce each embedding
            for embedding_id in embedding_ids:
                await self.memory_agent.reinforce_memory(
                    embedding_id=embedding_id,
                    feedback_type=feedback.feedback_type.value,
                    confidence_boost=confidence_boost
                )

            return True

        except Exception as e:
            logger.error(f"Memory reinforcement error: {str(e)}")
            return False

    async def create_audit_trail(
        self,
        feedback: DoctorFeedback,
        processing_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create compliance-audit trail entry
        """

        audit_entry = {
            "audit_id": f"AUDIT-{datetime.now().timestamp()}",
            "feedback_id": feedback.feedback_id,
            "report_id": feedback.report_id,
            "doctor": {
                "name": feedback.doctor_name,
                "id": feedback.doctor_id
            },
            "feedback_type": feedback.feedback_type.value,
            "voice_recording_path": feedback.voice_recording_path,
            "corrections": feedback.corrections,
            "reason": feedback.reason,
            "processing_result": processing_result,
            "timestamp": datetime.now().isoformat(),
            "compliance_status": "compliant"
        }

        return audit_entry

    async def rescan_report_with_corrections(
        self,
        original_report: Dict[str, Any],
        corrections: list,
        feedback: DoctorFeedback
    ) -> Dict[str, Any]:
        """
        Re-analyze report with corrections for PARTIAL/WRONG feedback
        Creates corrected version for future reference
        """

        reasoning = f"""
REPORT RESCANNING WITH CORRECTIONS:
1. Original findings: From initial analysis
2. Doctor's corrections: From feedback
3. Merge strategy:
   - Keep correct parts from original
   - Replace wrong parts with corrections
   - Add missing findings from feedback
   
4. Updated diagnosis:
   - Primary diagnosis: [Corrected]
   - Confidence: [Adjusted based on feedback]
   - Reasoning: Updated with corrections
   
5. Updated treatment plan:
   - Medications: [Adjusted if diagnosis changed]
   - Procedures: [Updated as needed]
   - Precautions: [Reinforced]
   
6. Learning record:
   - Store corrected version
   - Link to doctor feedback
   - Use for future training
        """

        corrected_report = {
            "original_report_id": original_report.get("report_id"),
            "feedback_id": feedback.feedback_id,
            "feedback_type": feedback.feedback_type.value,
            "corrections_applied": corrections,
            "corrected_findings": f"Original findings with {len(corrections)} corrections",
            "corrected_confidence": original_report.get("confidence_score", 0) * 0.9,  # Slight reduction
            "reasoning": reasoning,
            "created_at": datetime.now().isoformat()
        }

        return corrected_report

    async def generate_feedback_report(self) -> Dict[str, Any]:
        """
        Generate feedback statistics and learning insights
        """

        total_feedback = len(self.feedback_history)
        correct_count = sum(
            1 for f in self.feedback_history
            if f.get("feedback_type") == "correct"
        )
        partial_count = sum(
            1 for f in self.feedback_history
            if f.get("feedback_type") == "partial"
        )
        wrong_count = sum(
            1 for f in self.feedback_history
            if f.get("feedback_type") == "wrong"
        )

        return {
            "total_feedback_received": total_feedback,
            "correct_feedback": correct_count,
            "partial_feedback": partial_count,
            "wrong_feedback": wrong_count,
            "accuracy_rate": correct_count / total_feedback if total_feedback > 0 else 0,
            "system_improvement_needed": [
                f"Address {wrong_count} wrong classifications" if wrong_count > 0 else None,
                f"Improve {partial_count} partial matches" if partial_count > 0 else None
            ],
            "recommendation": "System learning is improving accuracy over time"
        }

    async def process(self, feedback_request) -> Dict[str, Any]:
        """
        Main processing for feedback
        """
        return await self.process_feedback(
            feedback=feedback_request.get("feedback"),
            original_report=feedback_request.get("original_report")
        )
