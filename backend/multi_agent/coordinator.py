from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional, Callable, Tuple
import uuid
import json
import os


AGENT_TYPES = ["research", "planner", "coding", "reviewer", "search", "analyzer", "summarizer"]


@dataclass
class AgentMessage:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = ""
    receiver_id: str = ""
    content: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    message_type: str = "task"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "message_type": self.message_type,
            "metadata": self.metadata
        }


@dataclass
class AgentTask:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    agent_type: str = ""
    status: str = "pending"
    priority: int = 3
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "agent_type": self.agent_type,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error
        }


@dataclass
class Agent:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    agent_type: str = ""
    description: str = ""
    skills: List[str] = field(default_factory=list)
    status: str = "idle"
    task_history: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "agent_type": self.agent_type,
            "description": self.description,
            "skills": self.skills,
            "status": self.status,
            "task_history": self.task_history
        }


class AgentCoordinator:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, AgentTask] = {}
        self.messages: List[AgentMessage] = []
        self._initialize_default_agents()
        self._load_state()

    def _initialize_default_agents(self):
        default_agents = [
            {
                "name": "SearchAgent",
                "agent_type": "search",
                "description": "搜索信息和资料",
                "skills": ["web_search", "information_retrieval", "data_finding"]
            },
            {
                "name": "ResearchAgent",
                "agent_type": "research",
                "description": "深入研究和分析主题",
                "skills": ["deep_research", "analysis", "synthesis"]
            },
            {
                "name": "CrawlerAgent",
                "agent_type": "search",
                "description": "爬取网页内容",
                "skills": ["web_crawling", "content_extraction"]
            },
            {
                "name": "CodingAgent",
                "agent_type": "coding",
                "description": "编写代码",
                "skills": ["python", "javascript", "typescript", "web_development"]
            },
            {
                "name": "ReviewerAgent",
                "agent_type": "reviewer",
                "description": "审查和优化代码",
                "skills": ["code_review", "quality_assurance", "optimization"]
            },
            {
                "name": "PlannerAgent",
                "agent_type": "planner",
                "description": "规划任务和项目",
                "skills": ["planning", "task_decomposition", "resource_allocation"]
            },
            {
                "name": "AnalyzerAgent",
                "agent_type": "analyzer",
                "description": "分析数据和结果",
                "skills": ["data_analysis", "reporting", "insights"]
            },
            {
                "name": "SummarizerAgent",
                "agent_type": "summarizer",
                "description": "总结和提炼信息",
                "skills": ["summarization", "content_synthesis", "abstracting"]
            }
        ]

        for agent_data in default_agents:
            if agent_data["name"] not in [a.name for a in self.agents.values()]:
                agent = Agent(
                    name=agent_data["name"],
                    agent_type=agent_data["agent_type"],
                    description=agent_data["description"],
                    skills=agent_data["skills"]
                )
                self.agents[agent.id] = agent

    def _load_state(self):
        if os.path.exists("database/agents.json"):
            try:
                with open("database/agents.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for agent_data in data.get("agents", []):
                        agent = Agent(**agent_data)
                        self.agents[agent.id] = agent
            except Exception:
                pass

    def _save_state(self):
        os.makedirs("database", exist_ok=True)
        data = {
            "agents": [agent.to_dict() for agent in self.agents.values()],
            "saved_at": datetime.now().isoformat()
        }
        with open("database/agents.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_agent(self, name: str, agent_type: str, description: str, skills: List[str]) -> Agent:
        if agent_type not in AGENT_TYPES:
            raise ValueError(f"Invalid agent type. Must be one of: {AGENT_TYPES}")

        agent = Agent(
            name=name,
            agent_type=agent_type,
            description=description,
            skills=skills
        )
        self.agents[agent.id] = agent
        self._save_state()
        return agent

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        return self.agents.get(agent_id)

    def get_agents_by_type(self, agent_type: str) -> List[Agent]:
        return [agent for agent in self.agents.values() if agent.agent_type == agent_type]

    def list_agents(self) -> List[Dict[str, Any]]:
        return [agent.to_dict() for agent in self.agents.values()]

    def assign_task(self, agent_id: str, title: str, description: str) -> Optional[AgentTask]:
        agent = self.agents.get(agent_id)
        if not agent:
            return None

        task = AgentTask(
            title=title,
            description=description,
            agent_type=agent.agent_type
        )
        self.tasks[task.id] = task

        agent.status = "working"
        task.status = "in_progress"
        task.started_at = datetime.now()
        agent.task_history.append(task.id)

        self._save_state()
        return task

    def execute_task(self, task_id: str) -> AgentTask:
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError("Task not found")

        agent = self._find_agent_by_task(task)
        if agent:
            agent.status = "working"

        task.status = "in_progress"
        
        simulated_result = self._simulate_execution(task)
        task.result = simulated_result
        task.status = "completed"
        task.completed_at = datetime.now()

        if agent:
            agent.status = "idle"

        self._save_state()
        return task

    def _find_agent_by_task(self, task: AgentTask) -> Optional[Agent]:
        for agent in self.agents.values():
            if task.id in agent.task_history:
                return agent
        return None

    def _simulate_execution(self, task: AgentTask) -> str:
        agent_type = task.agent_type
        
        if agent_type == "research":
            return f"研究完成：已收集关于 '{task.title}' 的详细资料，包括主要概念、最新进展和相关资源。"
        elif agent_type == "planner":
            return f"规划完成：已为 '{task.title}' 创建详细计划，包括任务分解、时间安排和资源分配。"
        elif agent_type == "coding":
            return f"编码完成：已实现 '{task.title}' 的核心功能代码，包含单元测试和文档。"
        elif agent_type == "reviewer":
            return f"审查完成：已审查 '{task.title}'，发现并修复了 {self._random_int(1, 5)} 个问题，代码质量已提升。"
        elif agent_type == "search":
            return f"搜索完成：为 '{task.title}' 找到了 {self._random_int(5, 15)} 个相关资源和参考链接。"
        elif agent_type == "analyzer":
            return f"分析完成：'{task.title}' 的数据分析报告已生成，包含关键洞察和建议。"
        elif agent_type == "summarizer":
            return f"总结完成：'{task.title}' 的内容已提炼为简明摘要，核心要点清晰呈现。"
        else:
            return f"任务 '{task.title}' 已完成。"

    def _random_int(self, min_val: int, max_val: int) -> int:
        import random
        return random.randint(min_val, max_val)

    def create_workflow(self, goal: str) -> Dict[str, Any]:
        tasks = []
        
        research_task = AgentTask(
            title=f"研究: {goal}",
            description=f"深入研究{goal}相关技术和最佳实践",
            agent_type="research",
            priority=1
        )
        self.tasks[research_task.id] = tasks.append(research_task.to_dict())

        plan_task = AgentTask(
            title=f"规划: {goal}",
            description=f"制定{goal}的详细实现计划",
            agent_type="planner",
            priority=1
        )
        self.tasks[plan_task.id] = tasks.append(plan_task.to_dict())

        code_task = AgentTask(
            title=f"编码: {goal}",
            description=f"实现{goal}的核心功能",
            agent_type="coding",
            priority=2
        )
        self.tasks[code_task.id] = tasks.append(code_task.to_dict())

        review_task = AgentTask(
            title=f"审查: {goal}",
            description=f"审查{goal}的代码质量",
            agent_type="reviewer",
            priority=2
        )
        self.tasks[review_task.id] = tasks.append(review_task.to_dict())

        return {
            "goal": goal,
            "tasks": tasks,
            "workflow": ["research", "planner", "coding", "reviewer"],
            "created_at": datetime.now().isoformat()
        }

    def execute_workflow(self, goal: str) -> Dict[str, Any]:
        workflow = self.create_workflow(goal)
        results = []

        for task_info in workflow["tasks"]:
            task_id = task_info["id"]
            task = self.tasks.get(task_id)
            if task:
                result = self.execute_task(task_id)
                results.append(result.to_dict())

                if task.agent_type != "reviewer":
                    self._send_message(
                        sender_id=task.agent_type,
                        receiver_id=self._get_next_agent(task.agent_type),
                        content=f"已完成: {task.title}\n结果: {task.result[:50]}..."
                    )

        return {
            "goal": goal,
            "status": "completed",
            "results": results,
            "summary": self._generate_workflow_summary(results)
        }

    def _get_next_agent(self, current_type: str) -> str:
        workflow_order = ["research", "planner", "coding", "reviewer"]
        idx = workflow_order.index(current_type)
        if idx < len(workflow_order) - 1:
            return workflow_order[idx + 1]
        return ""

    def _send_message(self, sender_id: str, receiver_id: str, content: str):
        message = AgentMessage(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content
        )
        self.messages.append(message)

    def _generate_workflow_summary(self, results: List[Dict[str, Any]]) -> str:
        completed_tasks = [r["title"] for r in results if r["status"] == "completed"]
        return f"工作流已完成！共完成 {len(completed_tasks)} 个任务: {', '.join(completed_tasks)}"

    def get_task(self, task_id: str) -> Optional[AgentTask]:
        return self.tasks.get(task_id)

    def list_tasks(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        all_tasks = [task.to_dict() for task in self.tasks.values()]
        if status:
            return [t for t in all_tasks if t["status"] == status]
        return all_tasks

    def get_workflow_history(self) -> List[Dict[str, Any]]:
        return [msg.to_dict() for msg in self.messages]

    def get_stats(self) -> Dict[str, Any]:
        completed_tasks = sum(1 for t in self.tasks.values() if t.status == "completed")
        in_progress_tasks = sum(1 for t in self.tasks.values() if t.status == "in_progress")
        
        return {
            "total_agents": len(self.agents),
            "active_agents": sum(1 for a in self.agents.values() if a.status == "idle"),
            "total_tasks": len(self.tasks),
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "task_completion_rate": completed_tasks / len(self.tasks) if self.tasks else 0
        }
