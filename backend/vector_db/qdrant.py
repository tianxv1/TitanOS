from typing import List, Dict, Any, Optional
from .base import VectorDBProvider, VectorSearchResult
import numpy as np


class QdrantProvider(VectorDBProvider):
    def __init__(
        self,
        collection_name: str = "titanos_memories",
        dimension: int = 384,
        host: str = "localhost",
        port: int = 6333,
        grpc_port: int = 6334,
        api_key: Optional[str] = None,
        distance: str = "Cosine",
        **kwargs
    ):
        super().__init__(collection_name, dimension, host, port, **kwargs)
        self.grpc_port = grpc_port
        self.api_key = api_key
        self.distance = distance
        self.client = None
        self._use_grpc = kwargs.get("use_grpc", False)

    def connect(self) -> bool:
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams

            if self._use_grpc:
                self.client = QdrantClient(
                    host=self.host,
                    port=self.port,
                    grpc_port=self.grpc_port,
                    api_key=self.api_key,
                    prefer_grpc=True
                )
            else:
                self.client = QdrantClient(
                    host=self.host,
                    port=self.port,
                    api_key=self.api_key
                )

            return True
        except ImportError:
            print("Qdrant client not installed. Install with: pip install qdrant-client")
            return False
        except Exception as e:
            print(f"Failed to connect to Qdrant: {e}")
            return False

    def disconnect(self):
        self.client = None

    def create_collection(self, if_not_exists: bool = True) -> bool:
        if not self.client:
            return False

        try:
            from qdrant_client.models import Distance, VectorParams

            distance_map = {
                "Cosine": Distance.COSINE,
                "Euclidean": Distance.EUCLID,
                "Dot": Distance.DOT
            }

            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.dimension,
                    distance=distance_map.get(self.distance, Distance.COSINE)
                )
            )
            return True
        except Exception as e:
            print(f"Failed to create collection: {e}")
            return False

    def delete_collection(self) -> bool:
        if not self.client:
            return False

        try:
            self.client.delete_collection(collection_name=self.collection_name)
            return True
        except Exception as e:
            print(f"Failed to delete collection: {e}")
            return False

    def collection_exists(self) -> bool:
        if not self.client:
            return False

        try:
            collections = self.client.get_collections().collections
            return any(c.name == self.collection_name for c in collections)
        except:
            return False

    def upsert(
        self,
        id: str,
        vector: List[float],
        payload: Optional[Dict[str, Any]] = None
    ) -> bool:
        if not self.client:
            return False

        try:
            from qdrant_client.models import PointStruct

            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=id,
                        vector=vector,
                        payload=payload or {}
                    )
                ]
            )
            return True
        except Exception as e:
            print(f"Failed to upsert vector: {e}")
            return False

    def upsert_batch(self, vectors: List[Dict[str, Any]]) -> int:
        if not self.client:
            return 0

        try:
            from qdrant_client.models import PointStruct

            points = [
                PointStruct(
                    id=item["id"],
                    vector=item["vector"],
                    payload=item.get("payload", {})
                )
                for item in vectors
            ]

            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return len(points)
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
        if not self.client:
            return []

        try:
            from qdrant_client.models import Filter, FieldCondition, MatchValue

            search_params = {"limit": top_k}

            if filters:
                must_conditions = []
                for key, value in filters.items():
                    must_conditions.append(
                        FieldCondition(
                            key=key,
                            match=MatchValue(value=value)
                        )
                    )
                search_params["filter"] = Filter(must=must_conditions)

            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                with_payload=with_payload,
                **search_params
            )

            return [
                VectorSearchResult(
                    id=str(r.id),
                    score=r.score,
                    payload=r.payload or {}
                )
                for r in results
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
        if not self.client:
            return None

        try:
            results = self.client.retrieve(
                collection_name=self.collection_name,
                ids=[id]
            )

            if results:
                r = results[0]
                return VectorSearchResult(
                    id=str(r.id),
                    score=1.0,
                    payload=r.payload or {}
                )
            return None
        except:
            return None

    def delete(self, id: str) -> bool:
        if not self.client:
            return False

        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[id]
            )
            return True
        except:
            return False

    def count(self) -> int:
        if not self.client:
            return 0

        try:
            return self.client.get_collection(collection_name=self.collection_name).points_count
        except:
            return 0

    def health_check(self) -> Dict[str, Any]:
        if not self.client:
            return {"status": "disconnected"}

        try:
            collections = self.client.get_collections()
            return {
                "status": "connected",
                "type": "qdrant",
                "host": self.host,
                "port": self.port,
                "collections": len(collections.collections)
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
