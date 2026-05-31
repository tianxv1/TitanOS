from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
import uuid
import json
import os


GOAL_CATEGORIES = ["Career", "Learning", "Health", "Project"]


@dataclass
class GoalNode:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    category: str = "Project"
    parent_id: Optional[str] = None
    priority: int = 3
    status: str = "pending"
    progress: float = 0.0
    deadline: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    children: List["GoalNode"] = field(default_factory=list)

    def to_dict(self, include_children: bool = True) -> dict:
        result = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "parent_id": self.parent_id,
            "priority": self.priority,
            "status": self.status,
            "progress": self.progress,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
        if include_children:
            result["children"] = [child.to_dict(include_children=True) for child in self.children]
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "GoalNode":
        data = data.copy()
        if isinstance(data.get("deadline"), str):
            data["deadline"] = datetime.fromisoformat(data["deadline"])
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("updated_at"), str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        
        children_data = data.pop("children", [])
        node = cls(**data)
        node.children = [cls.from_dict(child) for child in children_data]
        return node

    def add_child(self, child: "GoalNode"):
        child.parent_id = self.id
        self.children.append(child)
        self._update_progress()

    def remove_child(self, child_id: str) -> bool:
        for i, child in enumerate(self.children):
            if child.id == child_id:
                del self.children[i]
                self._update_progress()
                return True
        return False

    def _update_progress(self):
        if not self.children:
            return
        total_progress = sum(child.progress for child in self.children)
        self.progress = total_progress / len(self.children)

    def update_status(self, status: str):
        self.status = status
        self.updated_at = datetime.now()
        if status == "completed":
            self.progress = 1.0
        elif status == "in_progress":
            if self.progress == 0.0:
                self.progress = 0.1


