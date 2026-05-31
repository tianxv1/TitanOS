from typing import List, Optional, Dict, Any
from datetime import datetime
from .experience import Experience, LearnedPattern, GrowthMetrics
import json
import os


class LearningEngine:
    def __init__(self, storage_path: str = "database/learning.json"):
        self.storage_path = storage_path
        self.experiences: Dict[str, Experience] = {}
        self.patterns: Dict[str, LearnedPattern] = {}
        self.metrics = GrowthMetrics()
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    for exp_data in data.get("experiences", []):
                        exp = Experience.from_dict(exp_data)
                        self.experiences[exp.id] = exp

                    for pat_data in data.get("patterns", []):
                        pat = LearnedPattern.from_dict(pat_data)
                        self.patterns[pat.id] = pat

                    metrics_data = data.get("metrics", {})
                    self.metrics = GrowthMetrics(**metrics_data)

            except Exception:
                pass

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "experiences": [exp.to_dict() for exp in self.experiences.values()],
            "patterns": [pat.to_dict() for pat in self.patterns.values()],
            "metrics": self.metrics.to_dict(),
            "saved_at": datetime.now().isoformat()
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_experience(self, task: str, result: str, time_taken: str,
                      lesson: str, category: str = "general",
                      tags: Optional[List[str]] = None,
                      success: bool = True,
                      difficulty: int = 3,
                      next_actions: Optional[List[str]] = None) -> Experience:
        exp = Experience(
            task=task,
            result=result,
            time_taken=time_taken,
            lesson=lesson,
            category=category,
            tags=tags or [],
            success=success,
            difficulty=difficulty,
            next_actions=next_actions or []
        )
        self.experiences[exp.id] = exp
        self._update_metrics()
        self._extract_pattern(exp)
        self._save()
        return exp

    def get_experience(self, exp_id: str) -> Optional[Experience]:
        return self.experiences.get(exp_id)

    def get_recent_experiences(self, limit: int = 20) -> List[Experience]:
        sorted_exps = sorted(
            self.experiences.values(),
            key=lambda e: e.created_at,
            reverse=True
        )
        return sorted_exps[:limit]

    def get_experiences_by_category(self, category: str) -> List[Experience]:
        return [exp for exp in self.experiences.values() if exp.category == category]

    def get_experiences_by_tags(self, tags: List[str]) -> List[Experience]:
        results = []
        for exp in self.experiences.values():
            if any(tag in exp.tags for tag in tags):
                results.append(exp)
        return sorted(results, key=lambda e: e.created_at, reverse=True)

    def _update_metrics(self):
        exps = list(self.experiences.values())
        if not exps:
            return

        self.metrics.total_experiences = len(exps)
        self.metrics.successful_experiences = sum(1 for e in exps if e.success)

        total_seconds = 0
        for exp in exps:
            time_str = exp.time_taken.lower()
            if "min" in time_str:
                total_seconds += int(time_str.replace("min", "").strip()) * 60
            elif "h" in time_str:
                total_seconds += int(time_str.replace("h", "").strip()) * 3600
            elif "sec" in time_str:
                total_seconds += int(time_str.replace("sec", "").strip())

        hours = total_seconds / 3600
        self.metrics.total_time_spent = f"{hours:.1f}h"

        categories: Dict[str, int] = {}
        for exp in exps:
            categories[exp.category] = categories.get(exp.category, 0) + 1
        if categories:
            self.metrics.most_common_category = max(categories.items(), key=lambda x: x[1])[0]

        tag_counts: Dict[str, int] = {}
        for exp in exps:
            for tag in exp.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        self.metrics.strength_areas = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        self.metrics.strength_areas = [t[0] for t in self.metrics.strength_areas]

    def _extract_pattern(self, exp: Experience):
        if not exp.success or not exp.lesson:
            return

        pattern_str = f"{exp.task} -> {exp.lesson}"
        for existing_pat in self.patterns.values():
            if self._calculate_similarity(pattern_str, f"{existing_pat.pattern}") > 0.7:
                existing_pat.usage_count += 1
                existing_pat.confidence = min(existing_pat.confidence + 0.1, 1.0)
                existing_pat.last_used = datetime.now()
                self._save()
                return

        pattern = LearnedPattern(
            pattern=pattern_str,
            context=exp.task,
            action=exp.lesson,
            outcome=exp.result,
            confidence=0.5
        )
        self.patterns[pattern.id] = pattern

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        return intersection / union if union > 0 else 0.0

    def suggest_next_actions(self, task: str) -> List[str]:
        suggestions = []

        task_lower = task.lower()
        for pattern in self.patterns.values():
            if pattern.confidence > 0.6:
                if any(word in pattern.pattern.lower() for word in task_lower.split()):
                    if pattern.next_actions:
                        suggestions.extend(pattern.next_actions[:2])

        matching_exps = [
            exp for exp in self.experiences.values()
            if task_lower in exp.task.lower() and exp.next_actions
        ]
        for exp in matching_exps[:3]:
            suggestions.extend(exp.next_actions[:2])

        return list(dict.fromkeys(suggestions))[:5]

    def get_learned_lessons(self, limit: int = 10) -> List[str]:
        lessons = []
        for exp in self.experiences.values():
            if exp.success and exp.lesson:
                lessons.append(exp.lesson)
        return lessons[:limit]

    def update_experience_feedback(self, exp_id: str, feedback: str, rating: int = 5):
        exp = self.experiences.get(exp_id)
        if exp:
            exp.feedback = feedback
            if rating < 3 and exp.success:
                exp.success = False
                self._update_metrics()
            self._save()

    def get_pattern_suggestions(self, context: str) -> List[Dict[str, Any]]:
        suggestions = []
        context_words = set(context.lower().split())

        for pattern in self.patterns.values():
            pattern_words = set(pattern.pattern.lower().split())
            similarity = self._calculate_similarity(context, pattern.pattern)

            if similarity > 0.3 or any(word in pattern.pattern.lower() for word in context_words):
                suggestions.append({
                    "pattern": pattern.pattern,
                    "action": pattern.action,
                    "confidence": pattern.confidence,
                    "outcome": pattern.outcome
                })

        suggestions.sort(key=lambda x: x["confidence"], reverse=True)
        return suggestions[:5]

    def get_growth_report(self) -> Dict[str, Any]:
        self._update_metrics()
        recent_exps = self.get_recent_experiences(10)
        recent_success_rate = 0.0
        if recent_exps:
            recent_success_rate = sum(1 for e in recent_exps if e.success) / len(recent_exps)

        return {
            "metrics": self.metrics.to_dict(),
            "recent_success_rate": round(recent_success_rate, 2),
            "top_patterns": [
                p.to_dict() for p in sorted(self.patterns.values(),
                                            key=lambda x: x.confidence,
                                            reverse=True)[:5]
            ],
            "suggestions": self.suggest_next_actions("general")
        }

    def reset(self):
        self.experiences.clear()
        self.patterns.clear()
        self.metrics = GrowthMetrics()
        self._save()
