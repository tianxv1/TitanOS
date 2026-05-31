from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
from .task import Task, Workflow, TaskStatus, TaskPriority
from .skill_registry import SkillRegistry
import json
import os


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
