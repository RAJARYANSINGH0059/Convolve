"""
Agent 1: Data Ingestion Agent
Routes medical data across modalities and coordinates initial processing
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import mimetypes
from dataclasses import asdict
from concurrent.futures import ThreadPoolExecutor

from utils.models import MedicalData, PatientRecord
from config.settings import DATA_MODALITIES

logger = logging.getLogger(__name__)


class IngestionAgent:
    """
    Routes incoming medical data to appropriate modality-specific processors.
    Validates data, extracts metadata, and coordinates parallel processing.
    """
    
    def __init__(self):
        self.supported_formats = {}
        self.modality_handlers = {}
        self._initialize_formats()
        self.executor = ThreadPoolExecutor(max_workers=4)

    def _initialize_formats(self):
        """Map file formats to modalities"""
        for modality, config in DATA_MODALITIES.items():
            for fmt in config.get("format", []):
                self.supported_formats[fmt.lower()] = modality

    def register_handler(self, modality: str, handler):
        """Register a handler for a specific modality"""
        self.modality_handlers[modality] = handler
        logger.info(f"Registered handler for modality: {modality}")

    def detect_modality(self, file_path: str) -> Optional[str]:
        """Detect data modality from file extension"""
        ext = Path(file_path).suffix.lower().lstrip(".")
        return self.supported_formats.get(ext)

    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract metadata from file"""
        path = Path(file_path)
        return {
            "filename": path.name,
            "file_size": path.stat().st_size if path.exists() else 0,
            "mime_type": mimetypes.guess_type(file_path)[0],
            "extension": path.suffix
        }

    def validate_data(self, file_path: str, modality: str) -> bool:
        """Validate data format and integrity"""
        if not Path(file_path).exists():
            logger.error(f"File not found: {file_path}")
            return False
        
        path = Path(file_path)
        
        # Check file size (max 100MB)
        if path.stat().st_size > 100 * 1024 * 1024:
            logger.error(f"File too large: {file_path}")
            return False
        
        # Check extension matches modality
        ext = path.suffix.lower().lstrip(".")
        allowed_formats = DATA_MODALITIES.get(modality, {}).get("format", [])
        if not any(ext.lower() == fmt.lower() for fmt in allowed_formats):
            logger.error(f"Invalid format {ext} for modality {modality}")
            return False
        
        return True

    async def ingest_medical_data(
        self,
        patient_id: str,
        file_path: str,
        data_type: str,
        additional_metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[MedicalData]:
        """
        Main ingestion pipeline for medical data
        Returns MedicalData object ready for processing
        """
        try:
            # Detect modality
            modality = self.detect_modality(file_path)
            if not modality:
                logger.error(f"Unable to detect modality for {file_path}")
                return None

            # Validate data
            if not self.validate_data(file_path, modality):
                logger.error(f"Data validation failed for {file_path}")
                return None

            # Extract metadata
            metadata = self.extract_metadata(file_path)
            if additional_metadata:
                metadata.update(additional_metadata)

            # Create medical data record
            medical_data = MedicalData(
                patient_id=patient_id,
                modality=modality,
                data_type=data_type,
                file_path=file_path,
                file_format=Path(file_path).suffix.lower(),
                metadata=metadata
            )

            logger.info(f"Ingested data: {medical_data.data_id} for patient {patient_id}")
            return medical_data

        except Exception as e:
            logger.error(f"Error ingesting data: {str(e)}")
            return None

    async def batch_ingest(
        self,
        patient_id: str,
        data_items: List[Dict[str, Any]]
    ) -> List[MedicalData]:
        """
        Ingest multiple medical data items in parallel
        Each item: {"file_path": str, "data_type": str, "metadata": dict}
        """
        tasks = [
            self.ingest_medical_data(
                patient_id=patient_id,
                file_path=item["file_path"],
                data_type=item.get("data_type", "unknown"),
                additional_metadata=item.get("metadata")
            )
            for item in data_items
        ]
        
        results = await asyncio.gather(*tasks)
        return [r for r in results if r is not None]

    async def process_with_handler(
        self,
        medical_data: MedicalData
    ) -> Optional[Any]:
        """
        Route data to appropriate modality handler
        Handlers are set by specialized agents (Vision, Speech, NLP, TimeSeries)
        """
        handler = self.modality_handlers.get(medical_data.modality)
        if not handler:
            logger.warning(f"No handler for modality: {medical_data.modality}")
            return None

        try:
            # Run handler asynchronously
            result = await handler.process(medical_data)
            return result
        except Exception as e:
            logger.error(f"Error processing {medical_data.data_id}: {str(e)}")
            return None

    async def coordinate_parallel_ingestion(
        self,
        patient_id: str,
        data_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Coordinate complete ingestion workflow:
        1. Ingest all data items
        2. Route to appropriate handlers
        3. Return structured results
        """
        ingested_data = await self.batch_ingest(patient_id, data_items)
        
        processing_results = {
            "imaging": [],
            "audio": [],
            "text": [],
            "timeseries": []
        }

        # Process each modality
        for data in ingested_data:
            result = await self.process_with_handler(data)
            if result:
                processing_results[data.modality].append({
                    "data_id": data.data_id,
                    "type": data.data_type,
                    "processing_result": result
                })

        return {
            "patient_id": patient_id,
            "total_items_ingested": len(ingested_data),
            "processing_results": processing_results,
            "status": "completed"
        }
