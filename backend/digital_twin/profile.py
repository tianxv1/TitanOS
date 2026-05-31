from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
import uuid
import json
import os


@dataclass
class WritingStyle:
    formal_level: float = 0.5
    sentence_length_preference: str = "medium"
    uses_emoji: bool = False
    greeting_style: str = "neutral"
    closing_style: str = "neutral"
    common_phrases: List[str] = field(default_factory=list)
    tone: str = "professional"
    samples: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "formal_level": self.formal_level,
            "sentence_length_preference": self.sentence_length_preference,
            "uses_emoji": self.uses_emoji,
            "greeting_style": self.greeting_style,
            "closing_style": self.closing_style,
            "common_phrases": self.common_phrases,
            "tone": self.tone,
            "samples": self.samples
        }


@dataclass
class CodeStyle:
    language_preferences: List[str] = field(default_factory=list)
    naming_convention: str = "snake_case"
    comment_style: str = "minimal"
    error_handling: str = "try_except"
    indentation: str = "spaces"
    framework_preferences: List[str] = field(default_factory=list)
    code_samples: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "language_preferences": self.language_preferences,
            "naming_convention": self.naming_convention,
            "comment_style": self.comment_style,
            "error_handling": self.error_handling,
            "indentation": self.indentation,
            "framework_preferences": self.framework_preferences,
            "code_samples": self.code_samples
        }


@dataclass
class DecisionPattern:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    situation: str = ""
    decision: str = ""
    reasoning: str = ""
    outcome: str = ""
    confidence: float = 0.5
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "situation": self.situation,
            "decision": self.decision,
            "reasoning": self.reasoning,
            "outcome": self.outcome,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class LearningHabit:
    subject: str = ""
    frequency: str = "daily"
    preferred_time: str = "morning"
    duration_minutes: int = 60
    learning_methods: List[str] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "subject": self.subject,
            "frequency": self.frequency,
            "preferred_time": self.preferred_time,
            "duration_minutes": self.duration_minutes,
            "learning_methods": self.learning_methods,
            "interests": self.interests,
            "goals": self.goals
        }


@dataclass
class PersonalityProfile:
    openness: float = 0.7
    conscientiousness: float = 0.7
    extraversion: float = 0.5
    agreeableness: float = 0.6
    neuroticism: float = 0.3
    creativity_score: float = 0.7
    analytical_score: float = 0.8
    sociability_score: float = 0.5

    def to_dict(self) -> dict:
        return {
            "openness": self.openness,
            "conscientiousness": self.conscientiousness,
            "extraversion": self.extraversion,
            "agreeableness": self.agreeableness,
            "neuroticism": self.neuroticism,
            "creativity_score": self.creativity_score,
            "analytical_score": self.analytical_score,
            "sociability_score": self.sociability_score
        }


@dataclass
class DigitalTwinProfile:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "My Digital Twin"
    writing_style: WritingStyle = field(default_factory=WritingStyle)
    code_style: CodeStyle = field(default_factory=CodeStyle)
    personality: PersonalityProfile = field(default_factory=PersonalityProfile)
    decision_patterns: List[DecisionPattern] = field(default_factory=list)
    learning_habits: List[LearningHabit] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "writing_style": self.writing_style.to_dict(),
            "code_style": self.code_style.to_dict(),
            "personality": self.personality.to_dict(),
            "decision_patterns": [p.to_dict() for p in self.decision_patterns],
            "learning_habits": [h.to_dict() for h in self.learning_habits],
            "interests": self.interests,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
