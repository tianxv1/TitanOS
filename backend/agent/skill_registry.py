from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass
import json
import os
import glob
import shutil
import csv
import re
from datetime import datetime


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

        self.register(Skill(
            name="list_files",
            description="List files in a directory",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path"},
                    "pattern": {"type": "string", "description": "Glob pattern filter"}
                },
                "required": ["path"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "files": {"type": "array"},
                    "directories": {"type": "array"},
                    "count": {"type": "integer"}
                }
            },
            handler=self._list_files_handler
        ))

        self.register(Skill(
            name="copy_file",
            description="Copy a file from source to destination",
            input_schema={
                "type": "object",
                "properties": {
                    "source": {"type": "string", "description": "Source file path"},
                    "destination": {"type": "string", "description": "Destination file path"}
                },
                "required": ["source", "destination"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "source": {"type": "string"},
                    "destination": {"type": "string"}
                }
            },
            handler=self._copy_file_handler
        ))

        self.register(Skill(
            name="delete_file",
            description="Delete a file",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to delete"}
                },
                "required": ["path"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "path": {"type": "string"}
                }
            },
            handler=self._delete_file_handler
        ))

        self.register(Skill(
            name="rename_file",
            description="Rename or move a file",
            input_schema={
                "type": "object",
                "properties": {
                    "old_path": {"type": "string", "description": "Current file path"},
                    "new_path": {"type": "string", "description": "New file path"}
                },
                "required": ["old_path", "new_path"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "old_path": {"type": "string"},
                    "new_path": {"type": "string"}
                }
            },
            handler=self._rename_file_handler
        ))

        self.register(Skill(
            name="create_directory",
            description="Create a directory",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path to create"}
                },
                "required": ["path"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "path": {"type": "string"}
                }
            },
            handler=self._create_directory_handler
        ))

        self.register(Skill(
            name="read_json",
            description="Read and parse JSON file",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "JSON file path"}
                },
                "required": ["path"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "data": {"type": "object"},
                    "success": {"type": "boolean"}
                }
            },
            handler=self._read_json_handler
        ))

        self.register(Skill(
            name="write_json",
            description="Write data to JSON file",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "JSON file path"},
                    "data": {"type": "object", "description": "Data to write"},
                    "pretty": {"type": "boolean", "default": True, "description": "Pretty print"}
                },
                "required": ["path", "data"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "path": {"type": "string"}
                }
            },
            handler=self._write_json_handler
        ))

        self.register(Skill(
            name="read_csv",
            description="Read CSV file",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "CSV file path"},
                    "delimiter": {"type": "string", "default": ",", "description": "Delimiter character"}
                },
                "required": ["path"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "rows": {"type": "array"},
                    "headers": {"type": "array"},
                    "success": {"type": "boolean"}
                }
            },
            handler=self._read_csv_handler
        ))

        self.register(Skill(
            name="write_csv",
            description="Write data to CSV file",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "CSV file path"},
                    "rows": {"type": "array", "description": "Data rows"},
                    "headers": {"type": "array", "description": "Column headers"}
                },
                "required": ["path", "rows"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "path": {"type": "string"},
                    "row_count": {"type": "integer"}
                }
            },
            handler=self._write_csv_handler
        ))

        self.register(Skill(
            name="system_info",
            description="Get system information",
            input_schema={
                "type": "object",
                "properties": {}
            },
            output_schema={
                "type": "object",
                "properties": {
                    "current_time": {"type": "string"},
                    "working_directory": {"type": "string"},
                    "platform": {"type": "string"}
                }
            },
            handler=self._system_info_handler
        ))

        self.register(Skill(
            name="text_replace",
            description="Replace text in a file",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "old_text": {"type": "string", "description": "Text to replace"},
                    "new_text": {"type": "string", "description": "New text"}
                },
                "required": ["path", "old_text", "new_text"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "replaced_count": {"type": "integer"}
                }
            },
            handler=self._text_replace_handler
        ))

        self.register(Skill(
            name="extract_text",
            description="Extract text using regex pattern",
            input_schema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Input text"},
                    "pattern": {"type": "string", "description": "Regex pattern"}
                },
                "required": ["text", "pattern"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "matches": {"type": "array"},
                    "match_count": {"type": "integer"}
                }
            },
            handler=self._extract_text_handler
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

    def _list_files_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", ".")
        pattern = params.get("pattern", "*")
        
        try:
            full_pattern = os.path.join(path, pattern)
            all_entries = glob.glob(full_pattern)
            
            files = []
            directories = []
            
            for entry in all_entries:
                if os.path.isfile(entry):
                    files.append({
                        "name": os.path.basename(entry),
                        "path": entry,
                        "size": os.path.getsize(entry),
                        "modified": datetime.fromtimestamp(os.path.getmtime(entry)).isoformat()
                    })
                elif os.path.isdir(entry):
                    directories.append({
                        "name": os.path.basename(entry),
                        "path": entry,
                        "modified": datetime.fromtimestamp(os.path.getmtime(entry)).isoformat()
                    })
            
            return {
                "files": files,
                "directories": directories,
                "count": len(files) + len(directories),
                "path": path
            }
        except Exception as e:
            return {"error": str(e), "files": [], "directories": [], "count": 0}

    def _copy_file_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        source = params.get("source", "")
        destination = params.get("destination", "")
        
        try:
            if not os.path.exists(source):
                return {"success": False, "error": "Source file not found"}
            
            os.makedirs(os.path.dirname(destination) if os.path.dirname(destination) else ".", exist_ok=True)
            shutil.copy2(source, destination)
            
            return {"success": True, "source": source, "destination": destination}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _delete_file_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", "")
        
        try:
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                return {"success": True, "path": path}
            return {"success": False, "error": "Path not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _rename_file_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        old_path = params.get("old_path", "")
        new_path = params.get("new_path", "")
        
        try:
            if not os.path.exists(old_path):
                return {"success": False, "error": "Source path not found"}
            
            os.makedirs(os.path.dirname(new_path) if os.path.dirname(new_path) else ".", exist_ok=True)
            os.rename(old_path, new_path)
            
            return {"success": True, "old_path": old_path, "new_path": new_path}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _create_directory_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", "")
        
        try:
            os.makedirs(path, exist_ok=True)
            return {"success": True, "path": path}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _read_json_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", "")
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {"data": data, "success": True}
        except Exception as e:
            return {"data": {}, "success": False, "error": str(e)}

    def _write_json_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", "")
        data = params.get("data", {})
        pretty = params.get("pretty", True)
        
        try:
            os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                if pretty:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                else:
                    json.dump(data, f, ensure_ascii=False)
            return {"success": True, "path": path}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _read_csv_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", "")
        delimiter = params.get("delimiter", ",")
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=delimiter)
                rows = list(reader)
            
            headers = rows[0] if rows else []
            data_rows = rows[1:] if len(rows) > 1 else []
            
            return {"rows": data_rows, "headers": headers, "success": True}
        except Exception as e:
            return {"rows": [], "headers": [], "success": False, "error": str(e)}

    def _write_csv_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", "")
        rows = params.get("rows", [])
        headers = params.get("headers", [])
        
        try:
            os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
            
            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                if headers:
                    writer.writerow(headers)
                writer.writerows(rows)
            
            return {"success": True, "path": path, "row_count": len(rows)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _system_info_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "current_time": datetime.now().isoformat(),
            "working_directory": os.getcwd(),
            "platform": os.name
        }

    def _text_replace_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        path = params.get("path", "")
        old_text = params.get("old_text", "")
        new_text = params.get("new_text", "")
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            replaced_count = content.count(old_text)
            new_content = content.replace(old_text, new_text)
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            return {"success": True, "replaced_count": replaced_count}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _extract_text_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        text = params.get("text", "")
        pattern = params.get("pattern", "")
        
        try:
            matches = re.findall(pattern, text)
            return {"matches": matches, "match_count": len(matches)}
        except Exception as e:
            return {"matches": [], "match_count": 0, "error": str(e)}

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
