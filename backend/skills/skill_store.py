from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import json
import os


@dataclass
class Skill:
    name: str
    description: str
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    usage_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "enabled": self.enabled,
            "usage_count": self.usage_count
        }

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement execute method")


class SearchSkill(Skill):
    def __init__(self):
        super().__init__(
            name="search",
            description="搜索互联网获取信息",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"}
                },
                "required": ["query"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "results": {"type": "array"},
                    "count": {"type": "integer"}
                }
            }
        )

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        self.usage_count += 1
        query = params.get("query", "")
        return {
            "skill": self.name,
            "query": query,
            "results": [
                {"title": f"关于'{query}'的搜索结果1", "url": "https://example.com/1", "snippet": "这是搜索结果的摘要内容..."},
                {"title": f"关于'{query}'的搜索结果2", "url": "https://example.com/2", "snippet": "这是另一个搜索结果的摘要内容..."},
            ],
            "count": 2,
            "status": "success"
        }


class CodingSkill(Skill):
    def __init__(self):
        super().__init__(
            name="coding",
            description="辅助编程和代码审查",
            input_schema={
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "编程任务描述"},
                    "language": {"type": "string", "description": "编程语言"}
                },
                "required": ["task"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "explanation": {"type": "string"}
                }
            }
        )

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        self.usage_count += 1
        task = params.get("task", "")
        language = params.get("language", "python")

        code_example = self._generate_code(task, language)
        return {
            "skill": self.name,
            "task": task,
            "language": language,
            "code": code_example,
            "explanation": f"这是一个{language}实现，完成了{task}",
            "status": "success"
        }

    def _generate_code(self, task: str, language: str) -> str:
        if language == "python":
            return f"# {task}\ndef solution():\n    pass\n"
        elif language == "javascript":
            return f"// {task}\nfunction solution() {{\n}}\n"
        else:
            return f"// {task}"


class MathSkill(Skill):
    def __init__(self):
        super().__init__(
            name="math",
            description="数学计算和公式推导",
            input_schema={
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式"},
                    "operation": {"type": "string", "enum": ["calculate", "simplify", "solve"]}
                },
                "required": ["expression"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "result": {"type": "string"},
                    "steps": {"type": "array"}
                }
            }
        )

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        self.usage_count += 1
        expression = params.get("expression", "")
        operation = params.get("operation", "calculate")

        result = f"计算结果: {expression}"
        return {
            "skill": self.name,
            "expression": expression,
            "operation": operation,
            "result": result,
            "steps": ["步骤1: 解析表达式", "步骤2: 执行计算", "步骤3: 返回结果"],
            "status": "success"
        }


class TranslateSkill(Skill):
    def __init__(self):
        super().__init__(
            name="translate",
            description="文本翻译",
            input_schema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "待翻译文本"},
                    "target_lang": {"type": "string", "description": "目标语言"},
                    "source_lang": {"type": "string", "description": "源语言"}
                },
                "required": ["text", "target_lang"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "translated_text": {"type": "string"},
                    "source_lang": {"type": "string"},
                    "target_lang": {"type": "string"}
                }
            }
        )

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        self.usage_count += 1
        text = params.get("text", "")
        target_lang = params.get("target_lang", "en")
        source_lang = params.get("source_lang", "auto")

        return {
            "skill": self.name,
            "original_text": text,
            "translated_text": f"[{target_lang}] {text}",
            "source_lang": source_lang,
            "target_lang": target_lang,
            "status": "success"
        }


class SkillStore:
    def __init__(self, storage_path: str = "database/skills.json"):
        self.storage_path = storage_path
        self.skills: Dict[str, Skill] = {}
        self._register_default_skills()
        self._load()

    def _register_default_skills(self):
        self.skills["search"] = SearchSkill()
        self.skills["coding"] = CodingSkill()
        self.skills["math"] = MathSkill()
        self.skills["translate"] = TranslateSkill()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for skill_data in data.get("skills", []):
                        name = skill_data.get("name")
                        if name and name in self.skills:
                            self.skills[name].usage_count = skill_data.get("usage_count", 0)
                            self.skills[name].enabled = skill_data.get("enabled", True)
            except Exception:
                pass

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "skills": [s.to_dict() for s in self.skills.values()]
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def register(self, skill: Skill) -> bool:
        if skill.name in self.skills:
            return False
        self.skills[skill.name] = skill
        self._save()
        return True

    def unregister(self, skill_name: str) -> bool:
        if skill_name in self.skills:
            del self.skills[skill_name]
            self._save()
            return True
        return False

    def get(self, skill_name: str) -> Optional[Skill]:
        return self.skills.get(skill_name)

    def list_all(self) -> List[Dict[str, Any]]:
        return [skill.to_dict() for skill in self.skills.values()]

    def list_enabled(self) -> List[Dict[str, Any]]:
        return [skill.to_dict() for skill in self.skills.values() if skill.enabled]

    def execute(self, skill_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        skill = self.skills.get(skill_name)
        if not skill:
            return {"error": f"Skill '{skill_name}' not found", "status": "error"}
        if not skill.enabled:
            return {"error": f"Skill '{skill_name}' is disabled", "status": "error"}
        try:
            return skill.execute(params)
        except Exception as e:
            return {"error": str(e), "status": "error"}

    def enable(self, skill_name: str) -> bool:
        skill = self.skills.get(skill_name)
        if skill:
            skill.enabled = True
            self._save()
            return True
        return False

    def disable(self, skill_name: str) -> bool:
        skill = self.skills.get(skill_name)
        if skill:
            skill.enabled = False
            self._save()
            return True
        return False
