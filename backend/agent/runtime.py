from typing import List, Dict, Any, Optional, Callable, Tuple
from datetime import datetime, timedelta
from .task import Task, Workflow, TaskStatus, TaskPriority
from .skill_registry import SkillRegistry
import json
import os
import heapq
from collections import defaultdict


class Runtime:
    def __init__(self):
        self.task_registry: Dict[str, Task] = {}
        self.workflows: Dict[str, Workflow] = {}
        self.skill_registry = SkillRegistry()
        self.execution_history: List[Dict[str, Any]] = []
        self._load_state()

    def _load_state(self):
        state_path = "database/agent_state.json"
        if os.path.exists(state_path):
            try:
                with open(state_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.execution_history = data.get("history", [])
            except Exception:
                pass

    def _save_state(self):
        os.makedirs("database", exist_ok=True)
        state_path = "database/agent_state.json"
        data = {
            "history": self.execution_history[-100:]
        }
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def create_task(self, name: str, task_type: str = "general",
                   input_data: Optional[Dict[str, Any]] = None,
                   priority: TaskPriority = TaskPriority.MEDIUM,
                   dependencies: Optional[List[str]] = None) -> Task:
        task = Task(
            name=name,
            task_type=task_type,
            input_data=input_data or {},
            priority=priority,
            dependencies=dependencies or []
        )
        self.task_registry[task.id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.task_registry.get(task_id)

    def execute_task(self, task_id: str) -> Dict[str, Any]:
        task = self.task_registry.get(task_id)
        if not task:
            return {"error": f"Task {task_id} not found", "status": "error"}

        if task.dependencies:
            for dep_id in task.dependencies:
                dep_task = self.task_registry.get(dep_id)
                if dep_task and dep_task.status != TaskStatus.COMPLETED:
                    return {"error": f"Dependency {dep_id} not completed", "status": "error"}

        task.start()

        try:
            result = self._execute_task_logic(task)
            task.complete(result)

            self.execution_history.append({
                "task_id": task.id,
                "task_name": task.name,
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "output": result
            })

            self._save_state()
            return {"task": task.to_dict(), "status": "completed"}

        except Exception as e:
            task.fail(str(e))
            self.execution_history.append({
                "task_id": task.id,
                "task_name": task.name,
                "status": "failed",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            })
            self._save_state()
            return {"task": task.to_dict(), "status": "failed", "error": str(e)}

    def _execute_task_logic(self, task: Task) -> Dict[str, Any]:
        task_type = task.task_type
        params = task.input_data

        if task_type == "skill":
            skill_name = params.get("skill", "")
            skill_params = params.get("params", {})
            return self.skill_registry.execute(skill_name, skill_params)

        elif task_type == "search":
            return self.skill_registry.execute("search", params)

        elif task_type == "analyze":
            return self.skill_registry.execute("analyze", params)

        elif task_type == "summarize":
            return self.skill_registry.execute("summarize", params)

        elif task_type == "composite":
            results = {}
            for step_name, step_params in params.get("steps", []):
                skill_name = step_params.get("skill", "")
                skill_params = step_params.get("params", {})
                results[step_name] = self.skill_registry.execute(skill_name, skill_params)
            return {"steps": results}

        else:
            return {
                "message": f"Executed {task_type} task",
                "params": params,
                "result": "Task completed successfully"
            }

    def create_workflow(self, name: str, description: str = "") -> Workflow:
        workflow = Workflow(name=name, description=description)
        self.workflows[workflow.id] = workflow
        return workflow

    def add_task_to_workflow(self, workflow_id: str, task: Task) -> bool:
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return False
        workflow.tasks.append(task)
        return True

    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {"error": f"Workflow {workflow_id} not found", "status": "error"}

        workflow.status = "running"
        results = {}

        for task in workflow.tasks:
            if task.dependencies:
                deps_completed = all(
                    self.task_registry.get(dep_id).status == TaskStatus.COMPLETED
                    for dep_id in task.dependencies
                    if self.task_registry.get(dep_id)
                )
                if not deps_completed:
                    task.fail("Dependencies not satisfied")
                    workflow.status = "failed"
                    continue

            result = self.execute_task(task.id)
            results[task.id] = result

            if result.get("status") == "failed":
                workflow.status = "failed"
                break

        workflow.status = "completed" if workflow.status == "running" else "failed"
        workflow.results = results

        return {
            "workflow": workflow.to_dict(),
            "results": results,
            "status": workflow.status
        }

    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        return self.workflows.get(workflow_id)

    def list_tasks(self, status: Optional[TaskStatus] = None) -> List[Dict[str, Any]]:
        tasks = self.task_registry.values()
        if status:
            tasks = [t for t in tasks if t.status == status]
        return [t.to_dict() for t in tasks]

    def list_workflows(self) -> List[Dict[str, Any]]:
        return [w.to_dict() for w in self.workflows.values()]

    def get_execution_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self.execution_history[-limit:]

    def cancel_task(self, task_id: str) -> bool:
        task = self.task_registry.get(task_id)
        if not task:
            return False
        if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            return False
        task.status = TaskStatus.CANCELLED
        task.completed_at = datetime.now()
        return True

    def predict_task_duration(self, task: Task) -> float:
        """预测任务执行时间（基于历史数据）"""
        task_type = task.task_type
        similar_tasks = [
            h for h in self.execution_history
            if h.get("task_name", "").startswith(task.name[:5]) or 
               any(t.get("task_type") == task_type for t in self.task_registry.values())
        ]
        
        if similar_tasks:
            durations = []
            for hist in similar_tasks:
                if hist.get("status") == "completed":
                    durations.append(0.5)
            if durations:
                return sum(durations) / len(durations) * 1.2
        
        base_duration = {
            "skill": 1.0,
            "search": 2.0,
            "analyze": 3.0,
            "summarize": 1.5,
            "composite": 5.0,
            "general": 0.5
        }
        return base_duration.get(task_type, 1.0)

    def predict_workflow_duration(self, workflow_id: str) -> Dict[str, Any]:
        """预测工作流执行时间"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {"error": f"Workflow {workflow_id} not found"}
        
        total_duration = 0.0
        task_predictions = []
        
        for task in workflow.tasks:
            pred = self.predict_task_duration(task)
            task_predictions.append({
                "task_id": task.id,
                "task_name": task.name,
                "predicted_duration": pred,
                "priority": task.priority.value
            })
            total_duration += pred
        
        return {
            "workflow_id": workflow_id,
            "workflow_name": workflow.name,
            "total_predicted_duration": total_duration,
            "task_predictions": task_predictions,
            "estimated_completion_time": (datetime.now() + timedelta(seconds=total_duration)).isoformat()
        }

    def schedule_tasks(self, strategy: str = "priority") -> List[str]:
        """智能任务调度，返回排序后的任务ID列表"""
        pending_tasks = [
            t for t in self.task_registry.values()
            if t.status == TaskStatus.PENDING
        ]
        
        if strategy == "priority":
            sorted_tasks = sorted(pending_tasks, key=lambda t: t.priority.value, reverse=True)
        elif strategy == "shortest_first":
            sorted_tasks = sorted(pending_tasks, key=self.predict_task_duration)
        elif strategy == "dependency":
            sorted_tasks = self._schedule_by_dependency(pending_tasks)
        else:
            sorted_tasks = pending_tasks
        
        return [t.id for t in sorted_tasks]

    def _schedule_by_dependency(self, tasks: List[Task]) -> List[Task]:
        """基于依赖关系的拓扑排序"""
        task_map = {t.id: t for t in tasks}
        in_degree = {t.id: len(t.dependencies) for t in tasks}
        queue = [t for t in tasks if in_degree[t.id] == 0]
        result = []
        
        while queue:
            task = queue.pop(0)
            result.append(task)
            
            for other in tasks:
                if task.id in other.dependencies:
                    in_degree[other.id] -= 1
                    if in_degree[other.id] == 0:
                        queue.append(other)
        
        return result

    def optimize_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """优化工作流，提供改进建议"""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {"error": f"Workflow {workflow_id} not found"}
        
        suggestions = []
        issues = []
        
        tasks_by_type = defaultdict(list)
        for task in workflow.tasks:
            tasks_by_type[task.task_type].append(task)
        
        if len(workflow.tasks) > 10:
            suggestions.append("考虑将工作流拆分为多个较小的工作流以提高可维护性")
        
        for task_type, tasks in tasks_by_type.items():
            if len(tasks) > 5:
                suggestions.append(f"类型为 '{task_type}' 的任务较多，考虑并行执行")
        
        for task in workflow.tasks:
            if not task.name:
                issues.append(f"任务 {task.id} 缺少名称")
            if task.dependencies:
                for dep_id in task.dependencies:
                    if dep_id not in self.task_registry:
                        issues.append(f"任务 {task.id} 的依赖 {dep_id} 不存在")
        
        critical_path = self._find_critical_path(workflow)
        
        return {
            "workflow_id": workflow_id,
            "suggestions": suggestions,
            "issues": issues,
            "critical_path": critical_path,
            "task_count": len(workflow.tasks),
            "optimization_score": self._calculate_optimization_score(workflow, suggestions, issues)
        }

    def _find_critical_path(self, workflow: Workflow) -> List[str]:
        """找到工作流的关键路径"""
        if not workflow.tasks:
            return []
        
        task_durations = {t.id: self.predict_task_duration(t) for t in workflow.tasks}
        task_map = {t.id: t for t in workflow.tasks}
        
        def calculate_critical_time(task_id: str) -> float:
            task = task_map.get(task_id)
            if not task:
                return 0
            if not task.dependencies:
                return task_durations[task_id]
            max_dep_time = max(
                calculate_critical_time(dep_id) for dep_id in task.dependencies
                if dep_id in task_map
            )
            return max_dep_time + task_durations[task_id]
        
        critical_path = []
        current_task = max(workflow.tasks, key=lambda t: calculate_critical_time(t.id))
        critical_path.append(current_task.id)
        
        while current_task.dependencies:
            dep_times = [(dep_id, calculate_critical_time(dep_id)) for dep_id in current_task.dependencies]
            if dep_times:
                current_task_id = max(dep_times, key=lambda x: x[1])[0]
                current_task = task_map.get(current_task_id)
                if current_task:
                    critical_path.append(current_task_id)
        
        return list(reversed(critical_path))

    def _calculate_optimization_score(self, workflow: Workflow, suggestions: List[str], issues: List[str]) -> int:
        """计算工作流优化分数"""
        score = 100
        
        score -= len(issues) * 10
        score -= len(suggestions) * 5
        
        if len(workflow.tasks) > 20:
            score -= 10
        if any(t.priority == TaskPriority.CRITICAL for t in workflow.tasks):
            score += 5
        
        return max(0, score)

    def execute_priority_tasks(self, limit: int = 5) -> Dict[str, Any]:
        """自动执行优先级最高的待处理任务"""
        scheduled = self.schedule_tasks(strategy="priority")[:limit]
        results = {}
        
        for task_id in scheduled:
            result = self.execute_task(task_id)
            results[task_id] = result
        
        return {
            "executed_tasks": len(results),
            "results": results,
            "scheduled_tasks": scheduled
        }

    def get_task_recommendations(self) -> Dict[str, Any]:
        """获取任务执行建议"""
        pending_tasks = [t for t in self.task_registry.values() if t.status == TaskStatus.PENDING]
        waiting_tasks = [t for t in self.task_registry.values() if t.status == TaskStatus.WAITING]
        
        recommendations = []
        
        if pending_tasks:
            high_priority = [t for t in pending_tasks if t.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL]]
            if high_priority:
                recommendations.append({
                    "type": "high_priority",
                    "message": f"有 {len(high_priority)} 个高优先级任务等待执行",
                    "tasks": [t.to_dict() for t in high_priority]
                })
        
        if waiting_tasks:
            recommendations.append({
                "type": "waiting_dependencies",
                "message": f"有 {len(waiting_tasks)} 个任务等待依赖完成",
                "tasks": [t.to_dict() for t in waiting_tasks]
            })
        
        avg_wait_time = self._calculate_average_wait_time()
        if avg_wait_time > 30:
            recommendations.append({
                "type": "long_wait",
                "message": f"任务平均等待时间较长 ({avg_wait_time:.1f}秒)，建议及时处理"
            })
        
        return {
            "recommendations": recommendations,
            "pending_count": len(pending_tasks),
            "waiting_count": len(waiting_tasks),
            "total_tasks": len(self.task_registry)
        }

    def _calculate_average_wait_time(self) -> float:
        """计算任务平均等待时间（秒）"""
        pending_tasks = [t for t in self.task_registry.values() if t.status == TaskStatus.PENDING]
        if not pending_tasks:
            return 0
        
        now = datetime.now()
        total_wait = sum((now - t.created_at).total_seconds() for t in pending_tasks)
        return total_wait / len(pending_tasks)

    def batch_execute(self, task_ids: List[str]) -> Dict[str, Any]:
        """批量执行任务"""
        results = {}
        successful = 0
        failed = 0
        
        for task_id in task_ids:
            result = self.execute_task(task_id)
            results[task_id] = result
            if result.get("status") == "completed":
                successful += 1
            else:
                failed += 1
        
        return {
            "total": len(task_ids),
            "successful": successful,
            "failed": failed,
            "results": results
        }
