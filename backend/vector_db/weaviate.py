from typing import List, Dict, Any, Optional
from .base import VectorDBProvider, VectorSearchResult
import json


class WeaviateProvider(VectorDBProvider):
    def __init__(
        self,
        collection_name: str = "TitanosMemories",
        dimension: int = 384,
        host: str = "localhost",
        port: int = 8080,
        api_key: Optional[str] = None,
        model: str = "text-embedding-ada-002",
        **kwargs
    ):
        super().__init__(collection_name, dimension, host, port, **kwargs)
        self.api_key = api_key
        self.model = model
        self.client = None
        self._scheme = kwargs.get("scheme", "http")

    def connect(self) -> bool:
        try:
            import weaviate
            from weaviate.auth import AuthApiKey

            auth_config = None
            if self.api_key:
                auth_config = AuthApiKey(api_key=self.api_key)

            self.client = weaviate.Client(
                url=f"{self._scheme}://{self.host}:{self.port}",
                auth_client_secret=auth_config,
                additional_headers={
                    "X-OpenAI-Api-Key": self.api_key if self.api_key else ""
                } if self.api_key else {}
            )

            return True
        except ImportError:
            print("Weaviate client not installed. Install with: pip install weaviate-client")
            return False
        except Exception as e:
            print(f"Failed to connect to Weaviate: {e}")
            return False

    def disconnect(self):
        self.client = None

    def create_collection(self, if_not_exists: bool = True) -> bool:
        if not self.client:
            return False

        try:
            if self.collection_exists() and if_not_exists:
                return True

            class_obj = {
                "Memory": {
                    "vectorizer": "text2vec-transformers",
                    "vectorIndexConfig": {
                        "distance": "cosine"
                    },
                    "properties": [
                        {"name": "content", "dataType": ["text"]},
                        {"name": "tags", "dataType": ["text[]"]},
                        {"name": "importance", "dataType": ["number"]},
                        {"name": "memory_id", "dataType": ["text"]},
                        {"name": "created_at", "dataType": ["date"]}
                    ]
                }
            }

            if if_not_exists:
                self.client.schema.create_class(class_obj)
            else:
                self.client.schema.delete_class(self.collection_name)
                self.client.schema.create_class(class_obj)

            return True
        except Exception as e:
            print(f"Failed to create collection: {e}")
            return False

    def delete_collection(self) -> bool:
        if not self.client:
            return False

        try:
            self.client.schema.delete_class(self.collection_name)
            return True
        except Exception as e:
            print(f"Failed to delete collection: {e}")
            return False

    def collection_exists(self) -> bool:
        if not self.client:
            return False

        try:
            schema = self.client.schema.get()
            return any(c["class"] == self.collection_name for c in schema.get("classes", []))
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
            data_object = {
                "content": payload.get("content", "") if payload else "",
                "tags": payload.get("tags", []) if payload else [],
                "importance": payload.get("importance", 0.5) if payload else 0.5,
                "memory_id": id,
                "created_at": payload.get("created_at", "") if payload else ""
            }

            self.client.data_object.create(
                class_name=self.collection_name,
                data_object=data_object,
                vector=vector
            )
            return True
        except Exception as e:
            print(f"Failed to upsert vector: {e}")
            return False

    def upsert_batch(self, vectors: List[Dict[str, Any]]) -> int:
        if not self.client:
            return 0

        try:
            objects = []
            for item in vectors:
                objects.append({
                    "class": self.collection_name,
                    "properties": {
                        "content": item.get("payload", {}).get("content", "") if item.get("payload") else "",
                        "tags": item.get("payload", {}).get("tags", []) if item.get("payload") else [],
                        "importance": item.get("payload", {}).get("importance", 0.5) if item.get("payload") else 0.5,
                        "memory_id": item["id"],
                        "created_at": item.get("payload", {}).get("created_at", "") if item.get("payload") else ""
                    },
                    "vector": item["vector"]
                })

            self.client.batch.add_objects(objects)
            self.client.batch.create_objects()
            return len(objects)
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
            near_vector = {"vector": query_vector}

            where_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append({
                        "path": [key],
                        "operator": "Equal",
                        "valueString": str(value)
                    })
                if conditions:
                    where_filter = {"operator": "And", "operands": conditions}

            search_params = {
                "limit": top_k,
                "nearVector": near_vector
            }

            if where_filter:
                search_params["where"] = where_filter

            if with_payload:
                search_params["returnProperties"] = ["content", "tags", "importance", "memory_id", "created_at"]

            results = self.client.query.get(
                class_name=self.collection_name,
                properties=["content", "tags", "importance", "memory_id", "created_at"]
            ).with_near_vector(near_vector).with_limit(top_k).do()

            memories = results.get("data", {}).get("Get", {}).get(self.collection_name, [])
            return [
                VectorSearchResult(
                    id=m.get("memory_id", ""),
                    score=1.0,
                    payload={
                        "content": m.get("content", ""),
                        "tags": m.get("tags", []),
                        "importance": m.get("importance", 0.5),
                        "created_at": m.get("created_at", "")
                    }
                )
                for m in memories
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
            result = self.client.data_object.get_by_id(
                uuid=id,
                class_name=self.collection_name
            )

            if result:
                props = result.get("properties", {})
                return VectorSearchResult(
                    id=props.get("memory_id", id),
                    score=1.0,
                    payload={
                        "content": props.get("content", ""),
                        "tags": props.get("tags", []),
                        "importance": props.get("importance", 0.5),
                        "created_at": props.get("created_at", "")
                    }
                )
            return None
        except:
            return None

    def delete(self, id: str) -> bool:
        if not self.client:
            return False

        try:
            self.client.data_object.delete(
                uuid=id,
                class_name=self.collection_name
            )
            return True
        except:
            return False

    def count(self) -> int:
        if not self.client:
            return 0

        try:
            result = self.client.query.aggregate(self.collection_name).with_meta_count().do()
            return result.get("data", {}).get("Aggregate", {}).get(self.collection_name, [{}])[0].get("meta", {}).get("count", 0)
        except:
            return 0

    def health_check(self) -> Dict[str, Any]:
        if not self.client:
            return {"status": "disconnected"}

        try:
            meta = self.client.get_meta()
            return {
                "status": "connected",
                "type": "weaviate",
                "host": self.host,
                "port": self.port,
                "version": meta.get("version", "unknown")
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