@dataclass
class GoalTree:
    root_nodes: List[GoalNode] = field(default_factory=list)
    storage_path: str = "database/goal_tree.json"

    def __post_init__(self):
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.root_nodes = [GoalNode.from_dict(node_data) for node_data in data.get("nodes", [])]
            except Exception:
                pass

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "nodes": [node.to_dict() for node in self.root_nodes],
            "saved_at": datetime.now().isoformat()
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_root_goal(self, title: str, description: str, category: str, 
                      priority: int = 3, deadline: Optional[datetime] = None) -> GoalNode:
        if category not in GOAL_CATEGORIES:
            raise ValueError(f"Invalid category. Must be one of: {GOAL_CATEGORIES}")

        node = GoalNode(
            title=title,
            description=description,
            category=category,
            priority=priority,
            deadline=deadline
        )
        self.root_nodes.append(node)
        self._save()
        return node

    def add_subgoal(self, parent_id: str, title: str, description: str, 
                    priority: int = 3, deadline: Optional[datetime] = None) -> Optional[GoalNode]:
        parent = self.find_node(parent_id)
        if not parent:
            return None

        child = GoalNode(
            title=title,
            description=description,
            category=parent.category,
            parent_id=parent_id,
            priority=priority,
            deadline=deadline
        )
        parent.add_child(child)
        self._save()
        return child

    def find_node(self, node_id: str) -> Optional[GoalNode]:
        for root in self.root_nodes:
            found = self._find_node_recursive(root, node_id)
            if found:
                return found
        return None

    def _find_node_recursive(self, node: GoalNode, node_id: str) -> Optional[GoalNode]:
        if node.id == node_id:
            return node
        for child in node.children:
            found = self._find_node_recursive(child, node_id)
            if found:
                return found
        return None

    def update_goal(self, node_id: str, **kwargs) -> bool:
        node = self.find_node(node_id)
        if not node:
            return False

        if "title" in kwargs:
            node.title = kwargs["title"]
        if "description" in kwargs:
            node.description = kwargs["description"]
        if "priority" in kwargs:
            node.priority = kwargs["priority"]
        if "status" in kwargs:
            node.update_status(kwargs["status"])
        if "progress" in kwargs:
            node.progress = min(max(0.0, kwargs["progress"]), 1.0)
        if "deadline" in kwargs:
            node.deadline = kwargs["deadline"]

        node.updated_at = datetime.now()
        self._propagate_progress(node)
        self._save()
        return True

    def _propagate_progress(self, node: GoalNode):
        if node.parent_id:
            parent = self.find_node(node.parent_id)
            if parent:
                parent._update_progress()
                self._propagate_progress(parent)

    def delete_goal(self, node_id: str) -> bool:
        for i, root in enumerate(self.root_nodes):
            if root.id == node_id:
                del self.root_nodes[i]
                self._save()
                return True
            
            if root.remove_child(node_id):
                self._save()
                return True
            
            if self._delete_from_children(root, node_id):
                self._save()
                return True
        return False

    def _delete_from_children(self, node: GoalNode, node_id: str) -> bool:
        for child in node.children:
            if child.remove_child(node_id):
                return True
            if self._delete_from_children(child, node_id):
                return True
        return False

    def get_tree_by_category(self, category: str) -> List[GoalNode]:
        return [root for root in self.root_nodes if root.category == category]

    def get_all_goals(self) -> List[Dict[str, Any]]:
        result = []
        for root in self.root_nodes:
            result.append(self._flatten_node(root))
        return result

    def _flatten_node(self, node: GoalNode, level: int = 0) -> Dict[str, Any]:
        data = node.to_dict(include_children=False)
        data["level"] = level
        data["children"] = [self._flatten_node(child, level + 1) for child in node.children]
        return data

    def get_tree_summary(self) -> Dict[str, Any]:
        stats = {cat: {"total": 0, "completed": 0, "in_progress": 0, "pending": 0} for cat in GOAL_CATEGORIES}
        
        for root in self.root_nodes:
            self._count_by_category(root, stats)

        return {
            "categories": stats,
            "total_goals": sum(stats[cat]["total"] for cat in GOAL_CATEGORIES),
            "completed_goals": sum(stats[cat]["completed"] for cat in GOAL_CATEGORIES),
            "overall_progress": self._calculate_overall_progress()
        }

    def _count_by_category(self, node: GoalNode, stats: Dict[str, Dict[str, int]]):
        stats[node.category]["total"] += 1
        if node.status == "completed":
            stats[node.category]["completed"] += 1
        elif node.status == "in_progress":
            stats[node.category]["in_progress"] += 1
        else:
            stats[node.category]["pending"] += 1
        
        for child in node.children:
            self._count_by_category(child, stats)

    def _calculate_overall_progress(self) -> float:
        all_nodes = []
        for root in self.root_nodes:
            all_nodes.extend(self._collect_all_nodes(root))
        
        if not all_nodes:
            return 0.0
        
        total_progress = sum(node.progress for node in all_nodes)
        return total_progress / len(all_nodes)

    def _collect_all_nodes(self, node: GoalNode) -> List[GoalNode]:
        nodes = [node]
        for child in node.children:
            nodes.extend(self._collect_all_nodes(child))
        return nodes

    def get_priority_goals(self, limit: int = 5) -> List[Dict[str, Any]]:
        all_nodes = []
        for root in self.root_nodes:
            all_nodes.extend(self._collect_all_nodes(root))
        
        sorted_nodes = sorted(all_nodes, key=lambda n: (-n.priority, n.progress))
        return [node.to_dict(include_children=False) for node in sorted_nodes[:limit]]

    def get_overdue_goals(self) -> List[Dict[str, Any]]:
        now = datetime.now()
        overdue = []
        
        for root in self.root_nodes:
            overdue.extend(self._find_overdue(root, now))
        
        return overdue

    def _find_overdue(self, node: GoalNode, now: datetime) -> List[Dict[str, Any]]:
        result = []
        if node.deadline and node.deadline < now and node.status != "completed":
            data = node.to_dict(include_children=False)
            data["days_overdue"] = (now - node.deadline).days
            result.append(data)
        
        for child in node.children:
            result.extend(self._find_overdue(child, now))
        
        return result
