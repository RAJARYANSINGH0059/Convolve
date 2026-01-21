"""
Recommendation Agent: Care planning and treatment recommendations
Generates actionable clinical recommendations
"""
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RecommendationAgent:
    """
    Generates evidence-based clinical recommendations:
    - Medication recommendations with doses
    - Investigations/diagnostics needed
    - Monitoring parameters
    - Lifestyle modifications
    - Follow-up scheduling
    - Precautions and warnings
    """

    def __init__(self):
        self.evidence_levels = {
            "level_A": "High-quality randomized controlled trial data",
            "level_B": "Well-conducted case-control or cohort studies",
            "level_C": "Expert opinion or case reports",
            "level_D": "Observational data or clinical judgment"
        }

    async def generate_medication_recommendations(
        self,
        diagnoses: List[str],
        patient_factors: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate medication recommendations with evidence levels
        Shows reasoning for medication selection
        """

        reasoning = f"""
MEDICATION RECOMMENDATION REASONING:
1. Diagnosis-based selection:
   - For each diagnosis, identify first-line medications
   - Consider guideline recommendations
   - Check evidence quality
   
2. Patient-specific factors:
   - Renal function: Adjust doses
   - Liver function: Modify metabolism
   - Drug interactions: Screen for conflicts
   - Age considerations: Elderly dosing
   - Pregnancy: Avoid teratogens
   - Allergies: Avoid contraindicated drugs
   
3. Dosage selection:
   - Standard dose: For most patients
   - Lower dose: For elderly, renal/liver disease
   - Higher dose: For severe disease (if safe)
   - Titration schedule: Gradual increase if needed
   
4. Monitoring:
   - Lab tests: Drug levels, liver/kidney function
   - Clinical response: Symptom improvement timeline
   - Side effects: What to watch for
   - Follow-up: When to reassess
        """

        recommendations = [
            {
                "medication_name": "Example Drug",
                "indication": diagnoses[0] if diagnoses else "To be determined",
                "dosage": "500 mg",
                "frequency": "twice daily",
                "route": "oral",
                "duration": "10 days",
                "evidence_level": "level_A",
                "rationale": "First-line therapy for indicated condition",
                "monitoring": [
                    "Clinical response after 3 days",
                    "Liver function tests if prolonged use"
                ],
                "interactions": [
                    "Avoid with NSAIDs",
                    "Check for warfarin interaction"
                ],
                "precautions": [
                    "Take with food if GI upset",
                    "Avoid driving if dizziness occurs"
                ],
                "side_effects": [
                    "Mild nausea (common)",
                    "Rare: Liver toxicity (monitor LFTs)"
                ]
            }
        ]

        return recommendations

    async def recommend_investigations(
        self,
        diagnoses: List[str],
        findings: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Recommend diagnostic investigations
        Shows investigation selection reasoning
        """

        reasoning = f"""
INVESTIGATION RECOMMENDATION:
1. Confirm diagnosis:
   - Imaging: X-ray, CT, MRI
   - Laboratory: CBC, metabolic panel, specialty labs
   - Functional: ECG, EEG, PFT
   
2. Assess severity:
   - Baseline measurements
   - Organ function assessment
   - Disease extent evaluation
   
3. Risk stratification:
   - Biomarkers for prognosis
   - Scores for risk assessment
   - Genetic testing if indicated
   
4. Drug monitoring:
   - Baseline before starting medications
   - Periodic monitoring during treatment
   - Follow-up confirmation of effectiveness
        """

        investigations = []

        # Example investigations
        if "cardiovascular" in str(diagnoses).lower():
            investigations.extend([
                {
                    "test_name": "Electrocardiogram (ECG)",
                    "purpose": "Assess cardiac rhythm and conduction",
                    "timing": "Immediately",
                    "urgency": "high"
                },
                {
                    "test_name": "Troponin levels",
                    "purpose": "Rule out acute myocardial infarction",
                    "timing": "Immediately",
                    "urgency": "high"
                }
            ])

        if "infection" in str(diagnoses).lower():
            investigations.extend([
                {
                    "test_name": "Blood cultures",
                    "purpose": "Identify causative organism",
                    "timing": "Before antibiotics if possible",
                    "urgency": "high"
                },
                {
                    "test_name": "Complete Blood Count",
                    "purpose": "Assess infection severity",
                    "timing": "Immediately",
                    "urgency": "high"
                }
            ])

        return investigations

    async def recommend_monitoring(
        self,
        diagnoses: List[str],
        treatments: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Recommend monitoring parameters and schedule
        """

        monitoring_plan = [
            {
                "parameter": "Vital signs",
                "frequency": "Every 4-8 hours initially",
                "target": "Stable, improving trend",
                "action_if_abnormal": "Notify physician"
            },
            {
                "parameter": "Symptoms",
                "frequency": "Daily assessment",
                "target": "Improving",
                "action_if_abnormal": "Adjust medications"
            }
        ]

        return monitoring_plan

    async def recommend_lifestyle_modifications(
        self,
        diagnoses: List[str],
        risk_factors: List[str]
    ) -> List[Dict[str, str]]:
        """
        Recommend lifestyle changes
        """

        modifications = []

        if "cardiovascular" in str(diagnoses).lower():
            modifications.extend([
                {
                    "modification": "Dietary changes",
                    "specifics": "Low sodium (< 2g/day), DASH diet",
                    "goal": "Reduce blood pressure, improve lipid profile"
                },
                {
                    "modification": "Exercise",
                    "specifics": "30 min moderate activity 5 days/week",
                    "goal": "Improve cardiovascular fitness"
                }
            ])

        if "diabetes" in str(diagnoses).lower():
            modifications.extend([
                {
                    "modification": "Carbohydrate management",
                    "specifics": "Low glycemic index foods",
                    "goal": "Better glucose control"
                },
                {
                    "modification": "Regular blood glucose monitoring",
                    "specifics": "Self-monitoring as directed",
                    "goal": "Track control and adjust medications"
                }
            ])

        return modifications

    async def generate_followup_plan(
        self,
        diagnoses: List[str],
        treatments: List[str],
        risk_level: str
    ) -> Dict[str, Any]:
        """
        Generate follow-up schedule
        """

        followup_timeline = {
            "immediate": [],
            "one_week": [],
            "one_month": [],
            "three_months": []
        }

        # Critical cases: urgent follow-up
        if risk_level == "critical":
            followup_timeline["immediate"] = [
                "Phone call check-in",
                "Lab work if needed"
            ]
            followup_timeline["one_week"] = [
                "In-person evaluation"
            ]

        # Standard cases
        followup_timeline["one_month"] = [
            "Follow-up appointment",
            "Repeat relevant labs"
        ]

        followup_timeline["three_months"] = [
            "Reassess treatment response",
            "Adjust medications if needed"
        ]

        return {
            "followup_schedule": followup_timeline,
            "next_appointment": (
                datetime.now() + timedelta(days=7)
            ).isoformat(),
            "emergency_criteria": [
                "Severe chest pain",
                "Shortness of breath",
                "Loss of consciousness"
            ],
            "contact_instructions": "Call immediately if emergency criteria present"
        }

    async def generate_precautions(
        self,
        medications: List[str],
        diagnoses: List[str],
        patient_factors: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Generate safety precautions and warnings
        """

        precautions = [
            {
                "category": "Medication safety",
                "precaution": "Take medications exactly as prescribed",
                "rationale": "Ensure therapeutic effect and minimize side effects"
            },
            {
                "category": "Side effect awareness",
                "precaution": "Report persistent side effects",
                "rationale": "May require medication adjustment"
            },
            {
                "category": "Drug interactions",
                "precaution": "Inform all providers of medications",
                "rationale": "Prevent dangerous interactions"
            },
            {
                "category": "Allergies",
                "precaution": "Wear medical alert bracelet if appropriate",
                "rationale": "Emergency responders need allergy information"
            }
        ]

        if "driving" not in str(patient_factors).lower():
            precautions.append({
                "category": "Activity restriction",
                "precaution": "Avoid driving if dizziness occurs",
                "rationale": "Safety risk"
            })

        return precautions

    async def generate_comprehensive_plan(
        self,
        patient_id: str,
        diagnoses: List[str],
        vital_signs: Dict[str, float],
        risk_assessment: Dict[str, Any],
        patient_factors: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate complete care plan
        """

        medications = await self.generate_medication_recommendations(
            diagnoses,
            patient_factors
        )

        investigations = await self.recommend_investigations(
            diagnoses,
            vital_signs
        )

        monitoring = await self.recommend_monitoring(
            diagnoses,
            [m["medication_name"] for m in medications]
        )

        lifestyle = await self.recommend_lifestyle_modifications(
            diagnoses,
            patient_factors.get("risk_factors", [])
        )

        followup = await self.generate_followup_plan(
            diagnoses,
            [m["medication_name"] for m in medications],
            risk_assessment.get("risk_level", "moderate")
        )

        precautions = await self.generate_precautions(
            [m["medication_name"] for m in medications],
            diagnoses,
            patient_factors
        )

        return {
            "care_plan_id": f"PLAN-{patient_id}-{datetime.now().timestamp()}",
            "patient_id": patient_id,
            "diagnoses": diagnoses,
            "medications": medications,
            "investigations": investigations,
            "monitoring_plan": monitoring,
            "lifestyle_modifications": lifestyle,
            "followup_schedule": followup,
            "precautions": precautions,
            "created_at": datetime.now().isoformat(),
            "valid_until": (
                datetime.now() + timedelta(days=90)
            ).isoformat()
        }

    async def process(self, request) -> Dict[str, Any]:
        """
        Main processing for recommendations
        """
        return await self.generate_comprehensive_plan(
            patient_id=request.get("patient_id"),
            diagnoses=request.get("diagnoses", []),
            vital_signs=request.get("vital_signs", {}),
            risk_assessment=request.get("risk_assessment", {}),
            patient_factors=request.get("patient_factors", {})
        )
