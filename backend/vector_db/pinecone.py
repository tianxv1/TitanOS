from typing import List, Dict, Any, Optional
from .base import VectorDBProvider, VectorSearchResult


class PineconeProvider(VectorDBProvider):
    def __init__(
        self,
        collection_name: str = "titanos-memories",
        dimension: int = 384,
        api_key: str = "",
        environment: str = "us-west1-gcp",
        cloud: str = "aws",
        **kwargs
    ):
        super().__init__(collection_name, dimension, **kwargs)
        self.api_key = api_key
        self.environment = environment
        self.cloud = cloud
        self.client = None
        self.index = None

    def connect(self) -> bool:
        try:
            from pinecone import Pinecone

            self.client = Pinecone(api_key=self.api_key)

            try:
                self.index = self.client.Index(self.collection_name)
            except:
                self.index = None

            return True
        except ImportError:
            print("Pinecone client not installed. Install with: pip install pinecone-client")
            return False
        except Exception as e:
            print(f"Failed to connect to Pinecone: {e}")
            return False

    def disconnect(self):
        self.client = None
        self.index = None

    def create_collection(self, if_not_exists: bool = True) -> bool:
        if not self.client:
            return False

        try:
            existing_indexes = [idx.name for idx in self.client.list_indexes()]

            if self.collection_name in existing_indexes:
                if if_not_exists:
                    self.index = self.client.Index(self.collection_name)
                    return True
                else:
                    self.client.delete_index(self.collection_name)

            self.client.create_index(
                name=self.collection_name,
                dimension=self.dimension,
                metric="cosine",
                cloud=self.cloud,
                environment=self.environment
            )

            self.index = self.client.Index(self.collection_name)
            return True
        except Exception as e:
            print(f"Failed to create collection: {e}")
            return False

    def delete_collection(self) -> bool:
        if not self.client:
            return False

        try:
            self.client.delete_index(self.collection_name)
            self.index = None
            return True
        except Exception as e:
            print(f"Failed to delete collection: {e}")
            return False

    def collection_exists(self) -> bool:
        if not self.client:
            return False

        try:
            existing_indexes = [idx.name for idx in self.client.list_indexes()]
            return self.collection_name in existing_indexes
        except:
            return False

    def upsert(
        self,
        id: str,
        vector: List[float],
        payload: Optional[Dict[str, Any]] = None
    ) -> bool:
        if not self.index:
            return False

        try:
            self.index.upsert(
                vectors=[{
                    "id": id,
                    "values": vector,
                    "metadata": payload or {}
                }]
            )
            return True
        except Exception as e:
            print(f"Failed to upsert vector: {e}")
            return False

    def upsert_batch(self, vectors: List[Dict[str, Any]]) -> int:
        if not self.index:
            return 0

        try:
            vectors_data = [
                {
                    "id": item["id"],
                    "values": item["vector"],
                    "metadata": item.get("payload", {})
                }
                for item in vectors
            ]

            self.index.upsert(vectors=vectors_data)
            return len(vectors_data)
        except Exception as e:
            print(f"Failed to upsert batch: {e}")
            return 0

    def search(
        self,
        query_vector: List[float],
        top_k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        with_payload: bool = True
    ) -> List[VectorSearchResult]:
        if not self.index:
            return []

        try:
            search_params = {
                "vector": query_vector,
                "top_k": top_k,
                "include_values": False,
                "include_metadata": with_payload
            }

            if filters:
                search_params["filter"] = filters

            results = self.index.query(**search_params)

            matches = results.get("matches", [])
            return [
                VectorSearchResult(
                    id=match.get("id", ""),
                    score=match.get("score", 0.0),
                    payload=match.get("metadata", {}) if with_payload else {}
                )
                for match in matches
            ]
        except Exception as e:
            print(f"Failed to search: {e}")
            return []

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
        if not self.index:
            return None

        try:
            results = self.index.fetch(ids=[id])
            vectors = results.get("vectors", {})

            if id in vectors:
                vec_data = vectors[id]
                return VectorSearchResult(
                    id=id,
                    score=1.0,
                    payload=vec_data.get("metadata", {})
                )
            return None
        except:
            return None

    def delete(self, id: str) -> bool:
        if not self.index:
            return False

        try:
            self.index.delete(ids=[id])
            return True
        except:
            return False

    def count(self) -> int:
        if not self.index:
            return 0

        try:
            stats = self.index.describe_index_stats()
            return stats.get("total_vector_count", 0)
        except:
            return 0

    def health_check(self) -> Dict[str, Any]:
        if not self.client:
            return {"status": "disconnected"}

        try:
            return {
                "status": "connected",
                "type": "pinecone",
                "environment": self.environment,
                "cloud": self.cloud
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
