from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from .runtime import Runtime
from .task import Task, Workflow, TaskStatus, TaskPriority
from .skill_registry import SkillRegistry, Skill


class Agent:
    """
    Agent System - 预测、帮助、替你执行
    
    提供统一的智能交互接口，支持：
    - 任务预测：基于历史数据预测任务执行时间
    - 智能帮助：提供任务执行建议和优化建议
    - 自动执行：自动执行任务和工作流
    """
    
    def __init__(self, name: str = "TitanOS Agent"):
        self.name = name
        self.runtime = Runtime()
        self.skill_registry = self.runtime.skill_registry
        self._init_prompt()
    
    def _init_prompt(self):
        """初始化 Agent 提示信息"""
        self.intro_prompt = f"""
你好！我是 {self.name}，你的智能助手。

我可以帮助你：
📅 任务管理 - 创建、执行和管理任务
🔄 工作流 - 创建和执行复杂工作流
⚡ 技能调用 - 使用各种内置技能（搜索、文件操作、数据分析等）
📊 智能预测 - 预测任务执行时间
💡 智能建议 - 提供优化建议

输入 'help' 获取帮助信息。
        """.strip()
    
    def say_hello(self) -> str:
        """返回欢迎信息"""
        return self.intro_prompt
    
    def get_help(self) -> Dict[str, Any]:
        """获取帮助信息"""
        help_info = {
            "agent_name": self.name,
            "available_commands": [
                {
                    "command": "create_task",
                    "description": "创建新任务",
                    "parameters": {
                        "name": "任务名称",
                        "task_type": "任务类型（skill/search/analyze/summarize/composite/general）",
                        "input_data": "输入数据（字典）",
                        "priority": "优先级（LOW/MEDIUM/HIGH/CRITICAL）",
                        "dependencies": "依赖任务ID列表"
                    }
                },
                {
                    "command": "execute_task",
                    "description": "执行任务",
                    "parameters": {"task_id": "任务ID"}
                },
                {
                    "command": "create_workflow",
                    "description": "创建工作流",
                    "parameters": {"name": "工作流名称", "description": "工作流描述"}
                },
                {
                    "command": "execute_workflow",
                    "description": "执行工作流",
                    "parameters": {"workflow_id": "工作流ID"}
                },
                {
                    "command": "list_tasks",
                    "description": "列出所有任务"
                },
                {
                    "command": "list_workflows",
                    "description": "列出所有工作流"
                },
                {
                    "command": "list_skills",
                    "description": "列出可用技能"
                },
                {
                    "command": "execute_skill",
                    "description": "直接执行技能",
                    "parameters": {"skill_name": "技能名称", "params": "技能参数"}
                },
                {
                    "command": "predict",
                    "description": "预测任务/工作流执行时间",
                    "parameters": {"target_id": "任务或工作流ID", "target_type": "task/workflow"}
                },
                {
                    "command": "recommend",
                    "description": "获取智能建议"
                },
                {
                    "command": "auto_execute",
                    "description": "自动执行优先级任务",
                    "parameters": {"limit": "最大执行任务数"}
                },
                {
                    "command": "optimize",
                    "description": "优化工作流",
                    "parameters": {"workflow_id": "工作流ID"}
                },
                {
                    "command": "help",
                    "description": "显示帮助信息"
                }
            ],
            "available_skills": [skill.name for skill in self.skill_registry.skills.values()]
        }
        return help_info
    
    def create_task(self, name: str, task_type: str = "general",
                    input_data: Optional[Dict[str, Any]] = None,
                    priority: str = "MEDIUM",
                    dependencies: Optional[List[str]] = None) -> Task:
        """创建任务"""
        priority_enum = TaskPriority[priority.upper()]
        return self.runtime.create_task(
            name=name,
            task_type=task_type,
            input_data=input_data,
            priority=priority_enum,
            dependencies=dependencies
        )
    
    def execute_task(self, task_id: str) -> Dict[str, Any]:
        """执行任务"""
        return self.runtime.execute_task(task_id)
    
    def create_workflow(self, name: str, description: str = "") -> Workflow:
        """创建工作流"""
        return self.runtime.create_workflow(name=name, description=description)
    
    def add_task_to_workflow(self, workflow_id: str, task: Task) -> bool:
        """向工作流添加任务"""
        return self.runtime.add_task_to_workflow(workflow_id, task)
    
    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """执行工作流"""
        return self.runtime.execute_workflow(workflow_id)
    
    def list_tasks(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出任务"""
        if status:
            try:
                status_enum = TaskStatus[status.upper()]
                return self.runtime.list_tasks(status=status_enum)
            except KeyError:
                return {"error": f"Invalid status: {status}"}
        return self.runtime.list_tasks()
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """列出工作流"""
        return self.runtime.list_workflows()
    
    def list_skills(self, enabled_only: bool = True) -> List[Dict[str, Any]]:
        """列出可用技能"""
        if enabled_only:
            return self.skill_registry.list_enabled()
        return self.skill_registry.list_all()
    
    def execute_skill(self, skill_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """直接执行技能"""
        return self.skill_registry.execute(skill_name, params)
    
    def predict(self, target_id: str, target_type: str = "task") -> Dict[str, Any]:
        """预测任务或工作流执行时间"""
        if target_type.lower() == "workflow":
            return self.runtime.predict_workflow_duration(target_id)
        else:
            task = self.runtime.get_task(target_id)
            if not task:
                return {"error": f"Task {target_id} not found"}
            return {
                "task_id": task.id,
                "task_name": task.name,
                "predicted_duration": self.runtime.predict_task_duration(task),
                "estimated_completion_time": (datetime.now() + 
                    datetime.timedelta(seconds=self.runtime.predict_task_duration(task))).isoformat()
            }
    
    def recommend(self) -> Dict[str, Any]:
        """获取智能建议"""
        recommendations = self.runtime.get_task_recommendations()
        
        workflow_issues = []
        for wf in self.runtime.workflows.values():
            opt_result = self.runtime.optimize_workflow(wf.id)
            if opt_result.get("issues"):
                workflow_issues.append({
                    "workflow_id": wf.id,
                    "workflow_name": wf.name,
                    "issues": opt_result["issues"]
                })
        
        recommendations["workflow_issues"] = workflow_issues
        
        return recommendations
    
    def auto_execute(self, limit: int = 5) -> Dict[str, Any]:
        """自动执行优先级最高的任务"""
        return self.runtime.execute_priority_tasks(limit=limit)
    
    def optimize(self, workflow_id: str) -> Dict[str, Any]:
        """优化工作流"""
        return self.runtime.optimize_workflow(workflow_id)
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务详情"""
        return self.runtime.get_task(task_id)
    
    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """获取工作流详情"""
        return self.runtime.get_workflow(workflow_id)
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        return self.runtime.cancel_task(task_id)
    
    def get_execution_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """获取执行历史"""
        return self.runtime.get_execution_history(limit=limit)
    
    def schedule_tasks(self, strategy: str = "priority") -> List[str]:
        """智能调度任务"""
        return self.runtime.schedule_tasks(strategy=strategy)
    
    def process_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """处理命令输入"""
        command = command.lower().strip()
        
        command_map = {
            "create_task": lambda: {
                "result": self.create_task(
                    name=kwargs.get("name", ""),
                    task_type=kwargs.get("task_type", "general"),
                    input_data=kwargs.get("input_data"),
                    priority=kwargs.get("priority", "MEDIUM"),
                    dependencies=kwargs.get("dependencies")
                ).to_dict()
            },
            "execute_task": lambda: self.execute_task(kwargs.get("task_id", "")),
            "create_workflow": lambda: {
                "result": self.create_workflow(
                    name=kwargs.get("name", ""),
                    description=kwargs.get("description", "")
                ).to_dict()
            },
            "execute_workflow": lambda: self.execute_workflow(kwargs.get("workflow_id", "")),
            "list_tasks": lambda: {"tasks": self.list_tasks(kwargs.get("status"))},
            "list_workflows": lambda: {"workflows": self.list_workflows()},
            "list_skills": lambda: {"skills": self.list_skills(kwargs.get("enabled_only", True))},
            "execute_skill": lambda: self.execute_skill(
                skill_name=kwargs.get("skill_name", ""),
                params=kwargs.get("params", {})
            ),
            "predict": lambda: self.predict(
                target_id=kwargs.get("target_id", ""),
                target_type=kwargs.get("target_type", "task")
            ),
            "recommend": lambda: self.recommend(),
            "auto_execute": lambda: self.auto_execute(kwargs.get("limit", 5)),
            "optimize": lambda: self.optimize(kwargs.get("workflow_id", "")),
            "help": lambda: self.get_help(),
            "hello": lambda: {"message": self.say_hello()}
        }
        
        if command in command_map:
            try:
                return {"status": "success", **command_map[command]()}
            except Exception as e:
                return {"status": "error", "message": str(e)}
        else:
            return {
                "status": "error",
                "message": f"Unknown command: {command}",
                "available_commands": [cmd for cmd in command_map.keys()]
            }
    
    def chat(self, message: str) -> str:
        """简单的聊天接口"""
        message = message.strip().lower()
        
        if message in ["hello", "hi", "你好"]:
            return self.say_hello()
        
        if message in ["help", "帮助"]:
            help_info = self.get_help()
            response = "可用命令：\n"
            for cmd in help_info["available_commands"]:
                response += f"- {cmd['command']}: {cmd['description']}\n"
            response += "\n可用技能：" + ", ".join(help_info["available_skills"])
            return response
        
        if message.startswith("create task"):
            task_name = message.replace("create task", "").strip()
            task = self.create_task(name=task_name)
            return f"已创建任务: {task.name} (ID: {task.id})"
        
        if message.startswith("list tasks"):
            tasks = self.list_tasks()
            if tasks:
                response = "任务列表：\n"
                for task in tasks:
                    response += f"- {task['name']} ({task['status']})\n"
                return response
            return "暂无任务"
        
        if message.startswith("list skills"):
            skills = self.list_skills()
            return "可用技能：" + ", ".join(skill["name"] for skill in skills)
        
        if message.startswith("recommend"):
            recs = self.recommend()
            response = "智能建议：\n"
            for rec in recs.get("recommendations", []):
                response += f"- {rec['message']}\n"
            return response
        
        if message.startswith("auto execute"):
            result = self.auto_execute()
            return f"已执行 {result['executed_tasks']} 个任务"
        
        return f"我不太理解你的请求。输入 'help' 获取可用命令列表。"