"""
Memory Agent: Qdrant Vector Database Interaction
Manages hybrid dense+sparse search, temporal indexing, audit trails
"""
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)


class MemoryAgent:
    """
    Manages all interactions with Qdrant vector database.
    Handles:
    - Dense embedding storage and search
    - Sparse embedding (BM25) search
    - Hybrid search combining both
    - Temporal similarity search
    - Audit trail logging
    - Patient memory management
    """

    def __init__(self, qdrant_config: Dict[str, str]):
        self.qdrant_endpoint = qdrant_config.get("endpoint")
        self.qdrant_api_key = qdrant_config.get("api_key")
        self.qdrant_cluster_id = qdrant_config.get("cluster_id")

        self.dense_collection = "clinical_dense_embeddings"
        self.sparse_collection = "clinical_sparse_embeddings"
        self.hybrid_collection = "clinical_hybrid_search"

        self.audit_trail = []

    async def initialize_collections(self):
        """
        Initialize Qdrant collections
        Creates collections if they don't exist
        """
        try:
            # In production: Use Qdrant Python client
            logger.info("Initializing Qdrant collections")

            # Dense collection configuration
            dense_config = {
                "collection_name": self.dense_collection,
                "vectors": {
                    "size": 3072,  # text-embedding-3-large
                    "distance": "Cosine"
                },
                "indexed_payload_config": {
                    "indexed_fields": ["patient_id", "data_type", "timestamp"]
                }
            }

            # Sparse collection configuration
            sparse_config = {
                "collection_name": self.sparse_collection,
                "vectors": {
                    "size": 512,  # BM25 sparse vectors
                    "distance": "Cosine",
                    "sparse": True
                }
            }

            logger.info("Collections initialized successfully")

        except Exception as e:
            logger.error(f"Collection initialization error: {str(e)}")

    async def store_embedding(
        self,
        embedding_id: str,
        patient_id: str,
        dense_vector: List[float],
        sparse_vector: Dict[int, float],
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Store embeddings in Qdrant
        Shows storage reasoning
        """

        reasoning = f"""
        EMBEDDING STORAGE REASONING:
        1. Vector preparation:
           - Normalize dense vectors L2
           - Verify dimensions (3072 for dense)
           - Validate sparse vector format
        
        2. Metadata enrichment:
           - Add timestamps for temporal search
           - Include patient_id for filtering
           - Store data_type for search refinement
           - Track data modality
        
        3. Dual storage:
           - Dense vector: Semantic similarity search
           - Sparse vector: Keyword/BM25 search
           - Hybrid: Combined relevance scoring
        
        4. Indexing strategy:
           - Index patient_id for fast patient queries
           - Index timestamp for temporal range queries
           - Index data_type for modality filtering
        
        5. Audit trail:
           - Log storage operation
           - Track operation timestamp
           - Record user/system that initiated
        """

        try:
            storage_entry = {
                "embedding_id": embedding_id,
                "patient_id": patient_id,
                "dense_vector_dims": len(dense_vector),
                "sparse_vector_terms": len(sparse_vector),
                "metadata": metadata,
                "stored_at": datetime.now().isoformat(),
                "reasoning": reasoning
            }

            # Log to audit trail
            self.audit_trail.append({
                "operation": "store_embedding",
                "entry": storage_entry,
                "timestamp": datetime.now().isoformat()
            })

            # In production: Write to Qdrant
            logger.info(f"Stored embedding: {embedding_id}")

            return True

        except Exception as e:
            logger.error(f"Storage error: {str(e)}")
            return False

    async def hybrid_search(
        self,
        patient_id: str,
        query_dense: List[float],
        query_sparse: Dict[int, float],
        filters: Optional[Dict[str, Any]] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid search: combines dense + sparse vectors
        Shows search reasoning
        """

        reasoning = f"""
        HYBRID SEARCH REASONING:
        1. Dense search (semantic):
           - Query vector: {len(query_dense)} dimensions
           - Distance metric: Cosine similarity
           - Captures meaning and context
           - Example: "chest pain" matches "angina"
        
        2. Sparse search (keyword):
           - Query terms: {len(query_sparse)} keywords
           - Distance metric: BM25
           - Captures exact terminology
           - Example: "Aspirin 500mg" exact match
        
        3. Score combination:
           - Dense score weight: 0.6 (semantic importance)
           - Sparse score weight: 0.4 (keyword specificity)
           - Combined: 0.6*dense_score + 0.4*sparse_score
        
        4. Filtering:
           - Patient ID: Isolate single patient data
           - Date range: Temporal filtering (if temporal_config enabled)
           - Data type: Modality-specific search
        
        5. Ranking:
           - Sort by combined score
           - Return top-k results (default 5)
           - Include relevance explanations
        """

        try:
            # In production: Execute Qdrant search
            search_result = {
                "patient_id": patient_id,
                "query_type": "hybrid",
                "dense_weight": 0.6,
                "sparse_weight": 0.4,
                "filters_applied": filters,
                "top_k": top_k,
                "results": [],  # Would be populated from Qdrant
                "search_reasoning": reasoning
            }

            # Log search
            self.audit_trail.append({
                "operation": "hybrid_search",
                "patient_id": patient_id,
                "query_type": "hybrid",
                "timestamp": datetime.now().isoformat(),
                "top_k": top_k
            })

            logger.info(f"Hybrid search for patient {patient_id}: {len(search_result['results'])} results")

            return search_result.get("results", [])

        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []

    async def temporal_search(
        self,
        patient_id: str,
        query_embedding: List[float],
        time_window_days: int = 90,
        similarity_decay: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search across patient timeline with temporal relevance
        Shows temporal reasoning
        """

        reasoning = f"""
        TEMPORAL SEARCH REASONING:
        1. Time window definition:
           - Current date: {datetime.now().isoformat()}
           - Search window: {time_window_days} days back
           - Allows temporal continuity in disease progression
        
        2. Similarity calculation:
           - Base similarity: Cosine distance
           - Temporal decay: More recent = higher weight
           - Decay formula: score * e^(-age_days / decay_factor)
        
        3. Timeline construction:
           - Chronological ordering
           - Gap detection (missing data periods)
           - Trend identification
        
        4. Clinical significance:
           - Recent findings: Higher priority
           - Chronic patterns: Also valuable
           - Acute changes: Flagged for attention
        
        5. Continuity assessment:
           - Disease progression tracking
           - Intervention effectiveness
           - Pattern recognition across time
        """

        try:
            cutoff_date = datetime.now() - timedelta(days=time_window_days)

            # In production: Query with temporal filtering
            results = []

            logger.info(f"Temporal search for {patient_id} with decay={similarity_decay}")

            return results

        except Exception as e:
            logger.error(f"Temporal search error: {str(e)}")
            return []

    async def reinforce_memory(
        self,
        embedding_id: str,
        feedback_type: str,
        confidence_boost: float = 0.1
    ) -> bool:
        """
        Reinforce memory based on doctor feedback
        Used in Agent 3 feedback loop
        Shows memory update reasoning
        """

        reasoning = f"""
        MEMORY REINFORCEMENT REASONING:
        1. Feedback assessment:
           - Type: {feedback_type} (correct/partial/wrong)
           - Confidence adjustment: {confidence_boost}
        
        2. Confidence update:
           - Correct: Increase confidence by {confidence_boost}
           - Partial: Increase by {confidence_boost * 0.5}
           - Wrong: Decrease by {confidence_boost * 0.8}
        
        3. Weight adjustment:
           - Higher confidence → higher search weight
           - Lower confidence → lower priority in future searches
           - Prevents reinforcing errors
        
        4. Audit trail:
           - Record feedback source (doctor name)
           - Timestamp of feedback
           - Previous confidence score
           - New confidence score
        
        5. Learning loop:
           - Continuous improvement
           - Error correction
           - System adaptation
        """

        try:
            update_entry = {
                "embedding_id": embedding_id,
                "feedback_type": feedback_type,
                "confidence_boost": confidence_boost,
                "operation": "memory_reinforcement",
                "timestamp": datetime.now().isoformat(),
                "reasoning": reasoning
            }

            self.audit_trail.append(update_entry)

            logger.info(f"Memory reinforced for {embedding_id}: {feedback_type}")

            return True

        except Exception as e:
            logger.error(f"Memory reinforcement error: {str(e)}")
            return False

    async def process(self, embedding_result) -> Dict[str, Any]:
        """
        Main processing function for embeddings
        Stores and indexes in Qdrant
        """
        try:
            success = await self.store_embedding(
                embedding_id=embedding_result.text_id,
                patient_id=embedding_result.metadata.get("patient_id", "unknown"),
                dense_vector=embedding_result.dense_embedding,
                sparse_vector=embedding_result.sparse_embedding,
                metadata=embedding_result.metadata
            )

            return {
                "agent": "memory_agent",
                "embedding_stored": success,
                "embedding_id": embedding_result.text_id,
                "status": "completed" if success else "failed"
            }

        except Exception as e:
            logger.error(f"Memory processing error: {str(e)}")
            return {"status": "error", "error": str(e)}

    def get_audit_trail(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve audit trail for compliance and debugging
        """
        if patient_id:
            return [
                entry for entry in self.audit_trail
                if entry.get("patient_id") == patient_id
            ]
        return self.audit_trail

    def export_audit_trail(self, filepath: str):
        """Export audit trail to JSON file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.audit_trail, f, indent=2)
            logger.info(f"Audit trail exported to {filepath}")
        except Exception as e:
            logger.error(f"Audit trail export error: {str(e)}")
