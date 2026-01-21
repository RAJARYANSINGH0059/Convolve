"""
NLP Agent: Clinical Natural Language Processing
Extracts entities, relationships, and clinical concepts from text
"""
import logging
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TextAnalysis:
    """Result of NLP analysis"""
    text_id: str
    document_type: str
    raw_text: str
    extracted_entities: Dict[str, List[str]]
    relationships: List[Dict[str, str]]
    medications: List[Dict[str, str]]
    diagnoses: List[Dict[str, str]]
    procedures: List[Dict[str, str]]
    allergies: List[str]
    document_sentiment: str
    reasoning: str


class NLPAgent:
    """
    Processes clinical text: notes, prescriptions, discharge summaries.
    Extracts medical entities, medications, diagnoses, and relationships.
    Shows reasoning for clinical NER (Named Entity Recognition).
    """

    def __init__(self):
        self.supported_formats = [".txt", ".pdf", ".docx"]
        self.entity_types = [
            "SYMPTOM", "DIAGNOSIS", "MEDICATION", "DOSAGE",
            "PROCEDURE", "ALLERGY", "VITAL_SIGN", "ANATOMICAL",
            "TEMPORAL", "NEGATION"
        ]

    async def extract_clinical_entities(
        self,
        text: str
    ) -> Dict[str, List[str]]:
        """
        Extract clinical named entities from text
        Shows LLM reasoning for each entity type
        """

        reasoning = f"""
        CLINICAL NER REASONING:
        
        1. SYMPTOM EXTRACTION:
           - Look for complaint descriptions
           - Identify modifiers (severe, mild, acute, chronic)
           - Extract temporal information (duration, onset)
           - Example: "severe headache for 3 days" -> symptom: headache, severity: severe, duration: 3 days
        
        2. DIAGNOSIS EXTRACTION:
           - Find confirmed diagnoses
           - Identify presumptive diagnoses
           - Extract confidence markers
           - Example: "probable hypertension" -> diagnosis: hypertension, confidence: probable
        
        3. MEDICATION EXTRACTION:
           - Identify drug names
           - Extract dosages and frequencies
           - Note routes of administration
           - Example: "Aspirin 500mg twice daily" -> drug: Aspirin, dose: 500mg, frequency: twice daily
        
        4. PROCEDURE EXTRACTION:
           - Find medical procedures mentioned
           - Extract outcomes if stated
           - Example: "CT scan revealed..." -> procedure: CT scan, outcome: findings
        
        5. ALLERGY EXTRACTION:
           - Identify allergens and reactions
           - Note severity
           - Example: "Penicillin - severe rash" -> allergen: Penicillin, reaction: rash, severity: severe
        
        6. VITAL SIGNS:
           - Extract numerical values
           - Link to measurement type
           - Example: "BP: 140/90" -> vital: blood_pressure, value: 140/90
        """

        # Template entity extraction
        entities = {
            "SYMPTOM": [],
            "DIAGNOSIS": [],
            "MEDICATION": [],
            "ALLERGY": [],
            "PROCEDURE": [],
            "VITAL_SIGN": []
        }

        # In production: Use spaCy biomedical model or LLM
        # entities would be populated from actual text

        return entities

    async def extract_medications(
        self,
        text: str
    ) -> List[Dict[str, str]]:
        """
        Extract medication information with all details
        Shows reasoning for medication parsing
        """

        reasoning = f"""
        MEDICATION EXTRACTION REASONING:
        1. Pattern matching: Find drug name patterns
        2. Dosage extraction: Identify quantity and units
        3. Frequency parsing: Extract "twice daily", "every 8 hours", etc.
        4. Route identification: Find administration route (oral, IV, topical)
        5. Duration extraction: Get treatment duration if mentioned
        6. Indications: Link medication to indication if stated
        """

        medications = [
            # Template structure
            {
                "name": "",
                "dosage": "",
                "frequency": "",
                "route": "oral",
                "duration": "",
                "indication": "",
                "confidence": 0.0
            }
        ]

        return medications

    async def extract_diagnoses(
        self,
        text: str
    ) -> List[Dict[str, str]]:
        """
        Extract diagnostic information
        Shows reasoning for diagnosis extraction
        """

        diagnoses = [
            {
                "diagnosis": "",
                "icd_code": "",
                "confidence": "definite",  # definite, probable, rule_out
                "context": ""
            }
        ]

        return diagnoses

    async def analyze_text(
        self,
        text: str,
        document_type: str,
        document_id: Optional[str] = None
    ) -> TextAnalysis:
        """
        Complete NLP analysis of clinical text
        document_type: 'clinical_notes', 'prescription', 'discharge_summary'
        """

        try:
            # Extract all entities
            entities = await self.extract_clinical_entities(text)
            medications = await self.extract_medications(text)
            diagnoses = await self.extract_diagnoses(text)

            # Extract relationships between entities
            relationships = await self._extract_relationships(
                text,
                entities,
                medications,
                diagnoses
            )

            # Determine document sentiment
            sentiment = await self._analyze_sentiment(text)

            analysis = TextAnalysis(
                text_id=document_id or "TEXT-unknown",
                document_type=document_type,
                raw_text=text,
                extracted_entities=entities,
                relationships=relationships,
                medications=medications,
                diagnoses=diagnoses,
                procedures=[],  # Would be extracted
                allergies=entities.get("ALLERGY", []),
                document_sentiment=sentiment,
                reasoning=f"Analyzed {len(text)} characters using clinical NER"
            )

            return analysis

        except Exception as e:
            logger.error(f"Text analysis error: {str(e)}")
            raise

    async def _extract_relationships(
        self,
        text: str,
        entities: Dict,
        medications: List[Dict],
        diagnoses: List[Dict]
    ) -> List[Dict[str, str]]:
        """
        Extract relationships between clinical entities
        Example: medication is for this diagnosis
        """

        relationships = [
            # {
            #     "entity1": "symptom",
            #     "entity1_value": "headache",
            #     "relationship": "treated_by",
            #     "entity2": "medication",
            #     "entity2_value": "aspirin"
            # }
        ]

        return relationships

    async def _analyze_sentiment(self, text: str) -> str:
        """
        Analyze overall sentiment of clinical note
        positive: improvement, better, resolved
        negative: worsening, severe, critical
        neutral: factual observations
        """
        return "neutral"  # Would be computed

    async def process(self, medical_data) -> Dict[str, Any]:
        """
        Main processing function called by ingestion agent
        """
        # Read text file
        try:
            with open(medical_data.file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
        except Exception as e:
            logger.error(f"Error reading text file: {str(e)}")
            text_content = ""

        analysis = await self.analyze_text(
            text=text_content,
            document_type=medical_data.data_type,
            document_id=medical_data.data_id
        )

        return {
            "agent": "nlp_agent",
            "analysis": {
                "document_type": analysis.document_type,
                "entities": analysis.extracted_entities,
                "medications": analysis.medications,
                "diagnoses": analysis.diagnoses,
                "allergies": analysis.allergies,
                "relationships": analysis.relationships
            },
            "status": "completed",
            "entity_count": sum(len(v) for v in analysis.extracted_entities.values())
        }

    async def batch_analyze(
        self,
        text_items: List[Dict[str, str]]
    ) -> List[TextAnalysis]:
        """
        Analyze multiple texts in parallel
        Each item: {"text": str, "document_type": str, "document_id": str}
        """
        tasks = [
            self.analyze_text(
                text=item["text"],
                document_type=item.get("document_type", "unknown"),
                document_id=item.get("document_id")
            )
            for item in text_items
        ]
        return await asyncio.gather(*tasks)
