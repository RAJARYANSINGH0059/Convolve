"""
Text-to-Speech and Multi-Language Report Narration
Google Cloud Text-to-Speech integration
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class TextToSpeechReportNarrator:
    """
    Converts clinical report to narrated audio in multiple languages
    Uses Google Cloud Text-to-Speech API
    Produces patient-friendly and medical professional narrations
    """

    def __init__(self, gcp_project_id: str):
        self.gcp_project_id = gcp_project_id
        self.supported_languages = {
            "en": {
                "name": "English",
                "language_code": "en-US",
                "voice_name": "en-US-Neural2-C",
                "ssml_gender": "FEMALE"
            },
            "es": {
                "name": "Spanish",
                "language_code": "es-ES",
                "voice_name": "es-ES-Neural2-A",
                "ssml_gender": "FEMALE"
            },
            "fr": {
                "name": "French",
                "language_code": "fr-FR",
                "voice_name": "fr-FR-Neural2-A",
                "ssml_gender": "FEMALE"
            },
            "de": {
                "name": "German",
                "language_code": "de-DE",
                "voice_name": "de-DE-Neural2-B",
                "ssml_gender": "MALE"
            },
            "hi": {
                "name": "Hindi",
                "language_code": "hi-IN",
                "voice_name": "hi-IN-Neural2-A",
                "ssml_gender": "FEMALE"
            },
            "pt": {
                "name": "Portuguese",
                "language_code": "pt-BR",
                "voice_name": "pt-BR-Neural2-A",
                "ssml_gender": "FEMALE"
            },
            "zh": {
                "name": "Chinese (Mandarin)",
                "language_code": "zh-CN",
                "voice_name": "zh-CN-Neural2-A",
                "ssml_gender": "FEMALE"
            },
            "ja": {
                "name": "Japanese",
                "language_code": "ja-JP",
                "voice_name": "ja-JP-Neural2-A",
                "ssml_gender": "FEMALE"
            }
        }

    async def create_patient_friendly_narrative(
        self,
        consolidated_report: Dict
    ) -> str:
        """
        Create simplified narrative for patients
        Uses non-technical language
        """

        narrative = f"""
PATIENT REPORT SUMMARY

Your Health Condition:
{consolidated_report.get('chief_complaint', 'Assessment completed')}

What We Found:
{consolidated_report.get('patient_voice', '')}

Our Assessment:
Based on our examination and tests, we found:
{consolidated_report.get('imaging_findings', 'Normal findings')}

Your Diagnosis:
{consolidated_report.get('primary_diagnosis', 'To be discussed with doctor')}

What You Need To Do:
Medications to take as prescribed
Keep all follow-up appointments
Watch for warning signs
Follow lifestyle recommendations

Important Safety Notes:
{', '.join(consolidated_report.get('precautions', []))}

Next Steps:
{consolidated_report.get('follow_up', '')}

If you have questions, please contact your healthcare provider.
        """

        return narrative

    async def create_medical_professional_narrative(
        self,
        consolidated_report: Dict,
        clinical_intelligence_summary: Dict
    ) -> str:
        """
        Create detailed clinical narrative for healthcare providers
        Uses medical terminology
        """

        narrative = f"""
CLINICAL INTELLIGENCE SUMMARY

PATIENT IDENTIFICATION:
{consolidated_report.get('patient_name', 'Unknown')}
ID: {consolidated_report.get('patient_id', 'N/A')}

CHIEF COMPLAINT:
{consolidated_report.get('chief_complaint', '')}

PATIENT NARRATIVE:
{consolidated_report.get('patient_voice', '')}

VITAL SIGNS:
{json.dumps(consolidated_report.get('vital_signs', {}), indent=2)}

IMAGING FINDINGS:
{consolidated_report.get('imaging_findings', 'No abnormalities detected')}

CLINICAL ASSESSMENT:
Primary Diagnosis: {consolidated_report.get('primary_diagnosis', '')}
Confidence Level: {consolidated_report.get('confidence_score', 0):.2%}
Severity: {consolidated_report.get('severity', 'Moderate')}

DIFFERENTIAL DIAGNOSES:
{json.dumps(consolidated_report.get('differential_diagnoses', []), indent=2)}

DIAGNOSTIC FINDINGS:
IoT Data: {consolidated_report.get('iot_data_summary', '')}
Laboratory: {json.dumps(consolidated_report.get('lab_results', {}), indent=2)}

RISK ASSESSMENT:
Overall Risk Score: {consolidated_report.get('confidence_score', 0)}

TREATMENT PLAN:
Medications: {json.dumps(consolidated_report.get('medications', []), indent=2)}
Required Investigations: {', '.join(consolidated_report.get('investigations_needed', []))}
Monitoring Plan: {consolidated_report.get('vital_signs', {})}

PRECAUTIONS AND CONTRAINDICATIONS:
{json.dumps(consolidated_report.get('precautions', []), indent=2)}

