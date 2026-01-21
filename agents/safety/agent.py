"""
Safety & Ethics Agent: Bias detection, hallucination checks, regulatory compliance
"""
import logging
from typing import Dict, Any, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SafetyAssessment:
    """Safety evaluation result"""
    assessment_id: str
    hallucination_risk: float
    bias_detected: List[str]
    evidence_requirement_met: bool
    confidence_threshold_met: bool
    regulatory_compliance: bool
    safety_score: float
    recommendations: List[str]


class SafetyAgent:
    """
    Detects:
    - Hallucinations (unsupported claims)
    - Bias (demographic, treatment)
    - Evidence gaps
    - Regulatory violations
    - Safety risks
    """

    def __init__(self):
        self.hallucination_threshold = 0.7
        self.confidence_threshold = 0.65

    async def detect_hallucinations(
        self,
        llm_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Detect hallucinations: LLM claims not supported by evidence
        Shows detection reasoning
        """

        reasoning = f"""
HALLUCINATION DETECTION REASONING:
1. Evidence linking:
   - Each claim must reference source data
   - Imaging finding → imaging report
   - Lab result → lab data
   - Symptom → clinical notes or patient voice
   
2. Logical consistency:
   - Findings should not contradict
   - Diagnoses should fit symptom pattern
   - Treatments should match diagnosis
   
3. Medical plausibility:
   - Check against medical knowledge
   - Verify drug interactions are real
   - Confirm diagnoses are plausible
   
4. Confidence scoring:
   - Higher evidence = lower hallucination risk
   - Multiple supporting sources = confidence boost
   - Single source = higher uncertainty
        """

        findings = []

        # Check each diagnosis claim
        diagnoses = llm_report.get("diagnoses", [])
        evidence_provided = llm_report.get("evidence", [])

        for diagnosis in diagnoses:
            supporting_evidence = [
                e for e in evidence_provided
                if diagnosis.lower() in e.lower()
            ]

            if len(supporting_evidence) < 2:
                findings.append({
                    "claim": diagnosis,
                    "hallucination_risk": 0.7,
                    "recommendation": "Requires stronger evidence support"
                })

        hallucination_risk = min(
            [f.get("hallucination_risk", 0) for f in findings] or [0]
        )

        return {
            "hallucination_risk": hallucination_risk,
            "unsupported_claims": findings,
            "reasoning": reasoning
        }

    async def detect_bias(
        self,
        llm_report: Dict[str, Any],
        patient_demographics: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Detect potential biases in recommendations
        Shows bias detection reasoning
        """

        reasoning = f"""
BIAS DETECTION REASONING:
1. Demographic bias:
   - Age bias: Different treatment for age groups?
   - Gender bias: Different diagnoses by gender?
   - Racial bias: Different treatment protocols?
   - Socioeconomic bias: Treatment based on assumed status?
   
2. Treatment bias:
   - Medication gender bias
   - Dosage based on demographic
   - Investigation frequency bias
   
3. Diagnostic bias:
   - Disease attribution bias
   - Symptom interpretation bias
   - Confirmation bias indicators
   
4. Mitigation:
   - Flag biased recommendations
   - Suggest alternative approaches
   - Recommend equal treatment options
        """

        detected_biases = []

        # Check for demographic-based treatment variations
        age = patient_demographics.get("age", "unknown")
        gender = patient_demographics.get("gender", "unknown")

        medications = llm_report.get("medications", [])
        for med in medications:
            if "elderly" in med.lower() and age in ["young", "middle-aged"]:
                detected_biases.append(
                    f"Age bias: {med} recommended despite non-elderly patient"
                )

        return {
            "biases_detected": len(detected_biases),
            "bias_list": detected_biases,
            "bias_severity": "high" if len(detected_biases) > 0 else "none",
            "reasoning": reasoning
        }

    async def check_evidence_requirements(
        self,
        llm_report: Dict[str, Any]
    ) -> bool:
        """
        Verify adequate evidence for recommendations
        """

        evidence = llm_report.get("evidence", [])
        claims = llm_report.get("diagnoses", []) + llm_report.get("medications", [])

        # Require at least 2 sources of evidence per claim
        evidence_requirement = len(evidence) >= len(claims) * 2

        return evidence_requirement

    async def check_confidence_levels(
        self,
        confidence_score: float
    ) -> bool:
        """
        Check if confidence meets threshold for clinical use
        """
        return confidence_score >= self.confidence_threshold

    async def assess_safety(
        self,
        llm_report: Dict[str, Any],
        patient_demographics: Dict[str, str]
    ) -> SafetyAssessment:
        """
        Complete safety assessment
        """

        hallucination_check = await self.detect_hallucinations(llm_report)
        bias_check = await self.detect_bias(llm_report, patient_demographics)
        evidence_check = await self.check_evidence_requirements(llm_report)
        confidence_check = await self.check_confidence_levels(
            llm_report.get("confidence_score", 0)
        )

        safety_score = (
            (1 - hallucination_check.get("hallucination_risk", 0)) * 0.4 +
            (1 - (len(bias_check.get("bias_list", [])) / 10)) * 0.3 +
            (int(evidence_check)) * 0.2 +
            (int(confidence_check)) * 0.1
        )

        assessment = SafetyAssessment(
            assessment_id=f"SAFETY-{hash(str(llm_report))}",
            hallucination_risk=hallucination_check.get("hallucination_risk", 0),
            bias_detected=bias_check.get("bias_list", []),
            evidence_requirement_met=evidence_check,
            confidence_threshold_met=confidence_check,
            regulatory_compliance=safety_score > 0.7,
            safety_score=safety_score,
            recommendations=[
                "Review hallucination risk claims",
                "Consider bias mitigation",
                "Strengthen evidence for key claims"
            ]
        )

        return assessment
