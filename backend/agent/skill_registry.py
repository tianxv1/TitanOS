from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass
import json
import os


@dataclass
class Skill:
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    handler: Callable
    enabled: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "enabled": self.enabled
        }


class SkillRegistry:
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        self._load_builtin_skills()

    def _load_builtin_skills(self):
        self.register(Skill(
            name="search",
            description="Search the web for information",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "results": {"type": "array"},
                    "count": {"type": "integer"}
                }
            },
            handler=self._search_handler
        ))

        self.register(Skill(
            name="read_file",
            description="Read content from a file",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to read"}
                },
                "required": ["path"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "success": {"type": "boolean"}
                }
            },
            handler=self._read_file_handler
        ))

        self.register(Skill(
            name="write_file",
            description="Write content to a file",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to write"},
                    "content": {"type": "string", "description": "Content to write"}
                },
                "required": ["path", "content"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "path": {"type": "string"}
                }
            },
            handler=self._write_file_handler
        ))

        self.register(Skill(
            name="summarize",
            description="Summarize text content",
            input_schema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to summarize"},
                    "max_length": {"type": "integer", "default": 100}
                },
                "required": ["text"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "summary": {"type": "string"},
                    "key_points": {"type": "array"}
                }
            },
            handler=self._summarize_handler
        ))

        self.register(Skill(
            name="analyze",
            description="Analyze code or text",
            input_schema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "type": {"type": "string", "enum": ["code", "text", "data"]}
                },
                "required": ["content"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "analysis": {"type": "string"},
                    "issues": {"type": "array"}
                }
            },
            handler=self._analyze_handler
        ))

    def _search_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        query = params.get("query", "")
        return {
            "results": [
                {"title": f"Result for '{query}' 1", "url": "https://example.com/1", "snippet": "Sample result..."},
                {"title": f"Result for '{query}' 2", "url": "https://example.com/2", "snippet": "Sample result..."}
            ],
            "count": 2,
            "query": query
        }

    def _read_file_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", "")
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                return {"content": content, "success": True}
            return {"content": "", "success": False, "error": "File not found"}
        except Exception as e:
            return {"content": "", "success": False, "error": str(e)}

    def _write_file_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", "")
        content = params.get("content", "")
        try:
            os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"success": True, "path": path}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _summarize_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        text = params.get("text", "")
        max_length = params.get("max_length", 100)

        sentences = text.split("。")
        summary = "。".join(sentences[:2]) + "。"

        if len(summary) > max_length:
            summary = summary[:max_length] + "..."

        return {
            "summary": summary,
            "key_points": [
                "First key point extracted from text",
                "Second key point extracted from text"
            ],
            "original_length": len(text),
            "summary_length": len(summary)
        }

    def _analyze_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        content = params.get("content", "")
        content_type = params.get("type", "text")

        if content_type == "code":
            lines = content.split("\n")
            return {
                "analysis": f"Analyzed {len(lines)} lines of code",
                "issues": ["Potential improvement: Add comments", "Consider refactoring"],
                "metrics": {
                    "lines": len(lines),
                    "has_functions": "def " in content or "function " in content,
                    "has_classes": "class " in content
                }
            }

        return {
            "analysis": f"Analyzed {len(content)} characters of text",
            "issues": [],
            "word_count": len(content.split())
        }

    def register(self, skill: Skill) -> bool:
        if skill.name in self.skills:
            return False
        self.skills[skill.name] = skill
        return True

    def unregister(self, skill_name: str) -> bool:
        if skill_name in self.skills:
            del self.skills[skill_name]
            return True
        return False

    def get(self, skill_name: str) -> Optional[Skill]:
        return self.skills.get(skill_name)

    def list_all(self) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in self.skills.values()]

    def list_enabled(self) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in self.skills.values() if s.enabled]

    def execute(self, skill_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        skill = self.skills.get(skill_name)
        if not skill:
            return {"error": f"Skill '{skill_name}' not found", "status": "error"}
        if not skill.enabled:
            return {"error": f"Skill '{skill_name}' is disabled", "status": "error"}

        try:
            result = skill.handler(params)
            result["status"] = "success"
            result["skill_used"] = skill_name
            return result
        except Exception as e:
            return {"error": str(e), "status": "error", "skill_used": skill_name}
