from typing import List, Optional, Dict, Any, Callable
import numpy as np
import hashlib
import math


class EmbeddingService:
    def __init__(self, model: str = "simulated", dimension: int = 384):
        self.model = model
        self.dimension = dimension
        self._cache: Dict[str, List[float]] = {}

    def embed_text(self, text: str) -> List[float]:
        if not text:
            return [0.0] * self.dimension

        if text in self._cache:
            return self._cache[text]

        if self.model == "simulated":
            embedding = self._simulate_embedding(text)
        else:
            embedding = self._simulate_embedding(text)

        self._cache[text] = embedding
        return embedding

    def _simulate_embedding(self, text: str) -> List[float]:
        hash_input = text.encode('utf-8')
        seed = int(hashlib.md5(hash_input).hexdigest()[:8], 16)

        np.random.seed(seed)
        embedding = np.random.randn(self.dimension)

        magnitude = np.linalg.norm(embedding)
        if magnitude > 0:
            embedding = embedding / magnitude

        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(text) for text in texts]

    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    def compute_cosine_similarity(self, text1: str, text2: str) -> float:
        emb1 = self.embed_text(text1)
        emb2 = self.embed_text(text2)
        return self.compute_similarity(emb1, emb2)


class VectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.vectors: Dict[str, List[float]] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}

    def add(self, id: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None):
        self.vectors[id] = vector
        self.metadata[id] = metadata or {}

    def search(self, query_vector: List[float], top_k: int = 5) -> List[tuple]:
        results = []
        for vid, vector in self.vectors.items():
            similarity = self._cosine_similarity(query_vector, vector)
            results.append((vid, similarity))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        v1 = np.array(vec1)
        v2 = np.array(vec2)

        dot = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot / (norm1 * norm2))

    def delete(self, id: str) -> bool:
        if id in self.vectors:
            del self.vectors[id]
            del self.metadata[id]
            return True
        return False

    def count(self) -> int:
        return len(self.vectors)

    def clear(self):
        self.vectors.clear()
        self.metadata.clear()
