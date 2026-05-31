from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional
from memory.memory_engine import MemoryEngine
from knowledge_graph.knowledge_graph import KnowledgeGraph
from planner.planner import Planner
from learning.learning_engine import LearningEngine
from digital_twin.digital_twin import DigitalTwin
from agent.runtime import Runtime
from reflection.reflection_engine import ReflectionEngine


@dataclass
class GrowthMetrics:
    total_memories: int = 0
    total_experiences: int = 0
    total_knowledge_nodes: int = 0
    total_tasks: int = 0
    completed_tasks: int = 0
    task_completion_rate: float = 0.0
    growth_score: int = 0
    digital_twin_maturity: float = 0.0
    learning_progress: float = 0.0
    reflection_count: int = 0
    improvement_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_memories": self.total_memories,
            "total_experiences": self.total_experiences,
            "total_knowledge_nodes": self.total_knowledge_nodes,
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "task_completion_rate": self.task_completion_rate,
            "growth_score": self.growth_score,
            "digital_twin_maturity": self.digital_twin_maturity,
            "learning_progress": self.learning_progress,
            "reflection_count": self.reflection_count,
            "improvement_count": self.improvement_count,
            "calculated_at": datetime.now().isoformat()
        }


class GrowthDashboard:
    def __init__(self):
        self.memory_engine = MemoryEngine()
        self.knowledge_graph = KnowledgeGraph()
        self.planner = Planner()
        self.learning_engine = LearningEngine()
        self.digital_twin = DigitalTwin()
        self.agent_runtime = Runtime()
        self.reflection_engine = ReflectionEngine()

    def calculate_task_completion_rate(self) -> float:
        plans = self.planner.get_all_plans()
        total_tasks = 0
        completed_tasks = 0

        for plan in plans:
            for milestone in plan.milestones:
                for task in milestone.tasks:
                    total_tasks += 1
                    if task.status == "completed":
                        completed_tasks += 1

        if total_tasks == 0:
            return 0.0
        return completed_tasks / total_tasks

    def calculate_growth_score(self) -> int:
        scores = []

        memories = self.memory_engine.get_all_memories()
        memory_score = min(len(memories) * 2, 25)
        scores.append(memory_score)

        experiences = self.learning_engine.get_all_experiences()
        experience_score = min(len(experiences) * 3, 20)
        scores.append(experience_score)

        entities = self.knowledge_graph.get_all_entities()
        knowledge_score = min(len(entities) * 2, 20)
        scores.append(knowledge_score)

        task_rate = self.calculate_task_completion_rate()
        task_score = int(task_rate * 20)
        scores.append(task_score)

        reflections = self.reflection_engine.get_all_reflections()
        reflection_score = min(len(reflections) * 3, 15)
        scores.append(reflection_score)

        total = sum(scores)
        return min(total, 100)

    def calculate_digital_twin_maturity(self) -> float:
        profile = self.digital_twin.get_profile()

        completeness = 0.0
        factors = 0

        if profile.name:
            completeness += 0.1
            factors += 1
        if profile.age:
            completeness += 0.1
            factors += 1
        if profile.gender:
            completeness += 0.1
            factors += 1
        if profile.bio:
            completeness += 0.15
            factors += 1
        if profile.avatar_url:
            completeness += 0.1
            factors += 1
        if profile.writing_style and profile.writing_style.traits:
            completeness += 0.2
            factors += 1
        if profile.code_style and profile.code_style.languages:
            completeness += 0.15
            factors += 1
        if profile.learning_style:
            completeness += 0.1
            factors += 1

        memories = self.memory_engine.get_all_memories()
        if len(memories) > 0:
            completeness += min(len(memories) * 0.02, 0.2)

        return min(completeness, 1.0)

    def calculate_learning_progress(self) -> float:
        experiences = self.learning_engine.get_all_experiences()
        patterns = self.learning_engine.get_all_patterns()

        total_weight = 0.0
        achieved_weight = 0.0

        for exp in experiences:
            total_weight += exp.importance
            if exp.learned:
                achieved_weight += exp.importance

        for pattern in patterns:
            total_weight += pattern.confidence
            achieved_weight += pattern.confidence

        if total_weight == 0:
            return 0.0

        return min(achieved_weight / total_weight, 1.0)

    def get_metrics(self) -> GrowthMetrics:
        metrics = GrowthMetrics()

        metrics.total_memories = len(self.memory_engine.get_all_memories())
        metrics.total_experiences = len(self.learning_engine.get_all_experiences())
        metrics.total_knowledge_nodes = len(self.knowledge_graph.get_all_entities())

        plans = self.planner.get_all_plans()
        for plan in plans:
            for milestone in plan.milestones:
                for task in milestone.tasks:
                    metrics.total_tasks += 1
                    if task.status == "completed":
                        metrics.completed_tasks += 1

        metrics.task_completion_rate = self.calculate_task_completion_rate()
        metrics.growth_score = self.calculate_growth_score()
        metrics.digital_twin_maturity = self.calculate_digital_twin_maturity()
        metrics.learning_progress = self.calculate_learning_progress()

        metrics.reflection_count = len(self.reflection_engine.get_all_reflections())
        metrics.improvement_count = len(self.reflection_engine.get_all_improvements())

        return metrics

    def get_detailed_report(self) -> Dict[str, Any]:
        metrics = self.get_metrics()

        return {
            "overview": {
                "title": "Growth Dashboard",
                "period": "Lifetime",
                "generated_at": datetime.now().isoformat()
            },
            "core_metrics": metrics.to_dict(),
            "breakdown": {
                "memory": {
                    "label": "Memory Growth",
                    "value": metrics.total_memories,
                    "unit": "memories",
                    "trend": "up"
                },
                "knowledge": {
                    "label": "Knowledge Expansion",
                    "value": metrics.total_knowledge_nodes,
                    "unit": "nodes",
                    "trend": "up"
                },
                "learning": {
                    "label": "Learning Progress",
                    "value": f"{int(metrics.learning_progress * 100)}%",
                    "unit": "completion",
                    "trend": "up"
                },
                "productivity": {
                    "label": "Task Completion",
                    "value": f"{int(metrics.task_completion_rate * 100)}%",
                    "unit": "rate",
                    "trend": "stable"
                }
            },
            "growth_score": {
                "value": metrics.growth_score,
                "max": 100,
                "level": self._get_growth_level(metrics.growth_score),
                "next_level_requirement": self._get_next_level_requirement(metrics.growth_score)
            },
            "digital_twin": {
                "maturity": f"{int(metrics.digital_twin_maturity * 100)}%",
                "status": self._get_twin_status(metrics.digital_twin_maturity)
            },
            "recommendations": self._generate_recommendations(metrics)
        }

    def _get_growth_level(self, score: int) -> str:
        if score >= 90:
            return "Master"
        elif score >= 70:
            return "Expert"
        elif score >= 50:
            return "Advanced"
        elif score >= 30:
            return "Intermediate"
        elif score >= 10:
            return "Beginner"
        else:
            return "Newborn"

    def _get_next_level_requirement(self, score: int) -> Optional[str]:
        if score >= 90:
            return None
        elif score >= 70:
            return f"Need {90 - score} more points to reach Master level"
        elif score >= 50:
            return f"Need {70 - score} more points to reach Expert level"
        elif score >= 30:
            return f"Need {50 - score} more points to reach Advanced level"
        elif score >= 10:
            return f"Need {30 - score} more points to reach Intermediate level"
        else:
            return f"Need {10 - score} more points to reach Beginner level"

    def _get_twin_status(self, maturity: float) -> str:
        if maturity >= 0.8:
            return "Fully Developed"
        elif maturity >= 0.6:
            return "Well Developed"
        elif maturity >= 0.4:
            return "Developing"
        elif maturity >= 0.2:
            return "Emerging"
        else:
            return "Initializing"

    def _generate_recommendations(self, metrics: GrowthMetrics) -> list:
        recommendations = []

        if metrics.total_memories < 10:
            recommendations.append("Add more memories to improve your knowledge base")
        if metrics.task_completion_rate < 0.5:
            recommendations.append("Complete pending tasks to boost productivity")
        if metrics.reflection_count < 5:
            recommendations.append("Reflect on completed tasks to learn from experiences")
        if metrics.digital_twin_maturity < 0.5:
            recommendations.append("Complete your Digital Twin profile")
        if metrics.total_knowledge_nodes < 20:
            recommendations.append("Explore more knowledge to expand your knowledge graph")

        return recommendations

    def get_summary(self) -> Dict[str, Any]:
        metrics = self.get_metrics()
        return {
            "growth_score": metrics.growth_score,
            "total_memories": metrics.total_memories,
            "total_experiences": metrics.total_experiences,
            "total_knowledge_nodes": metrics.total_knowledge_nodes,
            "task_completion_rate": round(metrics.task_completion_rate * 100, 1),
            "digital_twin_maturity": round(metrics.digital_twin_maturity * 100, 1),
            "learning_progress": round(metrics.learning_progress * 100, 1)
        }
