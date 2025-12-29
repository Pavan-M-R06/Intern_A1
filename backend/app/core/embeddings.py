"""
Embedding Generation
Generate vector embeddings for semantic search using Sentence Transformers
"""
from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np


class EmbeddingGenerator:
    """Generate embeddings for text using sentence transformers"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding model
        all-MiniLM-L6-v2: Fast, 384 dimensions, good for semantic search
        """
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = 384
    
    def generate(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Generate embeddings for text
        
        Args:
            text: Single string or list of strings
            
        Returns:
            Single embedding or list of embeddings
        """
        if isinstance(text, str):
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        else:
            embeddings = self.model.encode(text, convert_to_numpy=True)
            return embeddings.tolist()
    
    def generate_concept_embedding(self, name: str, definition: str = "") -> List[float]:
        """Generate embedding for a concept combining name and definition"""
        text = f"{name}. {definition}" if definition else name
        return self.generate(text)
    
    def generate_log_embedding(self, raw_text: str) -> List[float]:
        """Generate embedding for a daily log entry"""
        return self.generate(raw_text)


# Global instance
embedding_generator = EmbeddingGenerator()
