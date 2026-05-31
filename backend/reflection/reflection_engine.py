from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import Reflection, Improvement, GrowthMetrics
import json
import os


class ReflectionEngine:
    def __init__(self, storage_path: str = "database/reflection.json"):
        self.storage_path = storage_path
        self.reflections: Dict[str, Reflection] = {}
        self.improvements: Dict[str, Improvement] = {}
        self.metrics = GrowthMetrics()
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    for r_data in data.get("reflections", []):
                        reflection = Reflection.from_dict(r_data)
                        self.reflections[reflection.id] = reflection

                    for i_data in data.get("improvements", []):
                        improvement = Improvement.from_dict(i_data)
                        self.improvements[improvement.id] = improvement

                    metrics_data = data.get("metrics", {})
                    self.metrics = GrowthMetrics(**metrics_data)

            except Exception:
                pass

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "reflections": [r.to_dict() for r in self.reflections.values()],
            "improvements": [i.to_dict() for i in self.improvements.values()],
            "metrics": self.metrics.to_dict(),
            "saved_at": datetime.now().isoformat()
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def reflect(self, task_id: str, task_name: str,
               what_happened: str,
               what_went_well: Optional[List[str]] = None,
               what_could_improve: Optional[List[str]] = None,
               mistakes: Optional[List[str]] = None,
               lessons_learned: Optional[List[str]] = None,
               confidence_level: int = 3) -> Reflection:
        reflection = Reflection(
            task_id=task_id,
            task_name=task_name,
            what_happened=what_happened,
            what_went_well=what_went_well or [],
            what_could_improve=what_could_improve or [],
            mistakes=mistakes or [],
            lessons_learned=lessons_learned or [],
            confidence_level=confidence_level
        )

        self.reflections[reflection.id] = reflection
        self._generate_improvements(reflection)
        self._update_metrics()
        self._save()

        return reflection

    def _generate_improvements(self, reflection: Reflection):
        for mistake in reflection.mistakes:
            improvement_action = self._suggest_improvement(mistake)
            improvement = Improvement(
                reflection_id=reflection.id,
                original_mistake=mistake,
                improvement_action=improvement_action,
                expected_outcome="减少类似错误再次发生"
            )
            self.improvements[improvement.id] = improvement

        for area in reflection.what_could_improve:
            improvement = Improvement(
                reflection_id=reflection.id,
                original_mistake=area,
                improvement_action=f"改进{area}的方法",
                expected_outcome="提高效率和质量"
            )
            self.improvements[improvement.id] = improvement

    def _suggest_improvement(self, mistake: str) -> str:
        mistake_lower = mistake.lower()

        if "检索" in mistake_lower or "search" in mistake_lower:
            return "增加搜索轮次，使用多种关键词组合"
        elif "规划" in mistake_lower or "plan" in mistake_lower:
            return "制定更详细的任务分解计划"
        elif "代码" in mistake_lower or "code" in mistake_lower:
            return "增加代码审查步骤，确保代码质量"
        elif "沟通" in mistake_lower or "communicate" in mistake_lower:
            return "明确沟通目标和预期结果"
        elif "时间" in mistake_lower or "time" in mistake_lower:
            return "设置更合理的时间节点和里程碑"
        else:
            return f"分析{ mistake }的根本原因，制定预防措施"

    def _update_metrics(self):
        self.metrics.total_reflections = len(self.reflections)
        self.metrics.total_improvements = len(self.improvements)
        self.metrics.successful_improvements = sum(
            1 for i in self.improvements.values() if i.status == "success"
        )

        mistake_counts: Dict[str, int] = {}
        for reflection in self.reflections.values():
            for mistake in reflection.mistakes:
                mistake_counts[mistake] = mistake_counts.get(mistake, 0) + 1

        self.metrics.common_mistakes = sorted(
            mistake_counts.items(), key=lambda x: x[1], reverse=True
        )[:5]
        self.metrics.common_mistakes = [m[0] for m in self.metrics.common_mistakes]

        lesson_counts: Dict[str, int] = {}
        for reflection in self.reflections.values():
            for lesson in reflection.lessons_learned:
                lesson_counts[lesson] = lesson_counts.get(lesson, 0) + 1

        self.metrics.top_lessons = sorted(
            lesson_counts.items(), key=lambda x: x[1], reverse=True
        )[:5]
        self.metrics.top_lessons = [l[0] for l in self.metrics.top_lessons]

        if self.metrics.total_improvements > 0:
            self.metrics.improvement_rate = round(
                self.metrics.successful_improvements / self.metrics.total_improvements, 2
            )

        recent_reflections = sorted(
            self.reflections.values(),
            key=lambda r: r.created_at,
            reverse=True
        )[:10]

        self.metrics.confidence_trend = [
            r.confidence_level for r in recent_reflections
        ]

    def apply_improvement(self, improvement_id: str,
                         actual_outcome: str,
                         success: bool) -> bool:
        improvement = self.improvements.get(improvement_id)
        if not improvement:
            return False

        improvement.actual_outcome = actual_outcome
        improvement.status = "success" if success else "failed"
        improvement.applied_count += 1
        improvement.applied_at = datetime.now()

        if improvement.applied_count > 0:
            previous_successes = sum(
                1 for i in self.improvements.values()
                if i.original_mistake == improvement.original_mistake
                and i.status == "success"
            )
            improvement.success_rate = round(
                previous_successes / improvement.applied_count, 2
            )

        self._update_metrics()
        self._save()
        return True

    def get_reflection(self, reflection_id: str) -> Optional[Reflection]:
        return self.reflections.get(reflection_id)

    def get_recent_reflections(self, limit: int = 20) -> List[Reflection]:
        sorted_refs = sorted(
            self.reflections.values(),
            key=lambda r: r.created_at,
            reverse=True
        )
        return sorted_refs[:limit]

    def get_pending_improvements(self, limit: int = 10) -> List[Improvement]:
        pending = [
            i for i in self.improvements.values()
            if i.status == "pending"
        ]
        return sorted(pending, key=lambda x: x.created_at, reverse=True)[:limit]

    def get_improvements_by_type(self, mistake_type: str) -> List[Improvement]:
        return [
            i for i in self.improvements.values()
            if mistake_type in i.original_mistake
        ]

    def suggest_for_next_task(self, task_name: str) -> List[str]:
        suggestions = []

        task_lower = task_name.lower()

        related_improvements = [
            i for i in self.improvements.values()
            if i.status == "success" and i.success_rate > 0.5
        ]

        for improvement in related_improvements[:5]:
            suggestions.append(
                f"建议: {improvement.improvement_action} "
                f"(成功率: {improvement.success_rate:.0%})"
            )

        recent_reflections = self.get_recent_reflections(5)
        for reflection in recent_reflections:
            for lesson in reflection.lessons_learned[:1]:
                suggestions.append(f"从{reflection.task_name}学到的: {lesson}")

        return suggestions[:5]

    def get_growth_report(self) -> Dict[str, Any]:
        self._update_metrics()

        recent_trend = self.metrics.confidence_trend
        trend_direction = "stable"
        if len(recent_trend) >= 2:
            if recent_trend[0] > recent_trend[-1]:
                trend_direction = "improving"
            elif recent_trend[0] < recent_trend[-1]:
                trend_direction = "declining"

        return {
            "metrics": self.metrics.to_dict(),
            "trend_direction": trend_direction,
            "reflection_count": self.metrics.total_reflections,
            "pending_improvements": len(self.get_pending_improvements()),
            "suggestions": self.suggest_for_next_task("general task")
        }

    def delete_reflection(self, reflection_id: str) -> bool:
        if reflection_id in self.reflections:
            reflection = self.reflections[reflection_id]

            improvements_to_delete = [
                i_id for i_id, i in self.improvements.items()
                if i.reflection_id == reflection_id
            ]
            for i_id in improvements_to_delete:
                del self.improvements[i_id]

            del self.reflections[reflection_id]
            self._update_metrics()
            self._save()
            return True
        return False
