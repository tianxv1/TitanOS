from typing import List, Dict, Any, Optional
import json
from datetime import datetime, timedelta


class Task:
    def __init__(self, id: str, title: str, description: str = "",
                 priority: int = 3, deadline: Optional[str] = None,
                 status: str = "pending", milestone_id: Optional[str] = None):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.status = status
        self.milestone_id = milestone_id
        self.created_at = datetime.now().isoformat()
        self.completed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "deadline": self.deadline,
            "status": self.status,
            "milestone_id": self.milestone_id,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }

    def complete(self):
        self.status = "completed"
        self.completed_at = datetime.now().isoformat()


class Milestone:
    def __init__(self, id: str, title: str, description: str = "",
                 deadline: Optional[str] = None, priority: int = 2):
        self.id = id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.tasks: List[Task] = []
        self.created_at = datetime.now().isoformat()

    def add_task(self, task: Task):
        task.milestone_id = self.id
        self.tasks.append(task)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "priority": self.priority,
            "tasks": [t.to_dict() for t in self.tasks],
            "created_at": self.created_at,
            "progress": self.get_progress()
        }

    def get_progress(self) -> float:
        if not self.tasks:
            return 0.0
        completed = sum(1 for t in self.tasks if t.status == "completed")
        return round(completed / len(self.tasks), 2)


class Plan:
    def __init__(self, goal: str, description: str = ""):
        self.goal = goal
        self.description = description
        self.milestones: List[Milestone] = []
        self.created_at = datetime.now().isoformat()

    def add_milestone(self, milestone: Milestone):
        self.milestones.append(milestone)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal": self.goal,
            "description": self.description,
            "milestones": [m.to_dict() for m in self.milestones],
            "created_at": self.created_at,
            "total_progress": self.get_total_progress()
        }

    def get_total_progress(self) -> float:
        if not self.milestones:
            return 0.0
        total = sum(m.get_progress() for m in self.milestones) / len(self.milestones)
        return round(total, 2)