FOLLOW-UP SCHEDULE:
{consolidated_report.get('follow_up', 'As clinically indicated')}

EVIDENCE SUMMARY:
{consolidated_report.get('evidence_summary', '')}

This report is generated by AI-assisted analysis and requires clinician review and validation.
        """

        return narrative

    async def translate_narrative(
        self,
        text: str,
        target_language: str
    ) -> str:
        """
        Translate narrative to target language
        In production: Use Google Translate API
        """

        if target_language == "en":
            return text

        # In production: Call Google Translate API
        # For demo: Indicate translation would occur
        translated = f"[Translated to {self.supported_languages.get(target_language, {}).get('name', target_language)}]\n\n{text}"

        return translated

    async def synthesize_speech(
        self,
        text: str,
        language_code: str,
        output_path: str
    ) -> Dict[str, str]:
        """
        Convert text to speech using Google Cloud TTS
        Returns path to audio file
        """

        if language_code not in self.supported_languages:
            logger.error(f"Language not supported: {language_code}")
            return {"status": "error", "error": "Language not supported"}

        lang_config = self.supported_languages[language_code]

        try:
            # In production: Call Google Cloud TTS API
            synthesis_request = {
                "input": {"text": text},
                "voice": {
                    "language_code": lang_config["language_code"],
                    "name": lang_config["voice_name"],
                    "ssml_gender": lang_config["ssml_gender"]
                },
                "audio_config": {
                    "audio_encoding": "MP3",
                    "pitch": 0,
                    "speaking_rate": 1.0
                }
            }

            # Simulated response
            result = {
                "status": "completed",
                "audio_file": output_path,
                "language": lang_config["name"],
                "duration_ms": 0,  # Would be calculated
                "file_format": "MP3",
                "creation_time": datetime.now().isoformat()
            }

            logger.info(f"Speech synthesized for {lang_config['name']}")

            return result

        except Exception as e:
            logger.error(f"Speech synthesis error: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def generate_narrated_report(
        self,
        consolidated_report: Dict,
        clinical_summary: Dict,
        selected_language: str,
        narrative_type: str = "patient_friendly"
    ) -> Dict[str, str]:
        """
        Generate complete narrated report in selected language
        
        narrative_type: 'patient_friendly' or 'medical_professional'
        """

        try:
            # Create narrative
            if narrative_type == "patient_friendly":
                narrative = await self.create_patient_friendly_narrative(
                    consolidated_report
                )
            else:
                narrative = await self.create_medical_professional_narrative(
                    consolidated_report,
                    clinical_summary
                )

            # Translate if needed
            if selected_language != "en":
                narrative = await self.translate_narrative(
                    narrative,
                    selected_language
                )

            # Synthesize speech
            output_path = f"/tmp/report_narration_{selected_language}_{datetime.now().timestamp()}.mp3"
            
            speech_result = await self.synthesize_speech(
                text=narrative,
                language_code=selected_language,
                output_path=output_path
            )

            return {
                "status": "completed",
                "language": selected_language,
                "narrative_type": narrative_type,
                "narrative_text": narrative,
                "audio_file": speech_result.get("audio_file"),
                "audio_format": "MP3",
                "creation_time": datetime.now().isoformat(),
                "available_languages": list(self.supported_languages.keys())
            }

        except Exception as e:
            logger.error(f"Report narration error: {str(e)}")
            return {"status": "error", "error": str(e)}

    async def generate_multi_language_reports(
        self,
        consolidated_report: Dict,
        clinical_summary: Dict,
        languages: List[str]
    ) -> Dict[str, Dict]:
        """
        Generate narrated reports in multiple languages
        """

        results = {}

        for lang in languages:
            if lang in self.supported_languages:
                result = await self.generate_narrated_report(
                    consolidated_report,
                    clinical_summary,
                    lang,
                    narrative_type="patient_friendly"
                )
                results[lang] = result

        return {
            "status": "completed",
            "languages_generated": len(results),
            "reports": results
        }

    async def create_pdf_report(
        self,
        consolidated_report: Dict,
        output_path: str
    ) -> Dict[str, str]:
        """
        Create printable PDF report
        In production: Use reportlab or similar
        """

        try:
            pdf_content = f"""
CLINICAL REPORT

Patient: {consolidated_report.get('patient_name', 'Unknown')}
Date: {consolidated_report.get('visit_date', '')}

Diagnosis: {consolidated_report.get('primary_diagnosis', '')}
Severity: {consolidated_report.get('severity', 'Moderate')}

Medications:
{json.dumps(consolidated_report.get('medications', []), indent=2)}

Follow-up: {consolidated_report.get('follow_up', '')}

This report is generated by AI-assisted clinical analysis.
            """

            # In production: Use PDF library
            # For demo: Just indicate it was created

            return {
                "status": "completed",
                "pdf_path": output_path,
                "format": "PDF",
                "creation_time": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"PDF creation error: {str(e)}")
            return {"status": "error", "error": str(e)}
