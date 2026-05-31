from typing import List, Optional, Dict, Any
from .document import Chunk, Document, RetrievalResult
from .embedding import EmbeddingService
from .retrieval import RetrievalEngine
from .reranker import Reranker, ContextBuilder


class RAGEngine:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.retrieval_engine = RetrievalEngine(
            embedding_service=self.embedding_service
        )
        self.reranker = Reranker()
        self.context_builder = ContextBuilder()

    def add_document(self, document: Document) -> Document:
        for chunk in document.chunks:
            if not chunk.embedding:
                chunk.embedding = self.embedding_service.embed_text(chunk.content)

        self.retrieval_engine.add_chunks(document.chunks)
        return document

    def add_text(self, text: str, source: str = "user_input",
                metadata: Optional[Dict[str, Any]] = None,
                chunk_size: int = 500,
                overlap: int = 50) -> List[Chunk]:
        chunks = self._chunk_text(text, chunk_size, overlap)

        for i, chunk_content in enumerate(chunks):
            chunk = Chunk(
                content=chunk_content,
                source=source,
                source_type="text",
                chunk_index=i,
                metadata=metadata or {}
            )
            chunk.embedding = self.embedding_service.embed_text(chunk_content)
            self.retrieval_engine.add_chunk(chunk)

        return chunks

    def _chunk_text(self, text: str, chunk_size: int = 500,
                   overlap: int = 50) -> List[str]:
        if not text:
            return []

        words = text.split()
        chunks = []
        start = 0

        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunks.append(" ".join(chunk_words))

            if end >= len(words):
                break

            start = end - overlap

        return chunks

    def query(self, question: str, top_k: int = 5,
              use_rerank: bool = True,
              use_hybrid: bool = True,
              include_citations: bool = True) -> Dict[str, Any]:
        if use_hybrid:
            initial_results = self.retrieval_engine.hybrid_search(
                question, top_k=top_k * 2
            )
        else:
            initial_results = self.retrieval_engine.retrieve(
                question, top_k=top_k * 2
            )

        if use_rerank and initial_results:
            results = self.reranker.rerank(question, initial_results, top_k=top_k)
        else:
            results = initial_results[:top_k]

        if include_citations:
            context_data = self.context_builder.build_with_citations(results, question)
        else:
            context = self.context_builder.build_context(results, question)
            context_data = {"context": context, "query": question}

        return {
            "answer": self._generate_answer(question, context_data["context"]),
            "context": context_data["context"],
            "citations": context_data.get("citations", []),
            "sources": [r.chunk.source for r in results],
            "total_results": len(results)
        }

    def _generate_answer(self, question: str, context: str) -> str:
        if not context:
            return "抱歉，我没有找到与您问题相关的资料。"

        answer = f"根据我检索到的资料，关于「{question}」，以下是相关信息：\n\n"
        answer += context

        return answer

    def search(self, query: str, filters: Optional[Dict[str, Any]] = None,
               top_k: int = 10) -> List[Dict[str, Any]]:
        results = self.retrieval_engine.retrieve(query, top_k=top_k, filters=filters)

        return [
            {
                "content": r.chunk.content,
                "source": r.chunk.source,
                "source_type": r.chunk.source_type,
                "score": r.score,
                "rank": r.rank,
                "highlights": r.highlights,
                "metadata": r.chunk.metadata
            }
            for r in results
        ]

    def get_stats(self) -> Dict[str, Any]:
        return {
            "retrieval_stats": self.retrieval_engine.get_stats(),
            "reranker_model": self.reranker.model,
            "context_max_tokens": self.context_builder.max_tokens
        }

    def delete_by_source(self, source: str) -> int:
        deleted = 0
        chunk_ids = [cid for cid, c in self.retrieval_engine.chunks.items()
                    if c.source == source]

        for chunk_id in chunk_ids:
            if self.retrieval_engine.delete_chunk(chunk_id):
                deleted += 1

        return deleted
