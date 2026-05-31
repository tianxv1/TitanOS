from datetime import datetime
from typing import List, Optional, Dict, Any
import json
import os
from .memory_node import Memory
from .memory_score import MemoryScore


class MemoryEngine:
    def __init__(self, storage_path: str = "database/memories.json"):
        self.storage_path = storage_path
        self.memories: Dict[str, Memory] = {}
        self.score_threshold = 0.3
        self.max_memories = 10000
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for m_data in data.get("memories", []):
                        memory = Memory.from_dict(m_data)
                        self.memories[memory.id] = memory
            except Exception:
                pass

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "memories": [m.to_dict() for m in self.memories.values()],
            "saved_at": datetime.now().isoformat()
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add(self, content: str, importance: float = 0.5,
            tags: Optional[List[str]] = None,
            embedding: Optional[List[float]] = None) -> Memory:
        memory = Memory(
            content=content,
            importance=importance,
            tags=tags or [],
            embedding=embedding
        )
        self.memories[memory.id] = memory
        self._cleanup()
        self._save()
        return memory

    def access(self, memory_id: str) -> Optional[Memory]:
        memory = self.memories.get(memory_id)
        if memory:
            memory.access_count += 1
            memory.last_accessed = datetime.now()
            self._save()
        return memory

    def get(self, memory_id: str) -> Optional[Memory]:
        return self.memories.get(memory_id)

    def search(self, query: str, limit: int = 10) -> List[Memory]:
        query_lower = query.lower()
        results = []
        for memory in self.memories.values():
            if query_lower in memory.content.lower():
                memory.access_count += 1
                memory.last_accessed = datetime.now()
                results.append(memory)
        results.sort(key=lambda m: MemoryScore.calculate_score(m), reverse=True)
        return results[:limit]

    def search_by_tags(self, tags: List[str], limit: int = 10) -> List[Memory]:
        results = []
        for memory in self.memories.values():
            if any(tag in memory.tags for tag in tags):
                memory.access_count += 1
                memory.last_accessed = datetime.now()
                results.append(memory)
        results.sort(key=lambda m: MemoryScore.calculate_score(m), reverse=True)
        return results[:limit]

    def get_recent(self, limit: int = 20) -> List[Memory]:
        sorted_memories = sorted(
            self.memories.values(),
            key=lambda m: m.last_accessed,
            reverse=True
        )
        return sorted_memories[:limit]

    def get_important(self, limit: int = 20) -> List[Memory]:
        scored = MemoryScore.get_all_scores(self.memories.values())
        scored.sort(key=lambda x: x[1], reverse=True)
        return [m for m, _ in scored[:limit]]

    def update_importance(self, memory_id: str, importance: float):
        memory = self.memories.get(memory_id)
        if memory:
            memory.importance = max(0.0, min(1.0, importance))
            self._save()

    def delete(self, memory_id: str) -> bool:
        if memory_id in self.memories:
            del self.memories[memory_id]
            self._save()
            return True
        return False

    def _cleanup(self):
        to_delete = []
        for memory in self.memories.values():
            if MemoryScore.should_delete(memory, self.score_threshold):
                to_delete.append(memory.id)

        for memory_id in to_delete:
            del self.memories[memory_id]

        if len(self.memories) > self.max_memories:
            scored = MemoryScore.get_all_scores(self.memories.values())
            scored.sort(key=lambda x: x[1])
            excess = len(scored) - self.max_memories
            for memory_id, _ in scored[:excess]:
                del self.memories[memory_id]

    def get_stats(self) -> Dict[str, Any]:
        memories_list = list(self.memories.values())
        if not memories_list:
            return {
                "total": 0,
                "avg_importance": 0,
                "avg_access_count": 0,
                "top_tags": []
            }

        scores = MemoryScore.get_all_scores(memories_list)
        avg_score = sum(s for _, s in scores) / len(scores)

        tag_counts: Dict[str, int] = {}
        for m in memories_list:
            for tag in m.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "total": len(memories_list),
            "avg_importance": round(sum(m.importance for m in memories_list) / len(memories_list), 3),
            "avg_access_count": round(sum(m.access_count for m in memories_list) / len(memories_list), 2),
            "avg_score": round(avg_score, 3),
            "top_tags": top_tags
        }

    def form_experience(self, task: str, result: str, time_taken: str, lesson: str) -> Memory:
        content = f"任务: {task}\n结果: {result}\n用时: {time_taken}\n经验: {lesson}"
        return self.add(
            content=content,
            importance=0.8,
            tags=["experience", "learned"],
            embedding=None
        )
