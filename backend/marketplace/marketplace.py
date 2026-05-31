from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid
import json
import os


@dataclass
class AgentPackage:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    agent_type: str = ""
    author: str = ""
    version: str = "1.0.0"
    tags: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    rating: float = 0.0
    download_count: int = 0
    is_installed: bool = False
    is_featured: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "agent_type": self.agent_type,
            "author": self.author,
            "version": self.version,
            "tags": self.tags,
            "skills": self.skills,
            "dependencies": self.dependencies,
            "rating": self.rating,
            "download_count": self.download_count,
            "is_installed": self.is_installed,
            "is_featured": self.is_featured,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AgentPackage":
        data = data.copy()
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if isinstance(data.get("last_updated"), str):
            data["last_updated"] = datetime.fromisoformat(data["last_updated"])
        return cls(**data)


class AgentMarketplace:
    def __init__(self):
        self.packages: Dict[str, AgentPackage] = {}
        self.installed_packages: Dict[str, AgentPackage] = {}
        self._load_packages()
        self._initialize_default_packages()

    def _load_packages(self):
        if os.path.exists("database/marketplace.json"):
            try:
                with open("database/marketplace.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for pkg_data in data.get("packages", []):
                        pkg = AgentPackage.from_dict(pkg_data)
                        self.packages[pkg.id] = pkg
                        if pkg.is_installed:
                            self.installed_packages[pkg.id] = pkg
            except Exception:
                pass

    def _save_packages(self):
        os.makedirs("database", exist_ok=True)
        data = {
            "packages": [pkg.to_dict() for pkg in self.packages.values()],
            "saved_at": datetime.now().isoformat()
        }
        with open("database/marketplace.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _initialize_default_packages(self):
        default_packages = [
            {
                "name": "SearchAgent",
                "description": "强大的网络搜索代理，能够快速查找各种信息",
                "agent_type": "search",
                "author": "TitanOS Team",
                "version": "1.0.0",
                "tags": ["search", "information", "web"],
                "skills": ["web_search", "query_expansion", "result_filtering"],
                "dependencies": [],
                "rating": 4.8,
                "download_count": 12500,
                "is_installed": True,
                "is_featured": True
            },
            {
                "name": "ResearchAgent",
                "description": "深度研究代理，能够进行系统性的信息收集和分析",
                "agent_type": "research",
                "author": "TitanOS Team",
                "version": "1.0.0",
                "tags": ["research", "analysis", "knowledge"],
                "skills": ["deep_research", "source_evaluation", "content_synthesis"],
                "dependencies": ["SearchAgent"],
                "rating": 4.9,
                "download_count": 8900,
                "is_installed": True,
                "is_featured": True
            },
            {
                "name": "CrawlerAgent",
                "description": "网页爬虫代理，能够提取网页内容",
                "agent_type": "search",
                "author": "TitanOS Team",
                "version": "1.0.0",
                "tags": ["crawler", "web", "scraping"],
                "skills": ["web_crawling", "content_extraction", "html_parsing"],
                "dependencies": [],
                "rating": 4.5,
                "download_count": 6700,
                "is_installed": False,
                "is_featured": False
            },
            {
                "name": "CodingAgent",
                "description": "代码编写代理，支持多种编程语言",
                "agent_type": "coding",
                "author": "TitanOS Team",
                "version": "1.0.0",
                "tags": ["coding", "development", "automation"],
                "skills": ["python", "javascript", "typescript", "code_generation"],
                "dependencies": [],
                "rating": 4.7,
                "download_count": 15200,
                "is_installed": True,
                "is_featured": True
            },
            {
                "name": "ReviewerAgent",
                "description": "代码审查代理，确保代码质量",
                "agent_type": "reviewer",
                "author": "TitanOS Team",
                "version": "1.0.0",
                "tags": ["review", "quality", "code"],
                "skills": ["code_review", "bug_detection", "optimization"],
                "dependencies": ["CodingAgent"],
                "rating": 4.6,
                "download_count": 7800,
                "is_installed": True,
                "is_featured": False
            },
            {
                "name": "PlannerAgent",
                "description": "智能规划代理，帮助制定任务计划",
                "agent_type": "planner",
                "author": "TitanOS Team",
                "version": "1.0.0",
                "tags": ["planning", "task", "organization"],
                "skills": ["task_decomposition", "schedule_optimization", "resource_allocation"],
                "dependencies": [],
                "rating": 4.8,
                "download_count": 11000,
                "is_installed": True,
                "is_featured": True
            },
            {
                "name": "AnalyzerAgent",
                "description": "数据分析代理，提供深入的洞察",
                "agent_type": "analyzer",
                "author": "TitanOS Team",
                "version": "1.0.0",
                "tags": ["analysis", "data", "insights"],
                "skills": ["data_analysis", "visualization", "report_generation"],
                "dependencies": [],
                "rating": 4.5,
                "download_count": 5400,
                "is_installed": False,
                "is_featured": False
            },
            {
                "name": "SummarizerAgent",
                "description": "内容总结代理，提炼核心信息",
                "agent_type": "summarizer",
                "author": "TitanOS Team",
                "version": "1.0.0",
                "tags": ["summary", "content", "writing"],
                "skills": ["text_summarization", "key_point_extraction", "content_reduction"],
                "dependencies": [],
                "rating": 4.4,
                "download_count": 4300,
                "is_installed": False,
                "is_featured": False
            },
            {
                "name": "WriterAgent",
                "description": "写作助手代理，辅助内容创作",
                "agent_type": "summarizer",
                "author": "TitanOS Community",
                "version": "1.0.0",
                "tags": ["writing", "content", "creative"],
                "skills": ["content_writing", "editing", "creative_writing"],
                "dependencies": ["SummarizerAgent"],
                "rating": 4.3,
                "download_count": 3200,
                "is_installed": False,
                "is_featured": False
            },
            {
                "name": "DebuggerAgent",
                "description": "代码调试代理，帮助定位和修复bug",
                "agent_type": "coding",
                "author": "TitanOS Community",
                "version": "1.0.0",
                "tags": ["debugging", "code", "troubleshooting"],
                "skills": ["bug_detection", "error_analysis", "fix_suggestion"],
                "dependencies": ["CodingAgent"],
                "rating": 4.2,
                "download_count": 2800,
                "is_installed": False,
                "is_featured": False
            },
            {
                "name": "TranslatorAgent",
                "description": "多语言翻译代理",
                "agent_type": "summarizer",
                "author": "TitanOS Community",
                "version": "1.0.0",
                "tags": ["translation", "language", "localization"],
                "skills": ["text_translation", "language_detection", "localization"],
                "dependencies": [],
                "rating": 4.6,
                "download_count": 9100,
                "is_installed": False,
                "is_featured": False
            },
            {
                "name": "FinanceAgent",
                "description": "财务分析代理",
                "agent_type": "analyzer",
                "author": "TitanOS Community",
                "version": "1.0.0",
                "tags": ["finance", "analysis", "investment"],
                "skills": ["financial_analysis", "investment_research", "reporting"],
                "dependencies": ["ResearchAgent", "AnalyzerAgent"],
                "rating": 4.7,
                "download_count": 6200,
                "is_installed": False,
                "is_featured": False
            }
        ]

        for pkg_data in default_packages:
            if pkg_data["name"] not in [p.name for p in self.packages.values()]:
                pkg = AgentPackage(**pkg_data)
                self.packages[pkg.id] = pkg
                if pkg.is_installed:
                    self.installed_packages[pkg.id] = pkg

        self._save_packages()

    def list_packages(self, agent_type: Optional[str] = None, search_query: Optional[str] = None,
                      featured_only: bool = False, installed_only: bool = False) -> List[Dict[str, Any]]:
        packages = list(self.packages.values())

        if installed_only:
            packages = [p for p in packages if p.is_installed]
        if featured_only:
            packages = [p for p in packages if p.is_featured]
        if agent_type:
            packages = [p for p in packages if p.agent_type == agent_type]
        if search_query:
            query_lower = search_query.lower()
            packages = [p for p in packages if (query_lower in p.name.lower() or
                                               query_lower in p.description.lower() or
                                               any(query_lower in tag.lower() for tag in p.tags))]

        return sorted([p.to_dict() for p in packages], key=lambda x: (-x["is_featured"], -x["download_count"]))

    def get_package(self, package_id: str) -> Optional[AgentPackage]:
        return self.packages.get(package_id)

    def install_package(self, package_id: str) -> bool:
        package = self.packages.get(package_id)
        if not package:
            return False

        for dep_id in package.dependencies:
            dep_pkg = next((p for p in self.packages.values() if p.name == dep_id), None)
            if dep_pkg and not dep_pkg.is_installed:
                self.install_package(dep_pkg.id)

        package.is_installed = True
        package.download_count += 1
        self.installed_packages[package.id] = package
        self._save_packages()
        return True

    def uninstall_package(self, package_id: str) -> bool:
        package = self.packages.get(package_id)
        if not package or not package.is_installed:
            return False

        package.is_installed = False
        if package_id in self.installed_packages:
            del self.installed_packages[package_id]
        self._save_packages()
        return True

    def get_installed_packages(self) -> List[Dict[str, Any]]:
        return [pkg.to_dict() for pkg in self.installed_packages.values()]

    def get_featured_packages(self) -> List[Dict[str, Any]]:
        featured = [p for p in self.packages.values() if p.is_featured]
        return sorted([p.to_dict() for p in featured], key=lambda x: -x["download_count"])

    def search_packages(self, query: str) -> List[Dict[str, Any]]:
        return self.list_packages(search_query=query)

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_packages": len(self.packages),
            "installed_packages": len(self.installed_packages),
            "featured_packages": sum(1 for p in self.packages.values() if p.is_featured),
            "total_downloads": sum(p.download_count for p in self.packages.values()),
            "avg_rating": round(sum(p.rating for p in self.packages.values()) / len(self.packages), 2) if self.packages else 0.0
        }

    def get_categories(self) -> List[Dict[str, Any]]:
        categories = ["search", "research", "coding", "reviewer", "planner", "analyzer", "summarizer"]
        return [{"name": cat, "count": sum(1 for p in self.packages.values() if p.agent_type == cat)} for cat in categories]
