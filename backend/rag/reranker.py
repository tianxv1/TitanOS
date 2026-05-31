from typing import List, Dict, Any
from .document import Chunk, RetrievalResult


class Reranker:
    def __init__(self, model: str = "cross_encoder"):
        self.model = model

    def rerank(self, query: str, results: List[RetrievalResult],
               top_k: int = 5, with_scores: bool = True) -> List[RetrievalResult]:
        if not results:
            return []

        reranked = []
        for result in results:
            score = self._calculate_relevance(query, result.chunk)
            reranked.append((result, score))

        reranked.sort(key=lambda x: x[1], reverse=True)

        final_results = []
        for rank, (result, score) in enumerate(reranked[:top_k]):
            result.rank = rank + 1
            if with_scores:
                result.score = round(score, 4)
            final_results.append(result)

        return final_results

    def _calculate_relevance(self, query: str, chunk: Chunk) -> float:
        query_terms = set(query.lower().split())
        content_terms = set(chunk.content.lower().split())

        exact_matches = len(query_terms & content_terms) / len(query_terms) if query_terms else 0

        query_word_set = set(query.lower().replace("?", "").replace(".", "").split())
        content_lower = chunk.content.lower()

        partial_matches = 0
        for word in query_word_set:
            if len(word) > 2 and word in content_lower:
                partial_matches += 1

        partial_score = partial_matches / len(query_word_set) if query_word_set else 0

        position_score = 1.0
        content_lower = chunk.content.lower()
        query_lower = query.lower()
        first_pos = content_lower.find(query_lower.split()[0] if query_lower.split() else "")
        if first_pos > -1:
            position_score = 1.0 - (first_pos / len(chunk.content)) * 0.3

        length_penalty = 1.0
        if len(chunk.content) > 500:
            length_penalty = 0.9
        elif len(chunk.content) < 50:
            length_penalty = 0.7

        final_score = (
            exact_matches * 0.5 +
            partial_score * 0.3 +
            position_score * 0.1 +
            length_penalty * 0.1
        )

        return round(final_score, 4)

    def batch_rerank(self, queries: List[str],
                     results_list: List[List[RetrievalResult]],
                     top_k: int = 5) -> List[List[RetrievalResult]]:
        return [
            self.rerank(query, results, top_k)
            for query, results in zip(queries, results_list)
        ]


class ContextBuilder:
    def __init__(self, max_tokens: int = 4000, overlap_tokens: int = 200):
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens

    def build_context(self, results: List[RetrievalResult],
                     query: str,
                     include_metadata: bool = True) -> str:
        if not results:
            return ""

        context_parts = []
        context_parts.append(f"查询: {query}\n")

        current_tokens = 0

        for result in results:
            chunk_text = result.chunk.content
            chunk_tokens = len(chunk_text) // 4

            if current_tokens + chunk_tokens > self.max_tokens:
                break

            context_parts.append(f"[来源: {result.chunk.source}] (相关度: {result.score:.2f})")
            context_parts.append(chunk_text)
            context_parts.append("")

            current_tokens += chunk_tokens

        context = "\n".join(context_parts)
        return context.strip()

    def build_with_citations(self, results: List[RetrievalResult],
                           query: str) -> Dict[str, Any]:
        if not results:
            return {"context": "", "citations": []}

        citations = []
        context_parts = [f"基于以下参考资料回答问题: {query}\n"]

        for idx, result in enumerate(results):
            citation = {
                "index": idx + 1,
                "source": result.chunk.source,
                "source_type": result.chunk.source_type,
                "content": result.chunk.content[:200] + "..." if len(result.chunk.content) > 200 else result.chunk.content,
                "relevance_score": result.score
            }
            citations.append(citation)

            context_parts.append(f"[{idx + 1}] {result.chunk.content}")

        return {
            "context": "\n".join(context_parts),
            "citations": citations,
            "query": query
        }

    def build_few_shot_context(self, results: List[RetrievalResult],
                              query: str,
                              examples: List[Dict[str, str]] = None) -> str:
        context_parts = []

        if examples:
            context_parts.append("示例:")
            for ex in examples[:2]:
                context_parts.append(f"问题: {ex.get('question', '')}")
                context_parts.append(f"答案: {ex.get('answer', '')}")
                context_parts.append("")

        context_parts.append(f"当前问题: {query}")
        context_parts.append("\n相关资料:")
        context_parts.append(self.build_context(results, query, include_metadata=True))

        return "\n".join(context_parts)
