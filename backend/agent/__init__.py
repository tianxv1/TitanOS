"""
Agent System - 预测、帮助、替你执行

TitanOS v4.0 的核心 Agent 系统，提供：
- 任务管理和执行
- 工作流编排
- 技能注册和调用
- 智能预测和建议
- 自动执行能力
"""

from .task import Task, Workflow, TaskStatus, TaskPriority
from .skill_registry import Skill, SkillRegistry
from .runtime import Runtime
from .agent import Agent

__all__ = [
    # 任务和工作流
    'Task',
    'Workflow',
    'TaskStatus',
    'TaskPriority',
    
    # 技能系统
    'Skill',
    'SkillRegistry',
    
    # 运行时
    'Runtime',
    
    # 智能 Agent
    'Agent'
]

__version__ = "4.0.0"
__author__ = "TitanOS Team"