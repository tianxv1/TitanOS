from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid
import json
import os


@dataclass
class EpisodicMemory:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    time: datetime = field(default_factory=datetime.now)
    location: str = ""
    people: List[str] = field(default_factory=list)
    event: str = ""
    emotion: str = ""
    content: str = ""
    importance: float = 0.5
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": "episodic",
            "time": self.time.isoformat(),
            "location": self.location,
            "people": self.people,
            "event": self.event,
            "emotion": self.emotion,
            "content": self.content,
            "importance": self.importance,
            "tags": self.tags
        }

    @classmethod
    def from_dict(cls, data: dict) -> "EpisodicMemory":
        data = data.copy()
        if isinstance(data.get("time"), str):
            data["time"] = datetime.fromisoformat(data["time"])
        return cls(**data)


@dataclass
class SemanticMemory:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    concept: str = ""
    definition: str = ""
    relations: List[Dict[str, str]] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    source: str = ""
    confidence: float = 0.8
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": "semantic",
            "concept": self.concept,
            "definition": self.definition,
            "relations": self.relations,
            "examples": self.examples,
            "source": self.source,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SemanticMemory":
        data = data.copy()
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)


@dataclass
class ProceduralMemory:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    skill: str = ""
    steps: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    difficulty: str = "medium"
    mastery_level: float = 0.0
    last_practiced: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": "procedural",
            "skill": self.skill,
            "steps": self.steps,
            "prerequisites": self.prerequisites,
            "difficulty": self.difficulty,
            "mastery_level": self.mastery_level,
            "last_practiced": self.last_practiced.isoformat() if self.last_practiced else None,
            "created_at": self.created_at.isoformat(),
            "tags": self.tags
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProceduralMemory":
        data = data.copy()
        if isinstance(data.get("last_practiced"), str):
            data["last_practiced"] = datetime.fromisoformat(data["last_practiced"])
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)


