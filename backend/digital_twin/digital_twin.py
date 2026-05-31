from typing import List, Optional, Dict, Any
from datetime import datetime
from .profile import (
    DigitalTwinProfile, WritingStyle, CodeStyle, DecisionPattern,
    LearningHabit, PersonalityProfile
)
import json
import os


class DigitalTwin:
    def __init__(self, storage_path: str = "database/digital_twin.json"):
        self.storage_path = storage_path
        self.profile: Optional[DigitalTwinProfile] = None
        self.behavior_history: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    if "profile" in data:
                        p = data["profile"]
                        self.profile = DigitalTwinProfile(
                            id=p.get("id", str(uuid.uuid4())),
                            name=p.get("name", "My Digital Twin"),
                            writing_style=WritingStyle(**p.get("writing_style", {})),
                            code_style=CodeStyle(**p.get("code_style", {})),
                            personality=PersonalityProfile(**p.get("personality", {})),
                            decision_patterns=[
                                DecisionPattern(**dp) for dp in p.get("decision_patterns", [])
                            ],
                            learning_habits=[
                                LearningHabit(**lh) for lh in p.get("learning_habits", [])
                            ],
                            interests=p.get("interests", []),
                            strengths=p.get("strengths", []),
                            weaknesses=p.get("weaknesses", []),
                        )
                        if isinstance(p.get("created_at"), str):
                            self.profile.created_at = datetime.fromisoformat(p["created_at"])
                        if isinstance(p.get("updated_at"), str):
                            self.profile.updated_at = datetime.fromisoformat(p["updated_at"])

                    self.behavior_history = data.get("behavior_history", [])

            except Exception:
                pass

        if not self.profile:
            self.profile = DigitalTwinProfile()

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "profile": self.profile.to_dict() if self.profile else None,
            "behavior_history": self.behavior_history[-100:],
            "saved_at": datetime.now().isoformat()
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _get_timestamp(self):
        return datetime.now().isoformat()

    def initialize(self, name: str = "My Digital Twin"):
        self.profile = DigitalTwinProfile(name=name)
        self._save()

    def update_writing_style(self, **kwargs):
        if not self.profile:
            self.initialize()

        ws = self.profile.writing_style
        if "formal_level" in kwargs:
            ws.formal_level = max(0.0, min(1.0, kwargs["formal_level"]))
        if "sentence_length_preference" in kwargs:
            ws.sentence_length_preference = kwargs["sentence_length_preference"]
        if "uses_emoji" in kwargs:
            ws.uses_emoji = kwargs["uses_emoji"]
        if "greeting_style" in kwargs:
            ws.greeting_style = kwargs["greeting_style"]
        if "closing_style" in kwargs:
            ws.closing_style = kwargs["closing_style"]
        if "tone" in kwargs:
            ws.tone = kwargs["tone"]
        if "common_phrases" in kwargs:
            ws.common_phrases = kwargs["common_phrases"]

        self.profile.updated_at = self._get_timestamp()
        self._save()

    def add_writing_sample(self, sample: str):
        if not self.profile:
            self.initialize()
        if sample not in self.profile.writing_style.samples:
            self.profile.writing_style.samples.append(sample)
            self._analyze_writing_style(sample)
            self.profile.updated_at = self._get_timestamp()
            self._save()

    def _analyze_writing_style(self, sample: str):
        ws = self.profile.writing_style

        if len(sample) > 100:
            ws.sentence_length_preference = "long"
        elif len(sample) > 50:
            ws.sentence_length_preference = "medium"
        else:
            ws.sentence_length_preference = "short"

        if any(char in sample for char in ["😊", "😂", "👍", "❤️"]):
            ws.uses_emoji = True

        formal_markers = ["因此", "然而", "综上所述", "此外"]
        casual_markers = ["哈", "啦", "嘛", "呗"]
        formal_count = sum(1 for m in formal_markers if m in sample)
        casual_count = sum(1 for m in casual_markers if m in sample)

        if formal_count > casual_count:
            ws.formal_level = min(1.0, ws.formal_level + 0.1)
            ws.tone = "formal"
        elif casual_count > formal_count:
            ws.formal_level = max(0.0, ws.formal_level - 0.1)
            ws.tone = "casual"

    def update_code_style(self, **kwargs):
        if not self.profile:
            self.initialize()

        cs = self.profile.code_style
        if "language_preferences" in kwargs:
            cs.language_preferences = kwargs["language_preferences"]
        if "naming_convention" in kwargs:
            cs.naming_convention = kwargs["naming_convention"]
        if "comment_style" in kwargs:
            cs.comment_style = kwargs["comment_style"]
        if "error_handling" in kwargs:
            cs.error_handling = kwargs["error_handling"]
        if "framework_preferences" in kwargs:
            cs.framework_preferences = kwargs["framework_preferences"]

        self.profile.updated_at = self._get_timestamp()
        self._save()

    def add_code_sample(self, sample: str, language: str = "python"):
        if not self.profile:
            self.initialize()

        if sample not in self.profile.code_style.code_samples:
            self.profile.code_style.code_samples.append(sample)

        if language not in self.profile.code_style.language_preferences:
            self.profile.code_style.language_preferences.append(language)

        self._analyze_code_style(sample)
        self.profile.updated_at = self._get_timestamp()
        self._save()

    def _analyze_code_style(self, sample: str):
        cs = self.profile.code_style

        if "# " in sample or "// " in sample:
            cs.comment_style = "detailed"
        elif "#" in sample or "//" in sample:
            cs.comment_style = "minimal"

        if "try:" in sample or "try {" in sample:
            cs.error_handling = "try_except"
        elif "if err" in sample.lower():
            cs.error_handling = "error_checking"

        if sample.count("    ") > sample.count("\t"):
            cs.indentation = "spaces"
        else:
            cs.indentation = "tabs"

    def record_decision(self, situation: str, decision: str,
                       reasoning: str, outcome: str):
        if not self.profile:
            self.initialize()

        pattern = DecisionPattern(
            situation=situation,
            decision=decision,
            reasoning=reasoning,
            outcome=outcome,
            confidence=0.5
        )
        self.profile.decision_patterns.append(pattern)
        self.profile.updated_at = self._get_timestamp()
        self._save()

        self._add_behavior("decision", {
            "situation": situation,
            "decision": decision,
            "outcome": outcome
        })

    def update_learning_habit(self, subject: str, frequency: str = "daily",
                            preferred_time: str = "morning",
                            duration_minutes: int = 60,
                            learning_methods: Optional[List[str]] = None):
        if not self.profile:
            self.initialize()

        existing = None
        for habit in self.profile.learning_habits:
            if habit.subject == subject:
                existing = habit
                break

        if existing:
            existing.frequency = frequency
            existing.preferred_time = preferred_time
            existing.duration_minutes = duration_minutes
            if learning_methods:
                existing.learning_methods = learning_methods
        else:
            habit = LearningHabit(
                subject=subject,
                frequency=frequency,
                preferred_time=preferred_time,
                duration_minutes=duration_minutes,
                learning_methods=learning_methods or []
            )
            self.profile.learning_habits.append(habit)

        self.profile.updated_at = self._get_timestamp()
        self._save()

    def update_interests(self, interests: List[str]):
        if not self.profile:
            self.initialize()
        self.profile.interests = list(set(self.profile.interests + interests))
        self.profile.updated_at = self._get_timestamp()
        self._save()

    def update_strengths_weaknesses(self, strengths: Optional[List[str]] = None,
                                   weaknesses: Optional[List[str]] = None):
        if not self.profile:
            self.initialize()
        if strengths:
            self.profile.strengths = list(set(self.profile.strengths + strengths))
        if weaknesses:
            self.profile.weaknesses = list(set(self.profile.weaknesses + weaknesses))
        self.profile.updated_at = self._get_timestamp()
        self._save()

    def update_personality(self, **kwargs):
        if not self.profile:
            self.initialize()

        p = self.profile.personality
        valid_traits = ["openness", "conscientiousness", "extraversion",
                       "agreeableness", "neuroticism", "creativity_score",
                       "analytical_score", "sociability_score"]

        for trait in valid_traits:
            if trait in kwargs:
                setattr(p, trait, max(0.0, min(1.0, kwargs[trait])))

        self.profile.updated_at = self._get_timestamp()
        self._save()

    def _add_behavior(self, behavior_type: str, data: Dict[str, Any]):
        self.behavior_history.append({
            "type": behavior_type,
            "data": data,
            "timestamp": self._get_timestamp()
        })
        if len(self.behavior_history) > 100:
            self.behavior_history = self.behavior_history[-100:]
        self._save()

    def get_profile(self) -> Optional[Dict[str, Any]]:
        return self.profile.to_dict() if self.profile else None

    def generate_response_style(self, context: str) -> Dict[str, Any]:
        if not self.profile:
            return {"tone": "neutral", "style": "balanced"}

        ws = self.profile.writing_style
        p = self.profile.personality

        response_style = {
            "tone": ws.tone,
            "formality": "formal" if ws.formal_level > 0.6 else "casual",
            "sentence_length": ws.sentence_length_preference,
            "use_emoji": ws.uses_emoji,
            "suggested_phrases": ws.common_phrases[:3] if ws.common_phrases else [],
            "creativity": p.creativity_score,
            "analytical": p.analytical_score
        }

        if "question" in context.lower() or "?" in context:
            response_style["greeting"] = ws.greeting_style
        else:
            response_style["closing"] = ws.closing_style

        return response_style

    def suggest_decision(self, situation: str) -> Optional[Dict[str, Any]]:
        if not self.profile:
            return None

        situation_lower = situation.lower()
        best_match = None
        best_confidence = 0.0

        for pattern in self.profile.decision_patterns:
            pattern_words = set(pattern.situation.lower().split())
            situation_words = set(situation_lower.split())
            overlap = len(pattern_words & situation_words)

            if overlap > 0 and pattern.confidence > best_confidence:
                best_match = pattern
                best_confidence = pattern.confidence

        if best_match:
            return {
                "suggested_decision": best_match.decision,
                "reasoning": best_match.reasoning,
                "confidence": best_match.confidence,
                "past_outcome": best_match.outcome
            }
        return None

    def get_learning_recommendations(self) -> List[Dict[str, Any]]:
        if not self.profile or not self.profile.learning_habits:
            return []

        recommendations = []
        for habit in self.profile.learning_habits:
            recommendations.append({
                "subject": habit.subject,
                "suggested_time": habit.preferred_time,
                "suggested_duration": habit.duration_minutes,
                "methods": habit.learning_methods,
                "frequency": habit.frequency
            })
        return recommendations

    def get_interests_overview(self) -> Dict[str, Any]:
        if not self.profile:
            return {"interests": [], "strengths": [], "weaknesses": []}

        return {
            "interests": self.profile.interests,
            "strengths": self.profile.strengths,
            "weaknesses": self.profile.weaknesses,
            "primary_learning_style": self._infer_learning_style()
        }

    def _infer_learning_style(self) -> str:
        if not self.profile or not self.profile.learning_habits:
            return "mixed"

        methods: Dict[str, int] = {}
        for habit in self.profile.learning_habits:
            for method in habit.learning_methods:
                methods[method] = methods.get(method, 0) + 1

        if not methods:
            return "mixed"
        return max(methods.items(), key=lambda x: x[1])[0]

    def sync_with_learning_engine(self, learning_engine) -> bool:
        if not self.profile:
            return False

        try:
            growth_report = learning_engine.get_growth_report()
            if growth_report.get("metrics"):
                metrics = growth_report["metrics"]

                if metrics.get("strength_areas"):
                    self.update_interests(metrics["strength_areas"])
                    self.update_strengths_weaknesses(strengths=metrics["strength_areas"])

            return True
        except Exception:
            return False
