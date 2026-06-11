from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class VectorSearchResult:
    id: str
    score: float
    payload: Dict[str, Any]


class VectorDBProvider(ABC):
    def __init__(
        self,
        collection_name: str = "titanos_memories",
        dimension: int = 384,
        host: str = "localhost",
        port: int = 6333,
        **kwargs
    ):
        self.collection_name = collection_name
        self.dimension = dimension
        self.host = host
        self.port = port
        self.config = kwargs

    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def create_collection(self, if_not_exists: bool = True) -> bool:
        pass

    @abstractmethod
    def delete_collection(self) -> bool:
        pass

    @abstractmethod
    def collection_exists(self) -> bool:
        pass

    @abstractmethod
    def upsert(
        self,
        id: str,
        vector: List[float],
        payload: Optional[Dict[str, Any]] = None
    ) -> bool:
        pass

    @abstractmethod
    def upsert_batch(
        self,
        vectors: List[Dict[str, Any]]
    ) -> int:
        pass

    @abstractmethod
    def search(
        self,
        query_vector: List[float],
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        with_payload: bool = True
    ) -> List[VectorSearchResult]:
        pass

    @abstractmethod
    def search_by_text(
        self,
        query_text: str,
        embed_func,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[VectorSearchResult]:
        pass

    @abstractmethod
    def get(self, id: str) -> Optional[VectorSearchResult]:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass

    @abstractmethod
    def count(self) -> int:
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        pass


class InMemoryVectorDB(VectorDBProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._vectors: Dict[str, tuple] = {}

    def connect(self) -> bool:
        return True

    def disconnect(self):
        self._vectors.clear()

    def create_collection(self, if_not_exists: bool = True) -> bool:
        return True

    def delete_collection(self) -> bool:
        self._vectors.clear()
        return True

    def collection_exists(self) -> bool:
        return True

    def upsert(
        self,
        id: str,
        vector: List[float],
        payload: Optional[Dict[str, Any]] = None
    ) -> bool:
        self._vectors[id] = (vector, payload or {})
        return True

    def upsert_batch(self, vectors: List[Dict[str, Any]]) -> int:
        count = 0
        for item in vectors:
            if self.upsert(item["id"], item["vector"], item.get("payload")):
                count += 1
        return count

    def search(
        self,
        query_vector: List[float],
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        with_payload: bool = True
    ) -> List[VectorSearchResult]:
        import numpy as np

        results = []
        query_arr = np.array(query_vector)

        for vid, (vec, payload) in self._vectors.items():
            vec_arr = np.array(vec)
            similarity = float(np.dot(query_arr, vec_arr) / (np.linalg.norm(query_arr) * np.linalg.norm(vec_arr) + 1e-8))
            results.append(VectorSearchResult(id=vid, score=similarity, payload=payload))

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]

    def search_by_text(
        self,
        query_text: str,
        embed_func,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[VectorSearchResult]:
        query_vector = embed_func(query_text)
        return self.search(query_vector, top_k, filters)

    def get(self, id: str) -> Optional[VectorSearchResult]:
        if id in self._vectors:
            vector, payload = self._vectors[id]
            return VectorSearchResult(id=id, score=1.0, payload=payload)
        return None

    def delete(self, id: str) -> bool:
        if id in self._vectors:
            del self._vectors[id]
            return True
        return False

    def count(self) -> int:
        return len(self._vectors)

    def health_check(self) -> Dict[str, Any]:
        return {
            "status": "healthy",
            "type": "in_memory",
            "count": self.count()
        }
