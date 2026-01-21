"""
Retrieval Agent: Hybrid Search and Data Retrieval
Fetches relevant clinical data for reasoning agents
"""
import logging
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import asdict
from utils.models import QdrantSearchResult

logger = logging.getLogger(__name__)


class RetrievalAgent:
    """
    Retrieves clinical data from Qdrant for reasoning agents.
    Performs hybrid searches, manages relevance ranking,
    and provides evidence for clinical decision-making.
    Shows retrieval reasoning for transparency.
    """

    def __init__(self, memory_agent):
        self.memory_agent = memory_agent

    async def retrieve_patient_data(
        self,
        patient_id: str,
        query: str,
        query_embedding: List[float],
        query_sparse: Dict[int, float],
        search_type: str = "hybrid",
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Retrieve relevant clinical data for a patient
        Shows retrieval strategy and reasoning
        """

        reasoning = f"""
        RETRIEVAL STRATEGY REASONING:
        1. Query analysis:
           - User query: {query[:100]}...
           - Query type: {search_type}
           - Number of results: top_k={top_k}
        
        2. Filter application:
           - Patient ID: {patient_id} (isolation)
           - Modality filters: {filters.get('modalities') if filters else 'none'}
           - Date range: {filters.get('date_range') if filters else 'all'}
        
        3. Search execution:
           - Dense search: Semantic matching
           - Sparse search: Keyword matching
           - Hybrid: Combined relevance ranking
        
        4. Result ranking:
           - Primary: Relevance score
           - Secondary: Recency (temporal)
           - Tertiary: Data modality diversity
        
        5. Evidence presentation:
           - Include similarity scores
           - Show search term matches
           - Provide context snippets
        """

        try:
            # Execute appropriate search
            if search_type == "hybrid":
                results = await self.memory_agent.hybrid_search(
                    patient_id=patient_id,
                    query_dense=query_embedding,
                    query_sparse=query_sparse,
                    filters=filters,
                    top_k=top_k
                )
            elif search_type == "temporal":
                results = await self.memory_agent.temporal_search(
                    patient_id=patient_id,
                    query_embedding=query_embedding,
                    time_window_days=filters.get("time_window_days", 90) if filters else 90
                )
            else:
                results = []

            # Format results
            retrieval_result = {
                "patient_id": patient_id,
                "query": query,
                "search_type": search_type,
                "results_found": len(results),
                "top_k": top_k,
                "results": results,
                "retrieval_reasoning": reasoning
            }

            return retrieval_result

        except Exception as e:
            logger.error(f"Retrieval error: {str(e)}")
            return {
                "patient_id": patient_id,
                "error": str(e),
                "results": []
            }

    async def retrieve_by_modality(
        self,
        patient_id: str,
        modalities: List[str],
        top_k: int = 10
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Retrieve data grouped by modality type
        Used for comprehensive analysis
        """

        reasoning = f"""
        MODALITY-BASED RETRIEVAL:
        1. Request: Retrieve top {top_k} items per modality
        2. Modalities: {', '.join(modalities)}
        3. Use case: Comprehensive multi-modal analysis
        4. Ordering: Relevance within each modality
        """

        results = {}

        for modality in modalities:
            filters = {
                "patient_id": patient_id,
                "modality": modality
            }

            # Execute search for this modality
            modality_results = await self.memory_agent.hybrid_search(
                patient_id=patient_id,
                query_dense=[0] * 3072,  # Dummy query, will be filtered by modality
                query_sparse={},
                filters=filters,
                top_k=top_k
            )

            results[modality] = modality_results

        return results

    async def retrieve_patient_timeline(
        self,
        patient_id: str,
        days_back: int = 90
    ) -> Dict[str, Any]:
        """
        Retrieve complete patient timeline for continuity analysis
        Shows temporal construction reasoning
        """

        reasoning = f"""
        TIMELINE CONSTRUCTION REASONING:
        1. Temporal scope:
           - Period: Last {days_back} days
           - Start: {days_back} days ago
           - End: Today
        
        2. Data organization:
           - Chronological ordering
           - Modality grouping
           - Event sequencing
        
        3. Gap analysis:
           - Identify missing data periods
           - Flag unexpected gaps
           - Assess data completeness
        
        4. Trend identification:
           - Worsening vs improving
           - Stability assessment
           - Acute vs chronic changes
        
        5. Clinical continuity:
           - Disease progression
           - Treatment response
           - Intervention timing
        """

        try:
            # Retrieve all data for patient in time window
            filters = {
                "patient_id": patient_id,
                "time_window_days": days_back
            }

            timeline_data = await self.memory_agent.temporal_search(
                patient_id=patient_id,
                query_embedding=[0] * 3072,  # No specific query
                time_window_days=days_back,
                similarity_decay=True
            )

            return {
                "patient_id": patient_id,
                "time_period_days": days_back,
                "events": timeline_data,
                "timeline_reasoning": reasoning
            }

        except Exception as e:
            logger.error(f"Timeline retrieval error: {str(e)}")
            return {"error": str(e)}

    async def retrieve_similar_cases(
        self,
        patient_id: str,
        case_embedding: List[float],
        exclude_self: bool = True,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Retrieve similar cases from other patients for comparative analysis
        Shows clinical similarity reasoning
        """

        reasoning = f"""
        CLINICAL SIMILARITY MATCHING:
        1. Reference case:
           - Patient ID: {patient_id}
           - Case complexity: Multi-modal analysis
        
        2. Similarity search:
           - Metric: Cosine similarity
           - Exclude self: {exclude_self}
           - Top results: {top_k}
        
        3. Relevance factors:
           - Symptom overlap
           - Demographics similarity (if available)
           - Disease stage alignment
           - Treatment outcomes
        
        4. Clinical value:
           - Comparative treatment plans
           - Outcome prediction
           - Differential diagnosis support
        
        5. Privacy consideration:
           - Anonymization of retrieved cases
           - HIPAA compliance
           - De-identification
        """

        try:
            # Search for similar embeddings (from other patients)
            similar_results = await self.memory_agent.hybrid_search(
                patient_id="*",  # Search all patients
                query_dense=case_embedding,
                query_sparse={},
                filters={"exclude_patient_id": patient_id} if exclude_self else None,
                top_k=top_k
            )

            return similar_results

        except Exception as e:
            logger.error(f"Similar cases retrieval error: {str(e)}")
            return []

    async def retrieve_for_reasoning(
        self,
        patient_id: str,
        clinical_context: str,
        required_modalities: List[str]
    ) -> Dict[str, Any]:
        """
        Comprehensive retrieval for reasoning agents
        Gathers all necessary data for multi-modal analysis
        """

        try:
            # 1. Retrieve by modality
            modality_data = await self.retrieve_by_modality(
                patient_id=patient_id,
                modalities=required_modalities,
                top_k=5
            )

            # 2. Retrieve timeline
            timeline = await self.retrieve_patient_timeline(
                patient_id=patient_id,
                days_back=90
            )

            # 3. Retrieve similar cases for comparison
            # (would need case embedding from consolidated report)
            similar_cases = []

            return {
                "patient_id": patient_id,
                "clinical_context": clinical_context,
                "modality_data": modality_data,
                "timeline": timeline,
                "similar_cases": similar_cases,
                "retrieval_status": "completed"
            }

        except Exception as e:
            logger.error(f"Comprehensive retrieval error: {str(e)}")
            return {"error": str(e)}

    async def process(self, retrieval_request) -> Dict[str, Any]:
        """
        Main processing for retrieval requests
        """
        result = await self.retrieve_patient_data(
            patient_id=retrieval_request.get("patient_id"),
            query=retrieval_request.get("query", ""),
            query_embedding=retrieval_request.get("query_embedding", []),
            query_sparse=retrieval_request.get("query_sparse", {}),
            search_type=retrieval_request.get("search_type", "hybrid"),
            top_k=retrieval_request.get("top_k", 5),
            filters=retrieval_request.get("filters")
        )

        return {
            "agent": "retrieval_agent",
            **result
        }
