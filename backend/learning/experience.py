from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
import uuid
import json
import os


@dataclass
class Experience:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task: str = ""
    result: str = ""
    time_taken: str = ""
    lesson: str = ""
    category: str = "general"
    tags: List[str] = field(default_factory=list)
    success: bool = True
    difficulty: int = 3
    created_at: datetime = field(default_factory=datetime.now)
    feedback: Optional[str] = None
    next_actions: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "task": self.task,
            "result": self.result,
            "time_taken": self.time_taken,
            "lesson": self.lesson,
            "category": self.category,
            "tags": self.tags,
            "success": self.success,
            "difficulty": self.difficulty,
            "created_at": self.created_at.isoformat(),
            "feedback": self.feedback,
            "next_actions": self.next_actions
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Experience":
        data = data.copy()
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)


@dataclass
class LearnedPattern:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    pattern: str = ""
    context: str = ""
    action: str = ""
    outcome: str = ""
    confidence: float = 0.5
    usage_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    last_used: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "pattern": self.pattern,
            "context": self.context,
            "action": self.action,
            "outcome": self.outcome,
            "confidence": self.confidence,
            "usage_count": self.usage_count,
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "LearnedPattern":
        data = data.copy()
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("last_used"), str):
            data["last_used"] = datetime.fromisoformat(data["last_used"])
        return cls(**data)


@dataclass
class GrowthMetrics:
    total_experiences: int = 0
    successful_experiences: int = 0
    total_time_spent: str = "0h"
    most_common_category: str = "general"
    learning_velocity: float = 0.0
    improvement_rate: float = 0.0
    strength_areas: List[str] = field(default_factory=list)
    weakness_areas: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "total_experiences": self.total_experiences,
            "successful_experiences": self.successful_experiences,
            "total_time_spent": self.total_time_spent,
            "most_common_category": self.most_common_category,
            "learning_velocity": self.learning_velocity,
            "improvement_rate": self.improvement_rate,
            "strength_areas": self.strength_areas,
            "weakness_areas": self.weakness_areas
        }
