from typing import Dict, Optional, Any, List
from .base import VectorDBProvider, VectorSearchResult, InMemoryVectorDB
from .qdrant import QdrantProvider
from .weaviate import WeaviateProvider
from .pinecone import PineconeProvider


class VectorDBManager:
    PROVIDERS = {
        "in_memory": InMemoryVectorDB,
        "qdrant": QdrantProvider,
        "weaviate": WeaviateProvider,
        "pinecone": PineconeProvider
    }

    def __init__(self):
        self.current_provider: Optional[VectorDBProvider] = None
        self.current_type: str = "in_memory"
        self.embed_service = None

    def initialize(
        self,
        provider_type: str = "in_memory",
        embed_service=None,
        **config
    ) -> bool:
        self.embed_service = embed_service

        if provider_type not in self.PROVIDERS:
            print(f"Unknown provider type: {provider_type}")
            print(f"Available providers: {list(self.PROVIDERS.keys())}")
            return False

        provider_class = self.PROVIDERS[provider_type]
        self.current_provider = provider_class(**config)

        if not self.current_provider.connect():
            print(f"Failed to connect to {provider_type}")
            self.current_provider = None
            return False

        if not self.current_provider.create_collection():
            print(f"Failed to create collection in {provider_type}")
            return False

        self.current_type = provider_type
        print(f"VectorDB initialized with {provider_type}")
        return True

    def upsert_memory(
        self,
        memory_id: str,
        content: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        if not self.current_provider:
            return False

        payload = {
            "content": content,
            "memory_id": memory_id
        }

        if metadata:
            payload.update(metadata)

        return self.current_provider.upsert(memory_id, embedding, payload)

    def search_memories(
        self,
        query: str,
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[VectorSearchResult]:
        if not self.current_provider or not self.embed_service:
            return []

        query_vector = self.embed_service.embed_text(query)
        return self.current_provider.search(query_vector, top_k, filters)

    def semantic_search(
        self,
        query: str,
        top_k: int = 10
    ) -> List[VectorSearchResult]:
        return self.search_memories(query, top_k)

    def delete_memory(self, memory_id: str) -> bool:
        if not self.current_provider:
            return False
        return self.current_provider.delete(memory_id)

    def get_memory(self, memory_id: str) -> Optional[VectorSearchResult]:
        if not self.current_provider:
            return None
        return self.current_provider.get(memory_id)

    def count_memories(self) -> int:
        if not self.current_provider:
            return 0
        return self.current_provider.count()

    def health_check(self) -> Dict[str, Any]:
        if not self.current_provider:
            return {"status": "not_initialized"}

        return {
            "provider": self.current_type,
            **self.current_provider.health_check()
        }

    def switch_provider(self, provider_type: str, **config) -> bool:
        if self.current_provider:
            self.current_provider.disconnect()

        return self.initialize(provider_type, self.embed_service, **config)

    def get_stats(self) -> Dict[str, Any]:
        if not self.current_provider:
            return {"total": 0}

        return {
            "total": self.current_provider.count(),
            "provider": self.current_type,
            "health": self.current_provider.health_check()
        }


vector_db_manager = VectorDBManager()
