"""
Qdrant Vector Store Setup
Initialize and manage Qdrant collections for semantic search
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any
import uuid

from app.config import settings


class QdrantVectorStore:
    """Manage Qdrant vector database for semantic search"""
    
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key if settings.qdrant_api_key else None
        )
        self.concept_collection = "concept_embeddings"
        self.log_collection = "log_embeddings"
        
    def initialize_collections(self):
        """Create Qdrant collections if they don't exist"""
        # Concept embeddings collection (384 dim for all-MiniLM-L6-v2)
        if not self.client.collection_exists(self.concept_collection):
            self.client.create_collection(
                collection_name=self.concept_collection,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print(f"✅ Created collection: {self.concept_collection}")
        
        # Log embeddings collection
        if not self.client.collection_exists(self.log_collection):
            self.client.create_collection(
                collection_name=self.log_collection,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print(f"✅ Created collection: {self.log_collection}")
    
    def add_concept_embedding(self, concept_id: str, embedding: List[float], 
                            name: str, definition: str, category: str):
        """Store concept embedding in Qdrant"""
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "concept_id": concept_id,
                "name": name,
                "definition": definition,
                "category": category
            }
        )
        self.client.upsert(
            collection_name=self.concept_collection,
            points=[point]
        )
    
    def add_log_embedding(self, log_id: str, embedding: List[float],
                        log_date: str, summary: str, concepts: List[str]):
        """Store daily log embedding in Qdrant"""
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "log_id": log_id,
                "log_date": log_date,
                "summary": summary,
                "concepts": concepts
            }
        )
        self.client.upsert(
            collection_name=self.log_collection,
            points=[point]
        )
    
    def search_similar_concepts(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar concepts using vector similarity"""
        results = self.client.search(
            collection_name=self.concept_collection,
            query_vector=query_embedding,
            limit=limit
        )
        return [
            {
                "score": hit.score,
                **hit.payload
            }
            for hit in results
        ]
    
    def search_similar_logs(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar daily logs using vector similarity"""
        results = self.client.search(
            collection_name=self.log_collection,
            query_vector=query_embedding,
            limit=limit
        )
        return [
            {
                "score": hit.score,
                **hit.payload
            }
            for hit in results
        ]


# Global instance
vector_store = QdrantVectorStore()
