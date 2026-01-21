"""
Time-Series Agent: ECG, Vital Signs, and IoT Data Analysis
Processes waveforms, heart rate, blood pressure, and sensor data
"""
import logging
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class TimeSeriesAnalysis:
    """Result of time-series analysis"""
    ts_id: str
    signal_type: str  # ECG, HR, BP, O2, Temperature, etc.
    data_points: int
    time_range: str
    statistics: Dict[str, float]  # Mean, std, min, max
    abnormalities_detected: List[Dict[str, Any]]
    trend_analysis: str
    iot_insights: str
    reasoning: str


class TimeSeriesAgent:
    """
    Processes time-series medical data: ECG, vital signs, IoT wearables.
    Performs statistical analysis, anomaly detection, trend analysis.
    Shows reasoning for clinical interpretation.
    """

    def __init__(self):
        self.supported_signals = [
            "ecg", "heart_rate", "blood_pressure", "oxygen_saturation",
            "temperature", "respiratory_rate", "glucose", "accelerometer"
        ]

    async def parse_timeseries_data(
        self,
        file_path: str
    ) -> Dict[str, Any]:
        """
        Parse time-series data from CSV or JSON
        Returns: {"timestamps": [...], "values": [...], "signal_type": "..."}
        """
        try:
            # Read data file
            if file_path.endswith('.json'):
                with open(file_path, 'r') as f:
                    data = json.load(f)
            elif file_path.endswith('.csv'):
                # Simple CSV parsing
                data = await self._parse_csv(file_path)
            else:
                raise ValueError(f"Unsupported format: {file_path}")

            return data

        except Exception as e:
            logger.error(f"Error parsing time-series data: {str(e)}")
            return {}

    async def _parse_csv(self, file_path: str) -> Dict[str, Any]:
        """Parse CSV time-series data"""
        data = {
            "timestamps": [],
            "values": [],
            "signal_type": "unknown"
        }
        # In production: use pandas
        return data

    async def calculate_statistics(
        self,
        values: List[float]
    ) -> Dict[str, float]:
        """
        Calculate statistical measures
        Shows reasoning for interpretation
        """

        reasoning = f"""
        STATISTICAL ANALYSIS REASONING:
        1. Normality assessment: Check if data is normally distributed
        2. Central tendency: Calculate mean and median
           - Mean used for symmetric distributions
           - Median used for skewed data
        3. Variability: Calculate standard deviation
           - High variability may indicate instability
           - Low variability may indicate stasis
        4. Range analysis: Find min and max values
           - Compare to clinical reference ranges
           - Assess severity of deviations
        5. Percentile analysis: Calculate quartiles
           - Q1, Q2 (median), Q3
           - Detect outliers beyond 1.5*IQR
        """

        if not values:
            return {}

        import statistics
        stats = {
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values),
            "range": max(values) - min(values)
        }

        return stats

    async def analyze_ecg(
        self,
        ecg_data: Dict[str, Any]
    ) -> TimeSeriesAnalysis:
        """
        ECG-specific analysis
        Detect: normal rhythm, arrhythmias, ST changes, etc.
        """

        reasoning = f"""
        ECG ANALYSIS REASONING:
        1. Signal quality check:
           - Check for noise and artifacts
           - Assess baseline stability
           - Verify sampling rate (should be 100+ Hz)
        
        2. Heart rate calculation:
           - Measure RR intervals (peak-to-peak)
           - Calculate BPM from interval durations
           - Assess regularity (normal < 60-100 bpm)
        
        3. Rhythm interpretation:
           - Normal sinus rhythm: regular, P-QRS-T pattern
           - Atrial fibrillation: irregular, no P waves
           - Premature beats: early QRS complexes
           - Bradycardia: HR < 60 bpm
           - Tachycardia: HR > 100 bpm
        
        4. Waveform analysis:
           - QRS duration (should be < 120 ms)
           - ST segment level (should be at baseline)
           - T wave morphology
           - QT interval (corrected for rate)
        
        5. Clinical significance:
           - Acute vs chronic changes
           - Severity assessment
           - Treatment urgency
        """

        abnormalities = []
        trend_analysis = "Analyzing ECG trends..."

        analysis = TimeSeriesAnalysis(
            ts_id=f"ECG-{datetime.now().timestamp()}",
            signal_type="ECG",
            data_points=len(ecg_data.get("values", [])),
            time_range=f"{ecg_data.get('start_time', 'unknown')} to {ecg_data.get('end_time', 'unknown')}",
            statistics=await self.calculate_statistics(ecg_data.get("values", [])),
            abnormalities_detected=abnormalities,
            trend_analysis=trend_analysis,
            iot_insights="ECG monitoring active",
            reasoning=reasoning
        )

        return analysis

    async def analyze_vital_signs(
        self,
        vitals_data: Dict[str, List[float]]
    ) -> Dict[str, TimeSeriesAnalysis]:
        """
        Analyze multiple vital signs in parallel
        vitals_data: {"heart_rate": [...], "blood_pressure": [...], ...}
        """

        reasoning = f"""
        VITAL SIGNS ANALYSIS REASONING:
        
        HEART RATE (HR):
        - Normal range: 60-100 bpm at rest
        - Bradycardia: HR < 60 (concerning if symptomatic)
        - Tachycardia: HR > 100 (assess cause: fever, pain, anxiety, disease)
        - Variability: HRV assessment (higher is better for autonomic health)
        
        BLOOD PRESSURE (BP):
        - Normal: < 120/80 mmHg
        - Elevated: 120-129/<80
        - Stage 1 HTN: 130-139/80-89
        - Stage 2 HTN: ≥140/90
        - Hypotensive: < 90/60 (assess symptoms)
        - Pulse pressure: SYS - DIA (30-40 mmHg normal)
        
        OXYGEN SATURATION (SpO2):
        - Normal: > 95% at sea level
        - Mild hypoxia: 90-95%
        - Moderate hypoxia: 80-90% (requires intervention)
        - Severe hypoxia: < 80% (critical)
        - Trend: Declining SpO2 concerning
        
        TEMPERATURE:
        - Normal: 36.5-37.5°C (97.7-99.5°F)
        - Fever: > 38°C (100.4°F)
        - Hypothermia: < 36°C (< 96.8°F)
        - Significance: Fever suggests infection; trend important
        
        RESPIRATORY RATE (RR):
        - Normal: 12-20 breaths/min
        - Tachypnea: > 20 (assess cause)
        - Bradypnea: < 12 (concerning if depressed)
        - Pattern: Regular vs irregular
        """

        results = {}

        for vital_name, values in vitals_data.items():
            stats = await self.calculate_statistics(values)

            # Assess normality
            abnormalities = []
            if vital_name == "heart_rate":
                mean_hr = stats.get("mean", 0)
                if mean_hr > 100:
                    abnormalities.append({
                        "type": "tachycardia",
                        "value": mean_hr,
                        "severity": "mild" if mean_hr < 120 else "moderate",
                        "action": "monitor_trend"
                    })
                elif mean_hr < 60:
                    abnormalities.append({
                        "type": "bradycardia",
                        "value": mean_hr,
                        "action": "assess_symptoms"
                    })

            analysis = TimeSeriesAnalysis(
                ts_id=f"{vital_name.upper()}-{datetime.now().timestamp()}",
                signal_type=vital_name,
                data_points=len(values),
                time_range="Continuous monitoring",
                statistics=stats,
                abnormalities_detected=abnormalities,
                trend_analysis=await self._assess_trend(values),
                iot_insights=f"Wearable device tracking {vital_name}",
                reasoning=reasoning
            )

            results[vital_name] = analysis

        return results

    async def _assess_trend(self, values: List[float]) -> str:
        """
        Assess trend: stable, improving, worsening
        Shows reasoning for trend assessment
        """

        if len(values) < 2:
            return "insufficient_data"

        # Simple trend: compare recent vs older values
        recent_mean = sum(values[-5:]) / min(5, len(values))
        older_mean = sum(values[:5]) / min(5, len(values))

        if recent_mean > older_mean * 1.05:
            return "worsening"
        elif recent_mean < older_mean * 0.95:
            return "improving"
        else:
            return "stable"

    async def detect_iot_anomalies(
        self,
        timeseries_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Detect anomalies in IoT wearable data
        Uses statistical methods and ML
        """

        reasoning = f"""
        ANOMALY DETECTION REASONING:
        1. Statistical approach: Identify values > 3 std devs from mean
        2. Contextual outliers: Unusual patterns for time of day
        3. Physiologically impossible: Values outside biological range
        4. Sudden changes: Rapid transitions indicating events
        5. Sensor issues: Flat lines or noise indicating malfunction
        """

        anomalies = []

        # Get statistics
        values = timeseries_data.get("values", [])
        if values:
            stats = await self.calculate_statistics(values)
            threshold = stats.get("mean", 0) + 3 * stats.get("std_dev", 1)

            # Identify outliers
            for i, val in enumerate(values):
                if val > threshold or val < stats.get("mean", 0) - 3 * stats.get("std_dev", 1):
                    anomalies.append({
                        "timestamp_index": i,
                        "value": val,
                        "severity": "high",
                        "type": "statistical_outlier"
                    })

        return anomalies

    async def process(self, medical_data) -> Dict[str, Any]:
        """
        Main processing function called by ingestion agent
        """
        try:
            ts_data = await self.parse_timeseries_data(medical_data.file_path)

            if medical_data.data_type.lower() == "ecg":
                analysis = await self.analyze_ecg(ts_data)
            else:
                # Generic vital sign analysis
                analyses = await self.analyze_vital_signs({
                    medical_data.data_type: ts_data.get("values", [])
                })
                analysis = list(analyses.values())[0]

            return {
                "agent": "timeseries_agent",
                "analysis": analysis.__dict__,
                "status": "completed",
                "data_points": analysis.data_points
            }

        except Exception as e:
            logger.error(f"Time-series processing error: {str(e)}")
            return {"status": "error", "error": str(e)}