class CognitiveMemorySystem:
    def __init__(self):
        self.episodic_memories: Dict[str, EpisodicMemory] = {}
        self.semantic_memories: Dict[str, SemanticMemory] = {}
        self.procedural_memories: Dict[str, ProceduralMemory] = {}
        self._load_memories()

    def _load_memories(self):
        storage_paths = {
            "episodic": "database/episodic_memories.json",
            "semantic": "database/semantic_memories.json",
            "procedural": "database/procedural_memories.json"
        }

        for mem_type, path in storage_paths.items():
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        memories = data.get("memories", [])
                        
                        if mem_type == "episodic":
                            for m in memories:
                                mem = EpisodicMemory.from_dict(m)
                                self.episodic_memories[mem.id] = mem
                        elif mem_type == "semantic":
                            for m in memories:
                                mem = SemanticMemory.from_dict(m)
                                self.semantic_memories[mem.id] = mem
                        elif mem_type == "procedural":
                            for m in memories:
                                mem = ProceduralMemory.from_dict(m)
                                self.procedural_memories[mem.id] = mem
                except Exception:
                    pass

    def _save_memories(self):
        os.makedirs("database", exist_ok=True)
        
        storage_paths = {
            "episodic": ("episodic_memories.json", self.episodic_memories),
            "semantic": ("semantic_memories.json", self.semantic_memories),
            "procedural": ("procedural_memories.json", self.procedural_memories)
        }

        for mem_type, (filename, memories) in storage_paths.items():
            data = {
                "memories": [m.to_dict() for m in memories.values()],
                "saved_at": datetime.now().isoformat()
            }
            with open(f"database/{filename}", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    def add_episodic(self, time: datetime, location: str, people: List[str], 
                     event: str, emotion: str, content: str, 
                     importance: float = 0.5, tags: List[str] = None) -> EpisodicMemory:
        memory = EpisodicMemory(
            time=time,
            location=location,
            people=people,
            event=event,
            emotion=emotion,
            content=content,
            importance=importance,
            tags=tags or []
        )
        self.episodic_memories[memory.id] = memory
        self._save_memories()
        return memory

    def get_episodic(self, memory_id: str) -> Optional[EpisodicMemory]:
        return self.episodic_memories.get(memory_id)

    def list_episodic(self, year: Optional[int] = None, emotion: Optional[str] = None) -> List[Dict[str, Any]]:
        memories = list(self.episodic_memories.values())
        
        if year:
            memories = [m for m in memories if m.time.year == year]
        if emotion:
            memories = [m for m in memories if emotion.lower() in m.emotion.lower()]
        
        return sorted([m.to_dict() for m in memories], key=lambda x: x["time"], reverse=True)

    def add_semantic(self, concept: str, definition: str, relations: List[Dict[str, str]] = None,
                     examples: List[str] = None, source: str = "", confidence: float = 0.8) -> SemanticMemory:
        memory = SemanticMemory(
            concept=concept,
            definition=definition,
            relations=relations or [],
            examples=examples or [],
            source=source,
            confidence=confidence
        )
        self.semantic_memories[memory.id] = memory
        self._save_memories()
        return memory

    def get_semantic(self, memory_id: str) -> Optional[SemanticMemory]:
        return self.semantic_memories.get(memory_id)

    def list_semantic(self, concept: Optional[str] = None) -> List[Dict[str, Any]]:
        memories = list(self.semantic_memories.values())
        
        if concept:
            memories = [m for m in memories if concept.lower() in m.concept.lower()]
        
        return sorted([m.to_dict() for m in memories], key=lambda x: x["confidence"], reverse=True)

    def add_procedural(self, skill: str, steps: List[str], prerequisites: List[str] = None,
                       difficulty: str = "medium", tags: List[str] = None) -> ProceduralMemory:
        memory = ProceduralMemory(
            skill=skill,
            steps=steps,
            prerequisites=prerequisites or [],
            difficulty=difficulty,
            tags=tags or []
        )
        self.procedural_memories[memory.id] = memory
        self._save_memories()
        return memory

    def get_procedural(self, memory_id: str) -> Optional[ProceduralMemory]:
        return self.procedural_memories.get(memory_id)

    def list_procedural(self, skill: Optional[str] = None, difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
        memories = list(self.procedural_memories.values())
        
        if skill:
            memories = [m for m in memories if skill.lower() in m.skill.lower()]
        if difficulty:
            memories = [m for m in memories if m.difficulty.lower() == difficulty.lower()]
        
        return sorted([m.to_dict() for m in memories], key=lambda x: x["mastery_level"], reverse=True)

    def practice_skill(self, memory_id: str, practice_quality: float = 0.8):
        memory = self.procedural_memories.get(memory_id)
        if not memory:
            return False

        memory.last_practiced = datetime.now()
        memory.mastery_level = min(1.0, memory.mastery_level + practice_quality * 0.1)
        self._save_memories()
        return True

    def search(self, query: str) -> Dict[str, List[Dict[str, Any]]]:
        results = {
            "episodic": [],
            "semantic": [],
            "procedural": []
        }

        query_lower = query.lower()
        
        for mem in self.episodic_memories.values():
            if query_lower in mem.event.lower() or query_lower in mem.content.lower():
                results["episodic"].append(mem.to_dict())

        for mem in self.semantic_memories.values():
            if query_lower in mem.concept.lower() or query_lower in mem.definition.lower():
                results["semantic"].append(mem.to_dict())

        for mem in self.procedural_memories.values():
            if query_lower in mem.skill.lower():
                results["procedural"].append(mem.to_dict())

        return results

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_episodic": len(self.episodic_memories),
            "total_semantic": len(self.semantic_memories),
            "total_procedural": len(self.procedural_memories),
            "total_memories": (len(self.episodic_memories) + 
                              len(self.semantic_memories) + 
                              len(self.procedural_memories)),
            "avg_mastery_level": self._calculate_avg_mastery()
        }

    def _calculate_avg_mastery(self) -> float:
        if not self.procedural_memories:
            return 0.0
        total = sum(m.mastery_level for m in self.procedural_memories.values())
        return round(total / len(self.procedural_memories), 2)

    def get_timeline(self) -> List[Dict[str, Any]]:
        all_events = []
        
        for mem in self.episodic_memories.values():
            all_events.append({
                "type": "episodic",
                "time": mem.time.isoformat(),
                "title": mem.event,
                "content": mem.content[:50] + "..." if len(mem.content) > 50 else mem.content
            })

        for mem in self.semantic_memories.values():
            all_events.append({
                "type": "semantic",
                "time": mem.created_at.isoformat(),
                "title": f"Learned: {mem.concept}",
                "content": mem.definition[:50] + "..." if len(mem.definition) > 50 else mem.definition
            })

        for mem in self.procedural_memories.values():
            all_events.append({
                "type": "procedural",
                "time": mem.created_at.isoformat(),
                "title": f"Skill: {mem.skill}",
                "content": f"Mastery: {int(mem.mastery_level * 100)}%"
            })

        return sorted(all_events, key=lambda x: x["time"], reverse=True)
