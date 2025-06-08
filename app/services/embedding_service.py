from sentence_transformers import SentenceTransformer
import numpy as np
import json
from typing import List
from app.core.config import settings

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
    
    def generate_embedding(self, text: str) -> str:
        """Generate embedding for a given text and return it as a JSON string."""
        embedding = self.model.encode(text)
        return json.dumps(embedding.tolist())
    
    def generate_embeddings(self, texts: List[str]) -> List[str]:
        """Generate embeddings for multiple texts."""
        embeddings = self.model.encode(texts)
        return [json.dumps(emb.tolist()) for emb in embeddings]
    
    def cosine_similarity(self, embedding1: str, embedding2: str) -> float:
        """Calculate cosine similarity between two embeddings."""
        emb1 = np.array(json.loads(embedding1))
        emb2 = np.array(json.loads(embedding2))
        return float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))
    
    def find_similar_documents(self, query_embedding: str, document_embeddings: List[str], top_k: int = 3) -> List[int]:
        """Find the most similar documents to a query embedding."""
        similarities = [
            self.cosine_similarity(query_embedding, doc_emb)
            for doc_emb in document_embeddings
        ]
        return np.argsort(similarities)[-top_k:][::-1].tolist()

embedding_service = EmbeddingService() 