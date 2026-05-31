from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
import uuid
import json
import os


@dataclass
class Reflection:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = ""
    task_name: str = ""
    what_happened: str = ""
    what_went_well: List[str] = field(default_factory=list)
    what_could_improve: List[str] = field(default_factory=list)
    mistakes: List[str] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    confidence_level: int = 3
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "task_id": self.task_id,
            "task_name": self.task_name,
            "what_happened": self.what_happened,
            "what_went_well": self.what_went_well,
            "what_could_improve": self.what_could_improve,
            "mistakes": self.mistakes,
            "lessons_learned": self.lessons_learned,
            "improvements": self.improvements,
            "confidence_level": self.confidence_level,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Reflection":
        data = data.copy()
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)


@dataclass
class Improvement:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    reflection_id: str = ""
    original_mistake: str = ""
    improvement_action: str = ""
    expected_outcome: str = ""
    actual_outcome: Optional[str] = None
    status: str = "pending"
    applied_count: int = 0
    success_rate: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    applied_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "reflection_id": self.reflection_id,
            "original_mistake": self.original_mistake,
            "improvement_action": self.improvement_action,
            "expected_outcome": self.expected_outcome,
            "actual_outcome": self.actual_outcome,
            "status": self.status,
            "applied_count": self.applied_count,
            "success_rate": self.success_rate,
            "created_at": self.created_at.isoformat(),
            "applied_at": self.applied_at.isoformat() if self.applied_at else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Improvement":
        data = data.copy()
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("applied_at"), str):
            data["applied_at"] = datetime.fromisoformat(data["applied_at"])
        return cls(**data)


@dataclass
class GrowthMetrics:
    total_reflections: int = 0
    total_improvements: int = 0
    successful_improvements: int = 0
    common_mistakes: List[str] = field(default_factory=list)
    top_lessons: List[str] = field(default_factory=list)
    improvement_rate: float = 0.0
    confidence_trend: List[int] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "total_reflections": self.total_reflections,
            "total_improvements": self.total_improvements,
            "successful_improvements": self.successful_improvements,
            "common_mistakes": self.common_mistakes,
            "top_lessons": self.top_lessons,
            "improvement_rate": self.improvement_rate,
            "confidence_trend": self.confidence_trend
        }
