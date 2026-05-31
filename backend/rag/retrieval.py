from typing import List, Optional, Dict, Any, Callable
from .document import Chunk, RetrievalResult
from .embedding import EmbeddingService, VectorStore
import json
import os


class RetrievalEngine:
    def __init__(self, vector_store: Optional[VectorStore] = None,
                 embedding_service: Optional[EmbeddingService] = None):
        self.vector_store = vector_store or VectorStore()
        self.embedding_service = embedding_service or EmbeddingService()
        self.chunks: Dict[str, Chunk] = {}
        self._load_index()

    def _load_index(self):
        index_path = "database/rag_index.json"
        if os.path.exists(index_path):
            try:
                with open(index_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for chunk_data in data.get("chunks", []):
                        chunk = Chunk.from_dict(chunk_data)
                        self.chunks[chunk.id] = chunk
                        if chunk.embedding:
                            self.vector_store.add(chunk.id, chunk.embedding, chunk.metadata)
            except Exception:
                pass

    def _save_index(self):
        os.makedirs("database", exist_ok=True)
        index_path = "database/rag_index.json"
        data = {
            "chunks": [c.to_dict() for c in self.chunks.values()]
        }
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_chunk(self, chunk: Chunk):
        self.chunks[chunk.id] = chunk
        if chunk.embedding:
            self.vector_store.add(chunk.id, chunk.embedding, chunk.metadata)
        self._save_index()

    def add_chunks(self, chunks: List[Chunk]):
        for chunk in chunks:
            self.add_chunk(chunk)

    def retrieve(self, query: str, top_k: int = 5,
                 min_score: float = 0.0,
                 filters: Optional[Dict[str, Any]] = None) -> List[RetrievalResult]:
        query_embedding = self.embedding_service.embed_text(query)

        raw_results = self.vector_store.search(query_embedding, top_k * 2)

        results = []
        for rank, (chunk_id, score) in enumerate(raw_results):
            if score < min_score:
                continue

            chunk = self.chunks.get(chunk_id)
            if not chunk:
                continue

            if filters:
                if not self._matches_filters(chunk, filters):
                    continue

            result = RetrievalResult(
                chunk=chunk,
                score=round(score, 4),
                rank=rank + 1,
                highlights=self._extract_highlights(chunk.content, query)
            )
            results.append(result)

            if len(results) >= top_k:
                break

        return results

    def _matches_filters(self, chunk: Chunk, filters: Dict[str, Any]) -> bool:
        for key, value in filters.items():
            if key == "source":
                if chunk.source != value:
                    return False
            elif key == "source_type":
                if chunk.source_type != value:
                    return False
            elif key == "metadata":
                for mkey, mvalue in value.items():
                    if chunk.metadata.get(mkey) != mvalue:
                        return False
        return True

    def _extract_highlights(self, content: str, query: str, window: int = 50) -> List[str]:
        content_lower = content.lower()
        query_lower = query.lower()

        words = query_lower.split()
        highlights = []

        for word in words:
            if len(word) < 2:
                continue
            idx = content_lower.find(word)
            if idx != -1:
                start = max(0, idx - window)
                end = min(len(content), idx + len(word) + window)
                highlight = content[start:end]
                if start > 0:
                    highlight = "..." + highlight
                if end < len(content):
                    highlight = highlight + "..."
                highlights.append(highlight)
                break

        if not highlights:
            highlights.append(content[:window * 2] + ("..." if len(content) > window * 2 else ""))

        return highlights[:3]

    def hybrid_search(self, query: str, top_k: int = 5,
                     vector_weight: float = 0.7,
                     keyword_weight: float = 0.3) -> List[RetrievalResult]:
        vector_results = self.retrieve(query, top_k * 2)
        keyword_results = self._keyword_search(query, top_k * 2)

        scores: Dict[str, float] = {}
        chunk_scores: Dict[str, float] = {}

        for result in vector_results:
            scores[result.chunk.id] = result.score * vector_weight
            chunk_scores[result.chunk.id] = result.score

        for result in keyword_results:
            chunk_id = result.chunk.id
            if chunk_id in scores:
                scores[chunk_id] += result.score * keyword_weight
            else:
                scores[chunk_id] = result.score * keyword_weight
            chunk_scores[chunk_id] = max(chunk_scores.get(chunk_id, 0), result.score)

        sorted_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for rank, (chunk_id, combined_score) in enumerate(sorted_ids):
            chunk = self.chunks.get(chunk_id)
            if chunk:
                results.append(RetrievalResult(
                    chunk=chunk,
                    score=round(combined_score, 4),
                    rank=rank + 1,
                    highlights=self._extract_highlights(chunk.content, query)
                ))

        return results

    def _keyword_search(self, query: str, top_k: int) -> List[RetrievalResult]:
        query_words = set(query.lower().split())
        results = []

        for chunk in self.chunks.values():
            content_words = set(chunk.content.lower().split())
            overlap = len(query_words & content_words)
            if overlap > 0:
                score = overlap / len(query_words)
                results.append(RetrievalResult(
                    chunk=chunk,
                    score=score,
                    rank=0
                ))

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]

    def delete_chunk(self, chunk_id: str) -> bool:
        if chunk_id in self.chunks:
            del self.chunks[chunk_id]
            self.vector_store.delete(chunk_id)
            self._save_index()
            return True
        return False

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_chunks": len(self.chunks),
            "vector_count": self.vector_store.count(),
            "sources": list(set(c.source for c in self.chunks.values())),
            "source_types": list(set(c.source_type for c in self.chunks.values()))
        }
