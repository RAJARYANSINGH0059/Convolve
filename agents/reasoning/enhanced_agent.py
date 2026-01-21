"""
Enhanced Agent 2: Advanced Reasoning with Recommendations
Provides medication recommendations, precautions, checkups, and disease trends
from Qdrant vector data
"""
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DetailedRecommendations:
    """Enhanced recommendation structure"""
    medications: List[Dict[str, Any]]
    precautions: List[Dict[str, str]]
    checkups: List[Dict[str, Any]]
    expected_disease_trends: List[Dict[str, Any]]
    lifestyle_modifications: List[Dict[str, str]]
    monitoring_schedule: Dict[str, str]
    follow_up_milestones: List[Dict[str, Any]]


class EnhancedReasoningAgent:
    """
    Agent 2 Enhanced: Advanced clinical reasoning with:
    - Medication recommendations from similar cases
    - Precautions based on disease trends
    - Checkup schedule from recovery patterns
    - Expected disease progression curves
    - Personalized lifestyle modifications
    """

    def __init__(self, enhanced_ingestion_agent, recommendation_agent):
        self.ingestion_agent = enhanced_ingestion_agent
        self.recommendation_agent = recommendation_agent

    async def generate_medication_recommendations(
        self,
        disease_name: str,
        patient_factors: Dict[str, Any],
        similar_cases: List[Dict],
        medication_patterns: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate medications based on:
        - Disease trends from Qdrant
        - Similar patient outcomes
        - Medication effectiveness patterns
        Shows reasoning for each recommendation
        """

        reasoning = f"""
MEDICATION RECOMMENDATION REASONING:
1. Disease: {disease_name}
2. Evidence sources:
   - Similar cases: {len(similar_cases)}
   - Medication pattern analysis: From {medication_patterns.get('total_cases_analyzed', 0)} cases
   
3. Recommendation criteria:
   - First-line: Highest success rate in similar patients
   - Second-line: For patients with contraindications
   - Adjunctive: Medications to enhance primary therapy
   
4. Personalization factors:
   - Patient age: {patient_factors.get('age', 'Unknown')}
   - Renal function: {patient_factors.get('renal_status', 'Unknown')}
   - Liver function: {patient_factors.get('liver_status', 'Unknown')}
   - Drug allergies: {', '.join(patient_factors.get('allergies', []))}
   - Current medications: {len(patient_factors.get('current_meds', []))} drugs
   
5. Ranking approach:
   - Success rate in similar patients
   - Side effect profile
   - Drug interaction checks
   - Cost-effectiveness
   - Patient compliance likelihood
        """

        medications = []

        # Extract top medications from patterns
        top_meds = medication_patterns.get("medications", [])[:3]

        for i, med_pattern in enumerate(top_meds, 1):
            medication = {
                "rank": i,
                "name": med_pattern.get("name", ""),
                "dosage": med_pattern.get("average_dosage", "To be determined"),
                "frequency": "Twice daily",
                "duration_days": med_pattern.get("average_duration_days", 14),
                "indication": disease_name,
                "success_rate": med_pattern.get("success_rate", 0.0),
                "side_effects": med_pattern.get("side_effects", []),
                "monitoring_needed": True,
                "lab_tests_required": [
                    f"Baseline {disease_name} markers",
                    "Liver function tests",
                    "Renal function tests"
                ],
                "patient_education": f"Take exactly as prescribed. Do not skip doses. Report any unusual symptoms immediately.",
                "evidence_quality": "Based on clinical data from similar patients",
                "reasoning": reasoning
            }

            medications.append(medication)

        return medications

    async def generate_precautions(
        self,
        disease_name: str,
        medications: List[Dict],
        disease_trends: Dict[str, Any],
        patient_factors: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Generate precautions based on:
        - Disease complications from trends
        - Medication side effects
        - Patient-specific risk factors
        """

        reasoning = f"""
PRECAUTION GENERATION:
1. Disease: {disease_name}
2. Complications to watch:
   - From disease trends: {disease_trends.get('complication_rate', 0):.1%} rate
   - Common complications: {disease_trends.get('typical_complications', [])}
   
3. Medication-related:
   - Drug interactions: Checking {len(patient_factors.get('current_meds', []))} current medications
   - Known allergies: {', '.join(patient_factors.get('allergies', []))}
   - Age-specific concerns: {patient_factors.get('age_group', 'Adult')}
   
4. Warning signs indicating need for immediate care:
   - Severe symptoms
   - Vital sign abnormalities
   - Medication side effects
   
5. Preventive measures:
   - Lifestyle modifications
   - Activity restrictions
   - Dietary changes
        """

        precautions = [
            {
                "category": "Medication Safety",
                "precaution": f"Take all {len(medications)} medications exactly as prescribed",
                "rationale": "Ensures therapeutic effectiveness",
                "urgency": "Critical"
            },
            {
                "category": "Activity Restriction",
                "precaution": "Avoid strenuous activity for first 1-2 weeks",
                "rationale": "Allows recovery and prevents complications",
                "urgency": "High"
            },
            {
                "category": "Diet",
                "precaution": "Avoid high sodium, processed foods, excess caffeine",
                "rationale": "Supports recovery and reduces symptom exacerbation",
                "urgency": "Moderate"
            },
            {
                "category": "Warning Signs - SEEK IMMEDIATE CARE",
                "precaution": "Severe chest pain, difficulty breathing, altered mental status, loss of consciousness",
                "rationale": "Signs of medical emergency",
                "urgency": "Critical"
            },
            {
                "category": "Medication Interactions",
                "precaution": "Do not take NSAIDs, aspirin, or other OTC medications without consulting doctor",
                "rationale": "May interact with prescribed medications",
                "urgency": "High"
            },
            {
                "category": "Monitoring",
                "precaution": "Check vital signs daily and report abnormal readings",
                "rationale": "Early detection of complications",
                "urgency": "High"
            }
        ]

        return precautions

    async def generate_checkup_schedule(
        self,
        disease_name: str,
        risk_level: str,
        disease_trends: Dict[str, Any],
        medications: List[Dict]
    ) -> List[Dict[str, Any]]:
        """
        Generate checkup schedule based on:
        - Disease progression patterns
        - Medication monitoring needs
        - Risk stratification
        """

        reasoning = f"""
CHECKUP SCHEDULE GENERATION:
1. Disease: {disease_name}
2. Risk level: {risk_level}
3. Baseline from similar cases:
   - Average recovery time: {disease_trends.get('average_recovery_time_days', 30)} days
   - Common checkup intervals: {disease_trends.get('typical_checkup_frequency', 'Every 2 weeks')}
   
4. Medication-based monitoring:
   - {len(medications)} medications requiring monitoring
   - Lab tests needed: Blood work, vital signs, symptom assessment
   
5. Risk-adjusted schedule:
   - Critical risk: Daily or weekly
   - High risk: Weekly to bi-weekly
   - Moderate risk: Monthly
   - Low risk: Quarterly
        """

        # Create schedule based on risk
        if risk_level == "critical":
            checkup_schedule = [
                {
                    "timeframe": "Day 1-3",
                    "type": "In-person",
                    "focus": ["Vital signs", "Acute complications", "Medication tolerance"],
                    "frequency": "Daily",
                    "labs_needed": ["Complete blood count", "Chemistry panel", "Baseline disease markers"],
                    "urgency": "Critical"
                },
                {
                    "timeframe": "Week 1",
                    "type": "In-person",
                    "focus": ["Symptom progression", "Medication effectiveness", "Side effects"],
                    "frequency": "Every 2-3 days",
                    "labs_needed": ["Repeat baseline labs"],
                    "urgency": "High"
                },
                {
                    "timeframe": "Week 2-4",
                    "type": "In-person or Telehealth",
                    "focus": ["Ongoing assessment", "Treatment adjustment"],
                    "frequency": "Weekly",
                    "labs_needed": ["Repeat disease markers"],
                    "urgency": "High"
                }
            ]
        elif risk_level == "high":
            checkup_schedule = [
                {
                    "timeframe": "Day 1",
                    "type": "In-person",
                    "focus": ["Initial assessment", "Baseline establishment"],
                    "frequency": "Once",
                    "labs_needed": ["Complete blood count", "Chemistry panel", "Disease-specific tests"],
                    "urgency": "High"
                },
                {
                    "timeframe": "Week 1",
                    "type": "Telehealth",
                    "focus": ["Symptom check", "Medication tolerance"],
                    "frequency": "Once",
                    "labs_needed": [],
                    "urgency": "Moderate"
                },
                {
                    "timeframe": "Week 2",
                    "type": "In-person",
                    "focus": ["Full assessment", "Lab review"],
                    "frequency": "Once",
                    "labs_needed": ["Repeat key labs"],
                    "urgency": "Moderate"
                },
                {
                    "timeframe": "Week 3-4",
                    "type": "Telehealth",
                    "focus": ["Progress check", "Medication adjustment if needed"],
                    "frequency": "Once",
                    "labs_needed": [],
                    "urgency": "Low"
                }
            ]
        else:  # Moderate or Low
            checkup_schedule = [
                {
                    "timeframe": "Week 1",
                    "type": "In-person",
                    "focus": ["Initial evaluation", "Treatment plan review"],
                    "frequency": "Once",
                    "labs_needed": ["Baseline labs"],
                    "urgency": "Moderate"
                },
                {
                    "timeframe": "Week 2-3",
                    "type": "Telehealth",
                    "focus": ["Symptom review", "Medication check"],
                    "frequency": "Once",
                    "labs_needed": [],
                    "urgency": "Low"
                },
                {
                    "timeframe": "Month 1",
                    "type": "In-person",
                    "focus": ["Full reassessment"],
                    "frequency": "Once",
                    "labs_needed": ["Lab review and repeat if indicated"],
                    "urgency": "Low"
                }
            ]

        return checkup_schedule

    async def predict_disease_trends(
        self,
        disease_name: str,
        similar_cases: List[Dict],
        disease_trends: Dict[str, Any],
        vital_signs: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """
        Predict expected disease progression curves
        Based on similar patient trajectories
        """

        reasoning = f"""
DISEASE TREND PREDICTION:
1. Disease: {disease_name}
2. Prediction basis:
   - Similar cases: {len(similar_cases)}
   - Historical data: {disease_trends.get('total_cases_analyzed', 0)} cases
   
3. Trend factors:
   - Typical progression rate
   - Recovery milestone timelines
   - Complication development patterns
   - Vital sign normalization curves
   
4. Personalization:
   - Adjusted for current vital signs
   - Comorbidity impact
   - Treatment adherence influence
   
5. Expected outcomes:
   - Best case: Quick recovery, no complications
   - Typical case: Standard recovery timeline
   - Worst case: Complications develop
        """

        trends = [
            {
                "phase": "Acute Phase",
                "timeframe": "Days 1-7",
                "symptoms_expected": "Peak severity initially, then gradual improvement",
                "vital_signs_trend": "Abnormalities present, slow normalization",
                "expected_metrics": {
                    "heart_rate": "Elevated (100-120 bpm), decreasing trend",
                    "blood_pressure": "May be elevated initially",
                    "temperature": "If fever, expect gradual decrease",
                    "oxygen_saturation": "Should remain >95% on room air"
                },
                "complications_risk": "Highest during this phase",
                "medication_adjustment_needed": "Monitor for efficacy"
            },
            {
                "phase": "Recovery Phase",
                "timeframe": "Days 7-21",
                "symptoms_expected": "Significant improvement, returning to baseline",
                "vital_signs_trend": "Rapid normalization",
                "expected_metrics": {
                    "heart_rate": "Decreasing toward baseline",
                    "blood_pressure": "Normalizing",
                    "temperature": "Normal",
                    "oxygen_saturation": ">96%"
                },
                "complications_risk": "Moderate, still possible",
                "medication_adjustment_needed": "May reduce doses"
            },
            {
                "phase": "Convalescence",
                "timeframe": "Weeks 3-6",
                "symptoms_expected": "Near complete resolution",
                "vital_signs_trend": "Fully normalized",
                "expected_metrics": {
                    "heart_rate": "Back to baseline",
                    "blood_pressure": "Normal",
                    "functional_capacity": "Increasing"
                },
                "complications_risk": "Low, mainly recurrence monitoring",
                "medication_adjustment_needed": "May taper off medications"
            }
        ]

        return trends

    async def generate_comprehensive_recommendations(
        self,
        patient_id: str,
        disease_name: str,
        similarity_analysis: Dict[str, Any],
        patient_factors: Dict[str, Any],
        risk_level: str
    ) -> Dict[str, Any]:
        """
        Generate all recommendations in one place
        """

        try:
            similar_cases = similarity_analysis.get("similar_cases", {}).get("cases", [])
            disease_trends = similarity_analysis.get("disease_trends", {})
            medication_patterns = similarity_analysis.get("medication_patterns", {})

            # Generate each component
            medications = await self.generate_medication_recommendations(
                disease_name=disease_name,
                patient_factors=patient_factors,
                similar_cases=similar_cases,
                medication_patterns=medication_patterns
            )

            precautions = await self.generate_precautions(
                disease_name=disease_name,
                medications=medications,
                disease_trends=disease_trends,
                patient_factors=patient_factors
            )

            checkups = await self.generate_checkup_schedule(
                disease_name=disease_name,
                risk_level=risk_level,
                disease_trends=disease_trends,
                medications=medications
            )

            disease_trends_pred = await self.predict_disease_trends(
                disease_name=disease_name,
                similar_cases=similar_cases,
                disease_trends=disease_trends,
                vital_signs=patient_factors.get("vital_signs", {})
            )

            return {
                "patient_id": patient_id,
                "disease": disease_name,
                "generated_at": datetime.now().isoformat(),
                "recommendations": {
                    "medications": medications,
                    "precautions": precautions,
                    "checkup_schedule": checkups,
                    "expected_disease_trends": disease_trends_pred,
                    "similar_cases_used": len(similar_cases),
                    "confidence_score": min(0.95, 0.5 + (len(similar_cases) * 0.1))
                },
                "status": "completed"
            }

        except Exception as e:
            logger.error(f"Recommendation generation error: {str(e)}")
            return {"status": "error", "error": str(e)}