class Planner:
    PLANNER_PROMPT = """你是世界级规划师，将目标拆解成：
- Milestone (里程碑)
- Task (具体任务)
- Deadline (截止日期)
- Priority (优先级 1-5, 1最高)

输出JSON格式"""

    def __init__(self):
        self.plans: Dict[str, Plan] = {}
        self.current_plan_id: Optional[str] = None

    def create_plan(self, goal: str, description: str = "") -> Plan:
        import uuid
        plan_id = str(uuid.uuid4())
        plan = Plan(goal, description)
        self.plans[plan_id] = plan
        self.current_plan_id = plan_id
        return plan

    def add_milestone(self, plan_id: str, title: str, description: str = "",
                     deadline: Optional[str] = None, priority: int = 2) -> Optional[Milestone]:
        plan = self.plans.get(plan_id)
        if not plan:
            return None
        import uuid
        milestone = Milestone(str(uuid.uuid4()), title, description, deadline, priority)
        plan.add_milestone(milestone)
        return milestone

    def add_task(self, plan_id: str, milestone_id: str, title: str,
                 description: str = "", priority: int = 3,
                 deadline: Optional[str] = None) -> Optional[Task]:
        plan = self.plans.get(plan_id)
        if not plan:
            return None
        milestone = next((m for m in plan.milestones if m.id == milestone_id), None)
        if not milestone:
            return None
        import uuid
        task = Task(str(uuid.uuid4()), title, description, priority, deadline)
        milestone.add_task(task)
        return task

    def get_plan(self, plan_id: str) -> Optional[Plan]:
        return self.plans.get(plan_id)

    def get_current_plan(self) -> Optional[Plan]:
        if self.current_plan_id:
            return self.plans.get(self.current_plan_id)
        return None

    def complete_task(self, plan_id: str, task_id: str) -> bool:
        plan = self.plans.get(plan_id)
        if not plan:
            return False
        for milestone in plan.milestones:
            for task in milestone.tasks:
                if task.id == task_id:
                    task.complete()
                    return True
        return False

    def parse_goal_to_plan(self, goal: str) -> Plan:
        plan = self.create_plan(goal)

        goal_lower = goal.lower()

        if "考研" in goal_lower:
            self._plan_exam_preparation(plan)
        elif "学习" in goal_lower or "learn" in goal_lower:
            self._plan_learning(plan, goal)
        elif "工作" in goal_lower or "job" in goal_lower or "career" in goal_lower:
            self._plan_career(plan, goal)
        elif "项目" in goal_lower or "project" in goal_lower:
            self._plan_project(plan, goal)
        elif "健康" in goal_lower or "health" in goal_lower or "健身" in goal_lower:
            self._plan_health(plan)
        else:
            self._plan_default(plan, goal)

        return plan

    def _plan_exam_preparation(self, plan: Plan):
        m1 = self.add_milestone(plan.id, "确定目标学校", "收集招生信息，确定报考目标", priority=1)
        if m1:
            self.add_task(plan.id, m1.id, "查询目标院校历年分数线", priority=1)
            self.add_task(plan.id, m1.id, "了解专业课考试范围", priority=1)
            self.add_task(plan.id, m1.id, "联系学长学姐获取经验", priority=2)

        m2 = self.add_milestone(plan.id, "制定复习计划", "制定详细的复习时间表", priority=1)
        if m2:
            self.add_task(plan.id, m2.id, "分析各科基础水平", priority=1)
            self.add_task(plan.id, m2.id, "制定月/周/日计划", priority=1)
            self.add_task(plan.id, m2.id, "准备复习资料", priority=2)

        m3 = self.add_milestone(plan.id, "系统复习", "按计划执行各科复习", priority=2)
        if m3:
            self.add_task(plan.id, m3.id, "政治理论复习", priority=2)
            self.add_task(plan.id, m3.id, "英语单词和真题", priority=2)
            self.add_task(plan.id, m3.id, "专业课重点攻克", priority=1)

        m4 = self.add_milestone(plan.id, "冲刺阶段", "最后两个月冲刺", priority=2)
        if m4:
            self.add_task(plan.id, m4.id, "做真题模拟", priority=1)
            self.add_task(plan.id, m4.id, "查漏补缺", priority=1)
            self.add_task(plan.id, m4.id, "调整作息", priority=2)

    def _plan_learning(self, plan: Plan, goal: str):
        m1 = self.add_milestone(plan.id, "确定学习内容", "明确要学习的知识点", priority=1)
        if m1:
            self.add_task(plan.id, m1.id, "分解学习目标", priority=1)
            self.add_task(plan.id, m1.id, "收集学习资源", priority=2)

        m2 = self.add_milestone(plan.id, "学习阶段", "按计划学习", priority=2)
        if m2:
            self.add_task(plan.id, m2.id, "基础知识学习", priority=1)
            self.add_task(plan.id, m2.id, "实践练习", priority=2)
            self.add_task(plan.id, m2.id, "总结归纳", priority=2)

        m3 = self.add_milestone(plan.id, "巩固阶段", "巩固所学内容", priority=3)
        if m3:
            self.add_task(plan.id, m3.id, "复习重点", priority=2)
            self.add_task(plan.id, m3.id, "应用实践", priority=1)

    def _plan_career(self, plan: Plan, goal: str):
        m1 = self.add_milestone(plan.id, "职业规划", "明确职业方向", priority=1)
        if m1:
            self.add_task(plan.id, m1.id, "分析自身优势", priority=1)
            self.add_task(plan.id, m1.id, "调研目标行业", priority=2)

        m2 = self.add_milestone(plan.id, "技能提升", "提升相关技能", priority=1)
        if m2:
            self.add_task(plan.id, m2.id, "学习岗位技能", priority=1)
            self.add_task(plan.id, m2.id, "获取相关证书", priority=2)

        m3 = self.add_milestone(plan.id, "求职准备", "准备求职", priority=2)
        if m3:
            self.add_task(plan.id, m3.id, "准备简历", priority=1)
            self.add_task(plan.id, m3.id, "投递简历", priority=1)
            self.add_task(plan.id, m3.id, "面试准备", priority=1)

    def _plan_project(self, plan: Plan, goal: str):
        m1 = self.add_milestone(plan.id, "项目启动", "明确项目目标和范围", priority=1)
        if m1:
            self.add_task(plan.id, m1.id, "需求分析", priority=1)
            self.add_task(plan.id, m1.id, "技术选型", priority=2)

        m2 = self.add_milestone(plan.id, "开发阶段", "按模块开发", priority=2)
        if m2:
            self.add_task(plan.id, m2.id, "核心功能开发", priority=1)
            self.add_task(plan.id, m2.id, "功能测试", priority=2)

        m3 = self.add_milestone(plan.id, "项目收尾", "完成项目", priority=2)
        if m3:
            self.add_task(plan.id, m3.id, "集成测试", priority=1)
            self.add_task(plan.id, m3.id, "部署上线", priority=1)

    def _plan_health(self, plan: Plan):
        m1 = self.add_milestone(plan.id, "制定计划", "制定健身计划", priority=1)
        if m1:
            self.add_task(plan.id, m1.id, "设定目标", priority=1)
            self.add_task(plan.id, m1.id, "制定训练计划", priority=1)

        m2 = self.add_milestone(plan.id, "执行计划", "按计划训练", priority=2)
        if m2:
            self.add_task(plan.id, m2.id, "每日训练", priority=1)
            self.add_task(plan.id, m2.id, "记录进度", priority=2)

        m3 = self.add_milestone(plan.id, "评估调整", "评估效果并调整", priority=3)
        if m3:
            self.add_task(plan.id, m3.id, "月度评估", priority=2)
            self.add_task(plan.id, m3.id, "计划调整", priority=2)

    def _plan_default(self, plan: Plan, goal: str):
        m1 = self.add_milestone(plan.id, "目标分解", "将目标分解为具体步骤", priority=1)
        if m1:
            self.add_task(plan.id, m1.id, "明确最终目标", priority=1)
            self.add_task(plan.id, m1.id, "分解中间目标", priority=1)

        m2 = self.add_milestone(plan.id, "执行阶段", "按计划执行", priority=2)
        if m2:
            self.add_task(plan.id, m2.id, "开始行动", priority=1)
            self.add_task(plan.id, m2.id, "定期检查进度", priority=2)

        m3 = self.add_milestone(plan.id, "总结复盘", "评估和总结", priority=3)
        if m3:
            self.add_task(plan.id, m3.id, "评估结果", priority=2)
            self.add_task(plan.id, m3.id, "总结经验", priority=2)

    def get_all_plans(self) -> List[Dict[str, Any]]:
        return [plan.to_dict() for plan in self.plans.values()]

    def delete_plan(self, plan_id: str) -> bool:
        if plan_id in self.plans:
            del self.plans[plan_id]
            if self.current_plan_id == plan_id:
                self.current_plan_id = None
            return True
        return False
