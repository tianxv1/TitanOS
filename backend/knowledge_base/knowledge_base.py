from typing import List, Dict, Any, Optional
from datetime import datetime
from rag.rag_engine import RAGEngine
from rag.document import Document, Chunk
import json
import os
import re


class DocumentProcessor:
    def __init__(self, rag_engine: Optional[RAGEngine] = None):
        self.rag_engine = rag_engine or RAGEngine()

    def process_markdown(self, content: str, title: str = "",
                        metadata: Optional[Dict[str, Any]] = None) -> Document:
        chunks = self._split_markdown(content)

        doc = Document(
            title=title,
            content=content,
            source_type="markdown",
            metadata=metadata or {}
        )

        for i, chunk_content in enumerate(chunks):
            chunk = Chunk(
                content=chunk_content,
                source=title or "markdown",
                source_type="markdown",
                chunk_index=i,
                metadata=metadata or {}
            )
            doc.chunks.append(chunk)

        return doc

    def _split_markdown(self, content: str, chunk_size: int = 500) -> List[str]:
        sections = re.split(r'\n(?=#+\s)', content)

        chunks = []
        current_chunk = ""

        for section in sections:
            if len(current_chunk) + len(section) <= chunk_size:
                current_chunk += section + "\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = section + "\n"

        if current_chunk:
            chunks.append(current_chunk.strip())

        if not chunks:
            words = content.split()
            for i in range(0, len(words), chunk_size):
                chunks.append(" ".join(words[i:i + chunk_size]))

        return chunks if chunks else [content]

    def process_text(self, content: str, source: str = "text",
                    metadata: Optional[Dict[str, Any]] = None) -> Document:
        words = content.split()
        chunk_size = 500
        chunks = []

        for i in range(0, len(words), chunk_size):
            chunk_words = words[i:i + chunk_size]
            chunk = Chunk(
                content=" ".join(chunk_words),
                source=source,
                source_type="text",
                chunk_index=i // chunk_size,
                metadata=metadata or {}
            )
            chunks.append(chunk)

        doc = Document(
            title=source,
            content=content,
            source_type="text",
            metadata=metadata or {}
        )
        doc.chunks = chunks

        return doc

    def process_web_content(self, url: str, content: str,
                           title: str = "") -> Document:
        content = self._clean_html(content)

        metadata = {
            "url": url,
            "title": title,
            "crawled_at": datetime.now().isoformat()
        }

        doc = self.process_text(content, source=url, metadata=metadata)

        for chunk in doc.chunks:
            chunk.source_type = "web"

        return doc

    def _clean_html(self, html: str) -> str:
        clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
        clean = re.sub(r'<[^>]+>', '', clean)
        clean = re.sub(r'\s+', ' ', clean)
        clean = clean.strip()

        return clean


class KnowledgeBase:
    def __init__(self, storage_path: str = "database/knowledge_base.json"):
        self.storage_path = storage_path
        self.documents: Dict[str, Document] = {}
        self.rag_engine = RAGEngine()
        self.processor = DocumentProcessor(self.rag_engine)
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for doc_data in data.get("documents", []):
                        doc = Document.from_dict(doc_data)
                        self.documents[doc.id] = doc
            except Exception:
                pass

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "documents": [d.to_dict() for d in self.documents.values()]
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_markdown(self, content: str, title: str = "",
                    metadata: Optional[Dict[str, Any]] = None) -> Document:
        doc = self.processor.process_markdown(content, title, metadata)
        self.documents[doc.id] = doc
        self.rag_engine.add_document(doc)
        self._save()
        return doc

    def add_text(self, content: str, title: str = "",
                metadata: Optional[Dict[str, Any]] = None) -> Document:
        doc = self.processor.process_text(content, source=title or "text", metadata=metadata)
        self.documents[doc.id] = doc
        self.rag_engine.add_document(doc)
        self._save()
        return doc

    def add_web_content(self, url: str, content: str,
                       title: str = "") -> Document:
        doc = self.processor.process_web_content(url, content, title)
        self.documents[doc.id] = doc
        self.rag_engine.add_document(doc)
        self._save()
        return doc

    def query(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        return self.rag_engine.query(question, top_k=top_k)

    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        return self.rag_engine.search(query, top_k=top_k)

    def get_document(self, doc_id: str) -> Optional[Document]:
        return self.documents.get(doc_id)

    def list_documents(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": doc.id,
                "title": doc.title,
                "source_type": doc.source_type,
                "source_url": doc.source_url,
                "chunk_count": len(doc.chunks),
                "created_at": doc.created_at.isoformat()
            }
            for doc in self.documents.values()
        ]

    def delete_document(self, doc_id: str) -> bool:
        if doc_id in self.documents:
            doc = self.documents[doc_id]
            self.rag_engine.delete_by_source(doc.title or doc.id)
            del self.documents[doc_id]
            self._save()
            return True
        return False

    def get_stats(self) -> Dict[str, Any]:
        total_chunks = sum(len(doc.chunks) for doc in self.documents.values())
        source_types: Dict[str, int] = {}

        for doc in self.documents.values():
            source_types[doc.source_type] = source_types.get(doc.source_type, 0) + 1

        return {
            "total_documents": len(self.documents),
            "total_chunks": total_chunks,
            "source_types": source_types,
            "rag_stats": self.rag_engine.get_stats()
        }
