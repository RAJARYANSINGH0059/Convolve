"""
Risk Intelligence Agent: Multi-factor risk scoring and clinical risk assessment
"""
import logging
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class RiskAssessment:
    """Risk evaluation result"""
    patient_id: str
    overall_risk_score: float  # 0-1
    risk_level: str  # critical, high, moderate, low
    acute_risks: List[Dict[str, Any]]
    chronic_risks: List[Dict[str, Any]]
    complication_risks: List[Dict[str, Any]]
    mortality_risk: float
    hospitalization_risk: float
    interventions_needed: List[str]


class RiskIntelligenceAgent:
    """
    Multi-factor risk assessment and stratification
    Evaluates:
    - Acute medical emergencies
    - Chronic disease progression
    - Complication risks
    - Mortality indicators
    - Treatment-related risks
    """

    def __init__(self):
        self.risk_factors = {
            "cardiovascular": {
                "hypertension": 0.3,
                "high_cholesterol": 0.25,
                "diabetes": 0.35,
                "smoking": 0.4,
                "age_over_65": 0.2
            },
            "respiratory": {
                "low_oxygen": 0.6,
                "tachypnea": 0.4,
                "chronic_lung_disease": 0.3,
                "infection_risk": 0.45
            },
            "neurological": {
                "altered_mental_status": 0.7,
                "seizures": 0.6,
                "stroke_risk": 0.5
            }
        }

    async def assess_acute_risks(
        self,
        vital_signs: Dict[str, float],
        clinical_findings: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Assess immediate life-threatening risks
        Shows acute risk reasoning
        """

        reasoning = f"""
ACUTE RISK ASSESSMENT:
1. Vital sign abnormalities:
   - HR > 120 or < 40 → tachycardia/bradycardia risk
   - SBP > 180 or < 90 → hypertensive crisis/shock risk
   - RR > 25 or < 10 → respiratory failure risk
   - SpO2 < 90% → hypoxia risk
   - Temp > 38.5°C or < 35°C → sepsis/hypothermia
   
2. Clinical red flags:
   - Altered mental status → urgent intervention
   - Severe pain → possible emergent condition
   - Acute dyspnea → possible pulmonary embolism
   - Chest pain → possible MI
   - Severe headache → possible stroke
   
3. Risk hierarchy:
   - Critical (needs emergency intervention)
   - High (urgent evaluation needed)
   - Moderate (prompt evaluation)
   - Low (routine care)
        """

        acute_risks = []

        # Check vital signs
        hr = vital_signs.get("heart_rate", 70)
        if hr > 120:
            acute_risks.append({
                "condition": "Tachycardia",
                "severity": "high",
                "value": hr,
                "action": "Assess cause urgently"
            })

        # Check SpO2
        spo2 = vital_signs.get("oxygen_saturation", 98)
        if spo2 < 90:
            acute_risks.append({
                "condition": "Hypoxia",
                "severity": "critical",
                "value": spo2,
                "action": "Supplemental oxygen, respiratory support"
            })

        # Check BP
        sbp = vital_signs.get("systolic_bp", 120)
        if sbp > 180:
            acute_risks.append({
                "condition": "Hypertensive crisis",
                "severity": "high",
                "value": sbp,
                "action": "Urgent medication adjustment"
            })

        return acute_risks

    async def assess_chronic_risks(
        self,
        patient_history: Dict[str, Any],
        current_conditions: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Assess chronic disease progression and management risks
        """

        chronic_risks = []

        # Evaluate disease duration and control
        for condition in current_conditions:
            risk_factor = self.risk_factors.get("cardiovascular", {}).get(
                condition.lower(), 0.2
            )

            chronic_risks.append({
                "condition": condition,
                "risk_score": risk_factor,
                "progression_risk": "monitor",
                "management_priority": "continue_current_plan"
            })

        return chronic_risks

    async def assess_complication_risks(
        self,
        diagnoses: List[str],
        medications: List[str],
        patient_factors: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Assess risks of treatment-related complications
        """

        complication_risks = []

        # Drug-drug interactions
        if len(medications) > 3:
            complication_risks.append({
                "type": "Polypharmacy",
                "risk_level": "moderate",
                "description": "Multiple medications increase interaction risk",
                "mitigation": "Regular medication review"
            })

        # Age-related complications
        age = patient_factors.get("age", 50)
        if age > 65:
            complication_risks.append({
                "type": "Age-related",
                "risk_level": "moderate",
                "description": "Increased fall risk, reduced drug metabolism",
                "mitigation": "Adjust dosages, fall prevention"
            })

        return complication_risks

    async def calculate_mortality_risk(
        self,
        vital_signs: Dict[str, float],
        lab_values: Dict[str, float],
        diagnoses: List[str]
    ) -> float:
        """
        Estimate mortality risk
        Shows mortality risk calculation reasoning
        """

        reasoning = f"""
MORTALITY RISK CALCULATION:
1. Physiological parameters:
   - SpO2 < 90%: High mortality predictor
   - HR > 130: Cardiac stress
   - SBP < 90: Shock state
   - Temperature extremes
   
2. Laboratory markers:
   - Lactate > 4: Tissue hypoxia
   - Creatinine > 3: Kidney failure
   - INR > 2: Coagulopathy
   
3. Diagnosis severity:
   - Sepsis: 15-20% mortality
   - Acute MI: 5-10% mortality
   - Stroke: 10-15% mortality
   
4. Age adjustment:
   - Higher age multiplies risk
   - Comorbidities increase risk
   
5. Final calculation:
   - Weighted sum of factors
   - Scale 0-1 (0 = no risk, 1 = certain death)
        """

        risk_score = 0.0

        # SpO2 component
        spo2 = vital_signs.get("oxygen_saturation", 98)
        if spo2 < 90:
            risk_score += 0.3

        # Lactate component
        lactate = lab_values.get("lactate", 0)
        if lactate > 4:
            risk_score += 0.25

        # Diagnosis severity
        if "sepsis" in [d.lower() for d in diagnoses]:
            risk_score += 0.2
        if "acute_mi" in [d.lower() for d in diagnoses]:
            risk_score += 0.15

        return min(risk_score, 1.0)  # Cap at 1.0

    async def calculate_hospitalization_risk(
        self,
        acute_risks: List[Dict],
        chronic_conditions: int,
        functional_status: str
    ) -> float:
        """
        Estimate need for hospitalization
        """

        risk = 0.0

        # Number of acute risks
        if len(acute_risks) > 0:
            risk += 0.4

        # Chronic condition burden
        if chronic_conditions > 3:
            risk += 0.3

        # Functional status
        if functional_status == "dependent":
            risk += 0.3

        return min(risk, 1.0)

    async def assess_comprehensive_risk(
        self,
        patient_id: str,
        vital_signs: Dict[str, float],
        lab_values: Dict[str, float],
        clinical_findings: Dict[str, Any],
        patient_history: Dict[str, Any]
    ) -> RiskAssessment:
        """
        Complete risk stratification
        """

        current_conditions = clinical_findings.get("diagnoses", [])
        medications = clinical_findings.get("medications", [])

        # Assess all risk components
        acute_risks = await self.assess_acute_risks(vital_signs, clinical_findings)
        chronic_risks = await self.assess_chronic_risks(
            patient_history,
            current_conditions
        )
        complication_risks = await self.assess_complication_risks(
            current_conditions,
            medications,
            patient_history
        )

        # Calculate aggregate scores
        mortality_risk = await self.calculate_mortality_risk(
            vital_signs,
            lab_values,
            current_conditions
        )

        hospitalization_risk = await self.calculate_hospitalization_risk(
            acute_risks,
            len(current_conditions),
            patient_history.get("functional_status", "independent")
        )

        # Overall risk score: weighted combination
        overall_risk = (
            0.4 * len(acute_risks) / 5 +  # Acute risk prevalence
            0.2 * mortality_risk +
            0.2 * hospitalization_risk +
            0.2 * (len(complication_risks) / 5)
        )

        # Determine risk level
        if overall_risk > 0.7:
            risk_level = "critical"
        elif overall_risk > 0.5:
            risk_level = "high"
        elif overall_risk > 0.3:
            risk_level = "moderate"
        else:
            risk_level = "low"

        # Generate interventions
        interventions = []
        if acute_risks:
            interventions.append("Urgent medical evaluation")
        if hospitalization_risk > 0.5:
            interventions.append("Consider hospitalization")
        if mortality_risk > 0.1:
            interventions.append("Intensive monitoring")

        assessment = RiskAssessment(
            patient_id=patient_id,
            overall_risk_score=overall_risk,
            risk_level=risk_level,
            acute_risks=acute_risks,
            chronic_risks=chronic_risks,
            complication_risks=complication_risks,
            mortality_risk=mortality_risk,
            hospitalization_risk=hospitalization_risk,
            interventions_needed=interventions
        )

        return assessment
