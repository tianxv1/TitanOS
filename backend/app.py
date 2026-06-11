from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory.memory_engine import MemoryEngine
from memory.memory_node import Memory
from brain.reasoning import ReasoningEngine
from planner.planner import Planner, Plan, Milestone, Task
from skills.skill_store import SkillStore
from knowledge_graph.knowledge_graph import KnowledgeGraph, RELATION_TYPES
from knowledge_graph.entities import Entity, Relation
from learning.learning_engine import LearningEngine, Experience, LearnedPattern
from digital_twin.digital_twin import DigitalTwin
from digital_twin.profile import DigitalTwinProfile, WritingStyle, CodeStyle

from rag.rag_engine import RAGEngine
from rag.document import Chunk, Document
from agent.runtime import Runtime, Task as AgentTask, Workflow
from agent.task import TaskStatus, TaskPriority
from reflection.reflection_engine import ReflectionEngine
from reflection.models import Reflection, Improvement
from knowledge_base.knowledge_base import KnowledgeBase, DocumentProcessor

from auth.auth_service import AuthService
from auth.user_store import User

from timeline.timeline import MemoryTimeline
from dashboard.dashboard import GrowthDashboard
from goal_tree.goal_tree import GoalTree, GoalNode
from multi_agent.coordinator import AgentCoordinator, Agent, AgentTask
from memory.cognitive.memory_system import CognitiveMemorySystem, EpisodicMemory, SemanticMemory, ProceduralMemory
from marketplace.marketplace import AgentMarketplace, AgentPackage

from chat.chat_engine import ChatEngine
from rag.embedding import EmbeddingService
from vector_db.manager import VectorDBManager, vector_db_manager


app = FastAPI(title="TitanOS API", version="1.0.0", description="Personal AI Operating System v1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend (legacy static HTML)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Serve Next.js production build (v2.0 React frontend)
next_static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", ".next", "static")
if os.path.exists(next_static_dir):
    app.mount("/_next/static", StaticFiles(directory=next_static_dir), name="next-static")

# Serve Next.js public assets
next_public_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "public")
if os.path.exists(next_public_dir):
    app.mount("/public", StaticFiles(directory=next_public_dir), name="next-public")


# Vector DB and Embedding Service (v1.5)
embedding_service = EmbeddingService(model='simulated', dimension=384)
vector_db_manager = VectorDBManager()
vector_db_manager.initialize(provider_type='in_memory', embed_service=embedding_service)

# Update memory_engine to use vector_db
memory_engine = MemoryEngine(
    storage_path='database/memories.json',
    embedding_service=embedding_service,
    vector_db_manager=vector_db_manager
)

reasoning_engine = ReasoningEngine()
planner = Planner()
skill_store = SkillStore()
knowledge_graph = KnowledgeGraph()
learning_engine = LearningEngine()
digital_twin = DigitalTwin()

rag_engine = RAGEngine()
agent_runtime = Runtime()
reflection_engine = ReflectionEngine()
knowledge_base = KnowledgeBase()

auth_service = AuthService()
timeline = MemoryTimeline()
dashboard = GrowthDashboard()
goal_tree = GoalTree()
multi_agent = AgentCoordinator()
cognitive_memory = CognitiveMemorySystem()
marketplace = AgentMarketplace()
chat_engine = ChatEngine()


class MemoryCreate(BaseModel):
    content: str
    importance: float = 0.5
    tags: Optional[List[str]] = None
    embedding: Optional[List[float]] = None


class MemoryUpdate(BaseModel):
    importance: Optional[float] = None
    tags: Optional[List[str]] = None


class ExperienceCreate(BaseModel):
    task: str
    result: str
    time_taken: str
    lesson: str


class ReasoningRequest(BaseModel):
    context: str
    question: str


class PlanCreate(BaseModel):
    goal: str
    description: Optional[str] = None


class TaskComplete(BaseModel):
    plan_id: str
    task_id: str


class SkillExecute(BaseModel):
    skill_name: str
    params: Dict[str, Any]


class EntityCreate(BaseModel):
    name: str
    entity_type: str = "concept"
    description: str = ""
    properties: Optional[Dict[str, Any]] = None
    memory_id: Optional[str] = None


class RelationCreate(BaseModel):
    from_entity_id: str
    to_entity_id: str
    relation_type: str
    weight: float = 1.0
    properties: Optional[Dict[str, Any]] = None


class LearningExperienceCreate(BaseModel):
    task: str
    result: str
    time_taken: str
    lesson: str
    category: str = "general"
    tags: Optional[List[str]] = None
    success: bool = True
    difficulty: int = 3


class TwinUpdate(BaseModel):
    writing_formal_level: Optional[float] = None
    writing_tone: Optional[str] = None
    code_naming_convention: Optional[str] = None
    interests: Optional[List[str]] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None


class RAGQuery(BaseModel):
    question: str
    top_k: int = 5
    use_rerank: bool = True
    use_hybrid: bool = True
    include_citations: bool = True


class RAGAddText(BaseModel):
    text: str
    source: str = "user_input"
    metadata: Optional[Dict[str, Any]] = None
    chunk_size: int = 500
    overlap: int = 50


class RAGAddDocument(BaseModel):
    title: str
    content: str
    source_type: str = "markdown"
    metadata: Optional[Dict[str, Any]] = None


class AgentTaskCreate(BaseModel):
    name: str
    task_type: str = "general"
    input_data: Optional[Dict[str, Any]] = None
    priority: int = 2
    dependencies: Optional[List[str]] = None


class AgentWorkflowCreate(BaseModel):
    name: str
    description: str = ""


class ReflectionCreate(BaseModel):
    task_id: str
    task_name: str
    what_happened: str
    what_went_well: Optional[List[str]] = None
    what_could_improve: Optional[List[str]] = None
    mistakes: Optional[List[str]] = None
    lessons_learned: Optional[List[str]] = None
    confidence_level: int = 3


class ImprovementApply(BaseModel):
    improvement_id: str
    actual_outcome: str
    success: bool


class KBAddMarkdown(BaseModel):
    content: str
    title: str = ""
    metadata: Optional[Dict[str, Any]] = None


class KBAddText(BaseModel):
    content: str
    title: str = ""
    metadata: Optional[Dict[str, Any]] = None


class KBAddWeb(BaseModel):
    url: str
    content: str
    title: str = ""


class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = ""


class UserLogin(BaseModel):
    email: str
    password: str


class UserLoginByUsername(BaseModel):
    username: str
    password: str


class TokenRefresh(BaseModel):
    token: str


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class ProfileUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None


class UserDelete(BaseModel):
    password: str


class GoalCreate(BaseModel):
    title: str
    description: str = ""
    category: str = "Project"
    priority: int = 3
    deadline: Optional[str] = None


class GoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[str] = None
    progress: Optional[float] = None
    deadline: Optional[str] = None


class SubgoalCreate(BaseModel):
    parent_id: str
    title: str
    description: str = ""
    priority: int = 3
    deadline: Optional[str] = None


class AgentCreate(BaseModel):
    name: str
    agent_type: str
    description: str = ""
    skills: Optional[List[str]] = None


class AgentTaskAssign(BaseModel):
    agent_id: str
    title: str
    description: str


class WorkflowCreate(BaseModel):
    goal: str


class EpisodicMemoryCreate(BaseModel):
    time: Optional[str] = None
    location: str = ""
    people: Optional[List[str]] = None
    event: str
    emotion: str = ""
    content: str = ""
    importance: float = 0.5
    tags: Optional[List[str]] = None


class SemanticMemoryCreate(BaseModel):
    concept: str
    definition: str
    relations: Optional[List[Dict[str, str]]] = None
    examples: Optional[List[str]] = None
    source: str = ""
    confidence: float = 0.8


class ProceduralMemoryCreate(BaseModel):
    skill: str
    steps: List[str]
    prerequisites: Optional[List[str]] = None
    difficulty: str = "medium"
    tags: Optional[List[str]] = None


class SkillPractice(BaseModel):
    memory_id: str
    practice_quality: float = 0.8


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    store_to_memory: bool = True
    importance: float = 0.6


@app.get("/")
async def root():
    next_index_path = os.path.join(os.path.dirname(__file__), "..", "frontend", ".next", "standalone", "index.html")
    if os.path.exists(next_index_path):
        return FileResponse(next_index_path)
    static_index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(static_index_path):
        return FileResponse(static_index_path)
    return {
        "name": "TitanOS",
        "version": "2.0.0",
        "description": "Personal AI Operating System v2.0 - Knowledge Graph + Neo4j + LLM + React Frontend"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "modules": {
            "memory": "active",
            "brain": "active",
            "planner": "active",
            "skills": "active",
            "knowledge_graph": "active",
            "learning": "active",
            "digital_twin": "active",
            "rag": "active",
            "agent": "active",
            "reflection": "active",
            "knowledge_base": "active",
            "auth": "active",
            "timeline": "active",
            "dashboard": "active",
            "goal_tree": "active",
            "multi_agent": "active",
            "cognitive_memory": "active",
            "marketplace": "active"
        }
    }


@app.post("/memory")
async def add_memory(data: MemoryCreate):
    memory = memory_engine.add(
        content=data.content,
        importance=data.importance,
        tags=data.tags,
        embedding=data.embedding
    )
    return {"memory": memory.to_dict(), "status": "created"}


@app.get("/memory")
async def list_memories(limit: int = 20):
    memories = memory_engine.get_recent(limit)
    return {"memories": [m.to_dict() for m in memories]}


@app.get("/memory/search/{query}")
async def search_memories(query: str, limit: int = 10):
    memories = memory_engine.search(query, limit)
    return {"query": query, "memories": [m.to_dict() for m in memories]}


@app.get("/memory/important")
async def get_important_memories(limit: int = 20):
    memories = memory_engine.get_important(limit)
    return {"memories": [m.to_dict() for m in memories]}


@app.get("/memory/stats")
async def get_memory_stats():
    return memory_engine.get_stats()


@app.get("/memory/{memory_id}")
async def get_memory(memory_id: str):
    memory = memory_engine.access(memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"memory": memory.to_dict()}


@app.patch("/memory/{memory_id}")
async def update_memory(memory_id: str, data: MemoryUpdate):
    if data.importance is not None:
        memory_engine.update_importance(memory_id, data.importance)
    memory = memory_engine.get(memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"memory": memory.to_dict(), "status": "updated"}


@app.delete("/memory/{memory_id}")
async def delete_memory(memory_id: str):
    success = memory_engine.delete(memory_id)
    if not success:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"status": "deleted"}


@app.post("/brain/reason")
async def reason(request: ReasoningRequest):
    result = reasoning_engine.think(request.context, request.question)
    return result


@app.post("/brain/think")
async def chain_of_thought(problem: str, steps: int = 5):
    thoughts = reasoning_engine.chain_of_thought(problem, steps)
    return {"problem": problem, "thoughts": thoughts}


@app.post("/brain/deduce")
async def deduce(premise: str, hypothesis: str):
    result = reasoning_engine.deduce(premise, hypothesis)
    return result


@app.get("/brain/context")
async def get_brain_context():
    return {"summary": reasoning_engine.get_context_summary()}


@app.post("/planner/plan")
async def create_plan(data: PlanCreate):
    plan = planner.parse_goal_to_plan(data.goal)
    return {"plan": plan.to_dict(), "status": "created"}


@app.get("/planner/plan/{plan_id}")
async def get_plan(plan_id: str):
    plan = planner.get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"plan": plan.to_dict()}


@app.get("/planner/plans")
async def list_plans():
    return {"plans": planner.get_all_plans()}


@app.post("/planner/complete-task")
async def complete_task(data: TaskComplete):
    success = planner.complete_task(data.plan_id, data.task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plan or task not found")
    return {"status": "completed"}


@app.delete("/planner/plan/{plan_id}")
async def delete_plan(plan_id: str):
    success = planner.delete_plan(plan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"status": "deleted"}


@app.get("/skills")
async def list_skills():
    return {"skills": skill_store.list_all()}


@app.get("/skills/enabled")
async def list_enabled_skills():
    return {"skills": skill_store.list_enabled()}


@app.post("/skills/execute")
async def execute_skill(data: SkillExecute):
    result = skill_store.execute(data.skill_name, data.params)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/skills/{skill_name}")
async def get_skill(skill_name: str):
    skill = skill_store.get(skill_name)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"skill": skill.to_dict()}


@app.get("/knowledge/relation-types")
async def get_relation_types():
    return {"relation_types": RELATION_TYPES}


@app.post("/knowledge/entity")
async def create_entity(data: EntityCreate):
    entity = knowledge_graph.add_entity(
        name=data.name,
        entity_type=data.entity_type,
        description=data.description,
        properties=data.properties,
        memory_id=data.memory_id
    )
    return {"entity": entity.to_dict(), "status": "created"}


@app.get("/knowledge/entity/{entity_id}")
async def get_entity(entity_id: str):
    entity = knowledge_graph.get_entity(entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return {"entity": entity.to_dict()}


@app.get("/knowledge/entity/search/{name}")
async def search_entity(name: str):
    entity = knowledge_graph.find_entity_by_name(name)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return {"entity": entity.to_dict()}


@app.get("/knowledge/entity/{entity_id}/neighbors")
async def get_neighbors(entity_id: str, depth: int = 1, relation_type: Optional[str] = None):
    neighbors = knowledge_graph.get_neighbors(entity_id, depth, relation_type)
    return {
        "entity_id": entity_id,
        "neighbors": [(e.to_dict(), r.to_dict()) for e, r in neighbors]
    }


@app.post("/knowledge/relation")
async def create_relation(data: RelationCreate):
    relation = knowledge_graph.add_relation(
        from_entity_id=data.from_entity_id,
        to_entity_id=data.to_entity_id,
        relation_type=data.relation_type,
        weight=data.weight,
        properties=data.properties
    )
    if not relation:
        raise HTTPException(status_code=400, detail="Failed to create relation")
    return {"relation": relation.to_dict(), "status": "created"}


@app.get("/knowledge/entity/{entity_id}/relations")
async def get_entity_relations(entity_id: str, relation_type: Optional[str] = None):
    relations = knowledge_graph.get_relations(entity_id, relation_type)
    return {"relations": [r.to_dict() for r in relations]}


@app.get("/knowledge/query")
async def query_knowledge(entity_name: Optional[str] = None,
                          entity_type: Optional[str] = None,
                          relation_type: Optional[str] = None):
    result = knowledge_graph.query(entity_name, entity_type, relation_type)
    return result


@app.get("/knowledge/stats")
async def get_knowledge_stats():
    return knowledge_graph.get_stats()


@app.get("/knowledge/graph")
async def get_knowledge_graph():
    """获取知识图谱数据（用于前端可视化）"""
    return knowledge_graph.get_graph()


@app.post("/knowledge/configure")
async def configure_knowledge_graph(uri: str = "bolt://localhost:7687",
                                    user: str = "neo4j",
                                    password: str = "password",
                                    database: str = "neo4j"):
    """配置 Neo4j 连接（兼容前端调用）"""
    global knowledge_graph
    neo4j_config = {
        "uri": uri,
        "username": user,
        "password": password,
        "database": database
    }
    knowledge_graph = KnowledgeGraph(
        storage_path="database/knowledge_graph.json",
        use_neo4j=True,
        neo4j_config=neo4j_config,
        llm_model="simulated"
    )
    return {
        "status": "configured",
        "neo4j_connected": knowledge_graph.neo4j_provider.connected if knowledge_graph.neo4j_provider else False,
        "config": {"uri": uri, "database": database, "user": user}
    }


@app.delete("/knowledge/entity/{entity_id}")
async def delete_entity(entity_id: str):
    success = knowledge_graph.delete_entity(entity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Entity not found")
    return {"status": "deleted"}


@app.post("/knowledge/extract")
async def extract_from_text(text: str):
    result = knowledge_graph.extract_from_text(text)
    return result


# V2.0 新增：Neo4j 集成端点
@app.post("/knowledge/neo4j/init")
async def init_neo4j(uri: str = "bolt://localhost:7687",
                     username: str = "neo4j",
                     password: str = "password",
                     database: str = "neo4j"):
    """初始化 Neo4j 连接"""
    global knowledge_graph
    neo4j_config = {
        "uri": uri,
        "username": username,
        "password": password,
        "database": database
    }
    knowledge_graph = KnowledgeGraph(
        storage_path="database/knowledge_graph.json",
        use_neo4j=True,
        neo4j_config=neo4j_config,
        llm_model="simulated"
    )
    return {
        "status": "initialized",
        "neo4j_connected": knowledge_graph.neo4j_provider.connected if knowledge_graph.neo4j_provider else False,
        "config": {"uri": uri, "database": database}
    }


@app.get("/knowledge/neo4j/health")
async def neo4j_health():
    """检查 Neo4j 连接状态"""
    if knowledge_graph.use_neo4j and knowledge_graph.neo4j_provider:
        return knowledge_graph.neo4j_provider.get_stats()
    return {"status": "Neo4j not configured"}


@app.post("/knowledge/neo4j/sync")
async def sync_to_neo4j():
    """同步本地知识图谱到 Neo4j"""
    result = knowledge_graph.sync_to_neo4j()
    return result


@app.post("/knowledge/neo4j/cypher")
async def execute_cypher(query: str):
    """执行 Cypher 查询"""
    results = knowledge_graph.execute_cypher(query)
    return {"query": query, "results": results}


@app.get("/knowledge/path")
async def find_path_between_entities(from_entity_name: str, to_entity_name: str, max_depth: int = 5):
    """查找两个实体之间的路径"""
    from_entity = knowledge_graph.find_entity_by_name(from_entity_name)
    to_entity = knowledge_graph.find_entity_by_name(to_entity_name)
    
    if not from_entity:
        raise HTTPException(status_code=404, detail=f"Entity '{from_entity_name}' not found")
    if not to_entity:
        raise HTTPException(status_code=404, detail=f"Entity '{to_entity_name}' not found")
    
    paths = knowledge_graph.find_path(from_entity.id, to_entity.id, max_depth)
    
    path_results = []
    for path in paths:
        path_data = []
        for entity, relation in path:
            path_data.append({
                "entity": entity.to_dict(),
                "relation": relation.to_dict() if relation else None
            })
        path_results.append(path_data)
    
    return {
        "from": from_entity_name,
        "to": to_entity_name,
        "paths_found": len(path_results),
        "paths": path_results
    }


@app.post("/knowledge/analyze")
async def analyze_text_with_llm(text: str):
    """使用 LLM 分析文本，提取实体和关系"""
    result = knowledge_graph.extract_from_text(text, use_llm=True)
    
    # 将提取的实体和关系添加到知识图谱
    for entity_data in result.get("entities", []):
        knowledge_graph.add_entity(
            name=entity_data.get("name", ""),
            entity_type=entity_data.get("entity_type", "concept"),
            description=entity_data.get("metadata", {}).get("description", "")
        )
    
    return {
        "summary": result.get("summary", ""),
        "entities_found": len(result.get("entities", [])),
        "relations_found": len(result.get("relations", [])),
        "cypher_query": result.get("cypher_query", ""),
        "data": result
    }


@app.get("/knowledge/cypher")
async def export_cypher():
    statements = knowledge_graph.export_to_cypher()
    return {"statements": statements}


@app.post("/learning/experience")
async def add_learning_experience(data: LearningExperienceCreate):
    experience = learning_engine.add_experience(
        task=data.task,
        result=data.result,
        time_taken=data.time_taken,
        lesson=data.lesson,
        category=data.category,
        tags=data.tags,
        success=data.success,
        difficulty=data.difficulty
    )
    return {"experience": experience.to_dict(), "status": "created"}


@app.get("/learning/experience/{exp_id}")
async def get_learning_experience(exp_id: str):
    exp = learning_engine.get_experience(exp_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    return {"experience": exp.to_dict()}


@app.get("/learning/experiences")
async def list_experiences(limit: int = 20):
    experiences = learning_engine.get_recent_experiences(limit)
    return {"experiences": [e.to_dict() for e in experiences]}


@app.get("/learning/experiences/category/{category}")
async def get_by_category(category: str):
    experiences = learning_engine.get_experiences_by_category(category)
    return {"category": category, "experiences": [e.to_dict() for e in experiences]}


@app.get("/learning/experiences/tags/{tags}")
async def get_by_tags(tags: str):
    tag_list = tags.split(",")
    experiences = learning_engine.get_experiences_by_tags(tag_list)
    return {"tags": tag_list, "experiences": [e.to_dict() for e in experiences]}


@app.get("/learning/lessons")
async def get_lessons(limit: int = 10):
    lessons = learning_engine.get_learned_lessons(limit)
    return {"lessons": lessons}


@app.get("/learning/suggestions/{task}")
async def get_suggestions(task: str):
    suggestions = learning_engine.suggest_next_actions(task)
    return {"task": task, "suggestions": suggestions}


@app.get("/learning/patterns")
async def get_patterns():
    patterns = learning_engine.patterns.values()
    return {"patterns": [p.to_dict() for p in patterns]}


@app.get("/learning/growth-report")
async def get_growth_report():
    report = learning_engine.get_growth_report()
    return report


@app.get("/learning/feedback/{exp_id}")
async def provide_feedback(exp_id: str, feedback: str, rating: int = 5):
    learning_engine.update_experience_feedback(exp_id, feedback, rating)
    exp = learning_engine.get_experience(exp_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    return {"experience": exp.to_dict(), "status": "updated"}


@app.get("/digital-twin/profile")
async def get_twin_profile():
    profile = digital_twin.get_profile()
    if not profile:
        return {"profile": None, "message": "Digital Twin not initialized"}
    return {"profile": profile}


@app.post("/digital-twin/initialize")
async def initialize_twin(name: str = "My Digital Twin"):
    digital_twin.initialize(name)
    return {"status": "initialized", "profile": digital_twin.get_profile()}


@app.patch("/digital-twin/writing-style")
async def update_writing_style(data: TwinUpdate):
    updates = {}
    if data.writing_formal_level is not None:
        updates["formal_level"] = data.writing_formal_level
    if data.writing_tone is not None:
        updates["tone"] = data.writing_tone
    digital_twin.update_writing_style(**updates)
    return {"status": "updated", "profile": digital_twin.get_profile()}


@app.post("/digital-twin/writing-samples")
async def add_writing_sample(sample: str):
    digital_twin.add_writing_sample(sample)
    return {"status": "updated"}


@app.patch("/digital-twin/code-style")
async def update_code_style(data: TwinUpdate):
    updates = {}
    if data.code_naming_convention is not None:
        updates["naming_convention"] = data.code_naming_convention
    digital_twin.update_code_style(**updates)
    return {"status": "updated", "profile": digital_twin.get_profile()}


@app.post("/digital-twin/code-samples")
async def add_code_sample(sample: str, language: str = "python"):
    digital_twin.add_code_sample(sample, language)
    return {"status": "updated"}


@app.post("/digital-twin/interests")
async def update_interests(interests: List[str]):
    digital_twin.update_interests(interests)
    return {"status": "updated"}


@app.post("/digital-twin/strengths-weaknesses")
async def update_strengths_weaknesses(data: TwinUpdate):
    digital_twin.update_strengths_weaknesses(
        strengths=data.strengths,
        weaknesses=data.weaknesses
    )
    return {"status": "updated"}


@app.post("/digital-twin/decision")
async def record_decision(situation: str, decision: str, reasoning: str, outcome: str):
    digital_twin.record_decision(situation, decision, reasoning, outcome)
    return {"status": "recorded"}


@app.get("/digital-twin/decision/{situation}")
async def suggest_decision(situation: str):
    suggestion = digital_twin.suggest_decision(situation)
    if not suggestion:
        return {"suggestion": None, "message": "No matching decision pattern found"}
    return {"situation": situation, "suggestion": suggestion}


@app.get("/digital-twin/response-style/{context}")
async def get_response_style(context: str):
    style = digital_twin.generate_response_style(context)
    return {"context": context, "style": style}


@app.get("/digital-twin/learning-recommendations")
async def get_learning_recommendations():
    recommendations = digital_twin.get_learning_recommendations()
    return {"recommendations": recommendations}


@app.get("/digital-twin/interests-overview")
async def get_interests_overview():
    overview = digital_twin.get_interests_overview()
    return overview


@app.post("/rag/query")
async def rag_query(data: RAGQuery):
    result = rag_engine.query(
        question=data.question,
        top_k=data.top_k,
        use_rerank=data.use_rerank,
        use_hybrid=data.use_hybrid,
        include_citations=data.include_citations
    )
    return result


@app.post("/rag/add-text")
async def rag_add_text(data: RAGAddText):
    chunks = rag_engine.add_text(
        text=data.text,
        source=data.source,
        metadata=data.metadata,
        chunk_size=data.chunk_size,
        overlap=data.overlap
    )
    return {
        "status": "added",
        "chunks_created": len(chunks),
        "chunks": [c.to_dict() for c in chunks]
    }


@app.post("/rag/add-document")
async def rag_add_document(data: RAGAddDocument):
    doc = rag_engine.add_document(Document(
        title=data.title,
        content=data.content,
        source_type=data.source_type,
        metadata=data.metadata or {}
    ))
    return {
        "status": "added",
        "document": doc.to_dict()
    }


@app.get("/rag/search")
async def rag_search(query: str, top_k: int = 10):
    results = rag_engine.search(query, top_k=top_k)
    return {"query": query, "results": results}


@app.get("/rag/stats")
async def rag_stats():
    return rag_engine.get_stats()


@app.delete("/rag/delete/{source}")
async def rag_delete_by_source(source: str):
    deleted = rag_engine.delete_by_source(source)
    return {"status": "deleted", "chunks_deleted": deleted}


@app.get("/agent/skills")
async def list_agent_skills():
    return {"skills": agent_runtime.skill_registry.list_all()}


@app.post("/agent/task")
async def create_agent_task(data: AgentTaskCreate):
    task = agent_runtime.create_task(
        name=data.name,
        task_type=data.task_type,
        input_data=data.input_data,
        priority=TaskPriority(data.priority),
        dependencies=data.dependencies
    )
    return {"task": task.to_dict(), "status": "created"}


@app.post("/agent/execute/{task_id}")
async def execute_agent_task(task_id: str):
    result = agent_runtime.execute_task(task_id)
    return result


@app.get("/agent/task/{task_id}")
async def get_agent_task(task_id: str):
    task = agent_runtime.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task": task.to_dict()}


@app.get("/agent/tasks")
async def list_agent_tasks(status: Optional[str] = None):
    task_status = TaskStatus(status) if status else None
    return {"tasks": agent_runtime.list_tasks(task_status)}


@app.post("/agent/workflow")
async def create_workflow(data: AgentWorkflowCreate):
    workflow = agent_runtime.create_workflow(
        name=data.name,
        description=data.description
    )
    return {"workflow": workflow.to_dict(), "status": "created"}


@app.post("/agent/workflow/{workflow_id}/add-task/{task_id}")
async def add_task_to_workflow(workflow_id: str, task_id: str):
    task = agent_runtime.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    success = agent_runtime.add_task_to_workflow(workflow_id, task)
    if not success:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return {"status": "added"}


@app.post("/agent/workflow/{workflow_id}/execute")
async def execute_workflow(workflow_id: str):
    result = agent_runtime.execute_workflow(workflow_id)
    return result


@app.get("/agent/workflows")
async def list_workflows():
    return {"workflows": agent_runtime.list_workflows()}


@app.get("/agent/workflow/{workflow_id}")
async def get_workflow(workflow_id: str):
    workflow = agent_runtime.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"workflow": workflow.to_dict()}


@app.get("/agent/history")
async def get_agent_history(limit: int = 50):
    return {"history": agent_runtime.get_execution_history(limit)}


@app.post("/reflection/reflect")
async def create_reflection(data: ReflectionCreate):
    reflection = reflection_engine.reflect(
        task_id=data.task_id,
        task_name=data.task_name,
        what_happened=data.what_happened,
        what_went_well=data.what_went_well,
        what_could_improve=data.what_could_improve,
        mistakes=data.mistakes,
        lessons_learned=data.lessons_learned,
        confidence_level=data.confidence_level
    )
    return {"reflection": reflection.to_dict(), "status": "created"}


@app.get("/reflection/{reflection_id}")
async def get_reflection(reflection_id: str):
    reflection = reflection_engine.get_reflection(reflection_id)
    if not reflection:
        raise HTTPException(status_code=404, detail="Reflection not found")
    return {"reflection": reflection.to_dict()}


@app.get("/reflection/recent")
async def get_recent_reflections(limit: int = 20):
    reflections = reflection_engine.get_recent_reflections(limit)
    return {"reflections": [r.to_dict() for r in reflections]}


@app.get("/reflection/improvements/pending")
async def get_pending_improvements(limit: int = 10):
    improvements = reflection_engine.get_pending_improvements(limit)
    return {"improvements": [i.to_dict() for i in improvements]}


@app.post("/reflection/improvement/apply")
async def apply_improvement(data: ImprovementApply):
    success = reflection_engine.apply_improvement(
        improvement_id=data.improvement_id,
        actual_outcome=data.actual_outcome,
        success=data.success
    )
    if not success:
        raise HTTPException(status_code=404, detail="Improvement not found")
    return {"status": "updated"}


@app.get("/reflection/suggestions/{task_name}")
async def get_reflection_suggestions(task_name: str):
    suggestions = reflection_engine.suggest_for_next_task(task_name)
    return {"task_name": task_name, "suggestions": suggestions}


@app.get("/reflection/growth-report")
async def get_reflection_growth_report():
    report = reflection_engine.get_growth_report()
    return report


@app.delete("/reflection/{reflection_id}")
async def delete_reflection(reflection_id: str):
    success = reflection_engine.delete_reflection(reflection_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reflection not found")
    return {"status": "deleted"}


@app.post("/knowledge-base/markdown")
async def kb_add_markdown(data: KBAddMarkdown):
    doc = knowledge_base.add_markdown(
        content=data.content,
        title=data.title,
        metadata=data.metadata
    )
    return {"status": "added", "document": doc.to_dict()}


@app.post("/knowledge-base/text")
async def kb_add_text(data: KBAddText):
    doc = knowledge_base.add_text(
        content=data.content,
        title=data.title,
        metadata=data.metadata
    )
    return {"status": "added", "document": doc.to_dict()}


@app.post("/knowledge-base/web")
async def kb_add_web(data: KBAddWeb):
    doc = knowledge_base.add_web_content(
        url=data.url,
        content=data.content,
        title=data.title
    )
    return {"status": "added", "document": doc.to_dict()}


@app.get("/knowledge-base/query")
async def kb_query(question: str, top_k: int = 5):
    result = knowledge_base.query(question, top_k=top_k)
    return result


@app.get("/knowledge-base/search")
async def kb_search(query: str, top_k: int = 10):
    results = knowledge_base.search(query, top_k=top_k)
    return {"query": query, "results": results}


@app.get("/knowledge-base/documents")
async def kb_list_documents():
    return {"documents": knowledge_base.list_documents()}


@app.get("/knowledge-base/document/{doc_id}")
async def kb_get_document(doc_id: str):
    doc = knowledge_base.get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"document": doc.to_dict()}


@app.delete("/knowledge-base/document/{doc_id}")
async def kb_delete_document(doc_id: str):
    success = knowledge_base.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"status": "deleted"}


@app.get("/knowledge-base/stats")
async def kb_stats():
    return knowledge_base.get_stats()


@app.post("/auth/register")
async def register(data: UserRegister):
    result = auth_service.register(
        username=data.username,
        email=data.email,
        password=data.password,
        full_name=data.full_name
    )
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@app.post("/auth/login")
async def login(data: UserLogin):
    result = auth_service.login(email=data.email, password=data.password)
    if result["status"] == "error":
        raise HTTPException(status_code=401, detail=result["message"])
    return result


@app.post("/auth/login/username")
async def login_by_username(data: UserLoginByUsername):
    result = auth_service.login_by_username(
        username=data.username,
        password=data.password
    )
    if result["status"] == "error":
        raise HTTPException(status_code=401, detail=result["message"])
    return result


@app.post("/auth/verify-token")
async def verify_token(token: str):
    result = auth_service.verify_token(token)
    if result["status"] == "error":
        raise HTTPException(status_code=401, detail=result["message"])
    return result


@app.post("/auth/refresh-token")
async def refresh_token(data: TokenRefresh):
    result = auth_service.refresh_token(data.token)
    if result["status"] == "error":
        raise HTTPException(status_code=401, detail=result["message"])
    return result


@app.post("/auth/change-password/{user_id}")
async def change_password(user_id: str, data: PasswordChange):
    result = auth_service.change_password(
        user_id=user_id,
        old_password=data.old_password,
        new_password=data.new_password
    )
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@app.get("/auth/user/{user_id}")
async def get_user(user_id: str):
    user = auth_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user.to_dict()}


@app.patch("/auth/profile/{user_id}")
async def update_profile(user_id: str, data: ProfileUpdate):
    updates = {}
    if data.username:
        updates["username"] = data.username
    if data.full_name:
        updates["full_name"] = data.full_name
    if data.avatar_url:
        updates["avatar_url"] = data.avatar_url

    if not updates:
        raise HTTPException(status_code=400, detail="No updates provided")

    result = auth_service.update_profile(user_id, **updates)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@app.delete("/auth/user/{user_id}")
async def delete_user(user_id: str, data: UserDelete):
    result = auth_service.delete_user(user_id, data.password)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result


@app.get("/auth/stats")
async def get_auth_stats():
    return auth_service.get_stats()


@app.get("/timeline")
async def get_timeline(year: Optional[int] = None, month: Optional[int] = None):
    if year and month:
        events = timeline.get_events_by_month(year, month)
        return {"year": year, "month": month, "events": [e.to_dict() for e in events]}
    elif year:
        events = timeline.get_events_by_year(year)
        return {"year": year, "events": [e.to_dict() for e in events]}
    else:
        groups = timeline.get_timeline_by_year()
        return {"groups": [g.to_dict() for g in groups]}


@app.get("/timeline/monthly")
async def get_timeline_monthly():
    groups = timeline.get_timeline_by_month()
    return {"groups": [g.to_dict() for g in groups]}


@app.get("/timeline/events")
async def get_all_events():
    events = timeline.get_all_events()
    return {"events": [e.to_dict() for e in events]}


@app.get("/timeline/events/tag/{tag}")
async def get_events_by_tag(tag: str):
    events = timeline.get_events_by_tag(tag)
    return {"tag": tag, "events": [e.to_dict() for e in events]}


@app.get("/timeline/events/importance")
async def get_events_by_importance(min_importance: float = 0.7):
    events = timeline.get_events_by_importance(min_importance)
    return {"min_importance": min_importance, "events": [e.to_dict() for e in events]}


@app.get("/timeline/milestones")
async def get_milestones():
    events = timeline.get_milestone_events()
    return {"milestones": [e.to_dict() for e in events]}


@app.get("/timeline/summary")
async def get_timeline_summary():
    return timeline.get_timeline_summary()


@app.get("/timeline/stats")
async def get_timeline_stats():
    return timeline.get_timeline_stats()


@app.get("/timeline/export")
async def export_timeline():
    success = timeline.export_timeline()
    return {"status": "success" if success else "failed"}


@app.get("/dashboard/metrics")
async def get_dashboard_metrics():
    metrics = dashboard.get_metrics()
    return metrics.to_dict()


@app.get("/dashboard/report")
async def get_dashboard_report():
    return dashboard.get_detailed_report()


@app.get("/dashboard/summary")
async def get_dashboard_summary():
    return dashboard.get_summary()


@app.get("/dashboard/growth-score")
async def get_growth_score():
    metrics = dashboard.get_metrics()
    return {
        "growth_score": metrics.growth_score,
        "level": dashboard._get_growth_level(metrics.growth_score),
        "max_score": 100
    }


@app.get("/dashboard/recommendations")
async def get_recommendations():
    metrics = dashboard.get_metrics()
    return {"recommendations": dashboard._generate_recommendations(metrics)}


# ==========================================
# Behavior Analytics API (Task 10)
# ==========================================
from analytics.behavior_analytics import BehaviorAnalytics

behavior_analytics = BehaviorAnalytics()


class ActivityRecord(BaseModel):
    activity_type: str
    duration_minutes: float
    metadata: Optional[Dict[str, Any]] = None


@app.get("/analytics/metrics")
async def get_behavior_metrics(days: int = 30):
    """获取行为指标"""
    from datetime import timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    metrics = behavior_analytics.get_metrics(start_date, end_date)
    return metrics.to_dict()


@app.post("/analytics/activity")
async def record_activity(activity: ActivityRecord):
    """记录活动"""
    behavior_analytics.record_activity(
        activity_type=activity.activity_type,
        duration_minutes=activity.duration_minutes,
        metadata=activity.metadata
    )
    return {"status": "recorded", "activity_type": activity.activity_type}


@app.get("/analytics/weekly-report")
async def get_weekly_report():
    """获取周报"""
    report = behavior_analytics.get_weekly_report()
    return report.to_dict()


@app.get("/analytics/monthly-report")
async def get_monthly_report(year: Optional[int] = None, month: Optional[int] = None):
    """获取月报"""
    report = behavior_analytics.get_monthly_report(year, month)
    return report.to_dict()


@app.get("/analytics/chart-data")
async def get_activity_chart_data(days: int = 30):
    """获取活动图表数据"""
    return behavior_analytics.get_activity_chart_data(days)


@app.get("/analytics/category-breakdown")
async def get_category_breakdown(days: int = 30):
    """获取活动类别分解"""
    return behavior_analytics.get_category_breakdown(days)


@app.get("/analytics/hourly-distribution")
async def get_hourly_distribution(days: int = 30):
    """获取每小时活动分布"""
    return behavior_analytics.get_hourly_distribution(days)


@app.get("/analytics/summary")
async def get_analytics_summary():
    """获取分析摘要"""
    weekly = behavior_analytics.get_weekly_report()
    category = behavior_analytics.get_category_breakdown(30)
    
    return {
        "weekly_metrics": weekly.metrics.to_dict(),
        "achievements": weekly.achievements,
        "recommendations": weekly.recommendations,
        "top_activities": weekly.top_activities,
        "category_distribution": category["percentages"],
        "streak_days": weekly.metrics.streak_days
    }


@app.post("/goal-tree/goal")
async def create_goal(data: GoalCreate):
    deadline = datetime.fromisoformat(data.deadline) if data.deadline else None
    try:
        goal = goal_tree.add_root_goal(
            title=data.title,
            description=data.description,
            category=data.category,
            priority=data.priority,
            deadline=deadline
        )
        return {"status": "success", "goal": goal.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/goal-tree/subgoal")
async def create_subgoal(data: SubgoalCreate):
    deadline = datetime.fromisoformat(data.deadline) if data.deadline else None
    goal = goal_tree.add_subgoal(
        parent_id=data.parent_id,
        title=data.title,
        description=data.description,
        priority=data.priority,
        deadline=deadline
    )
    if not goal:
        raise HTTPException(status_code=404, detail="Parent goal not found")
    return {"status": "success", "goal": goal.to_dict()}


@app.get("/goal-tree/tree")
async def get_goal_tree(category: Optional[str] = None):
    if category:
        goals = goal_tree.get_tree_by_category(category)
        return {"category": category, "goals": [g.to_dict() for g in goals]}
    return {"goals": [g.to_dict() for g in goal_tree.root_nodes]}


@app.get("/goal-tree/goal/{goal_id}")
async def get_goal(goal_id: str):
    goal = goal_tree.find_node(goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"goal": goal.to_dict()}


@app.put("/goal-tree/goal/{goal_id}")
async def update_goal(goal_id: str, data: GoalUpdate):
    updates = {}
    if data.title:
        updates["title"] = data.title
    if data.description:
        updates["description"] = data.description
    if data.priority:
        updates["priority"] = data.priority
    if data.status:
        updates["status"] = data.status
    if data.progress is not None:
        updates["progress"] = data.progress
    if data.deadline:
        updates["deadline"] = datetime.fromisoformat(data.deadline)

    if not updates:
        raise HTTPException(status_code=400, detail="No updates provided")

    success = goal_tree.update_goal(goal_id, **updates)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found")

    goal = goal_tree.find_node(goal_id)
    return {"status": "success", "goal": goal.to_dict()}


@app.delete("/goal-tree/goal/{goal_id}")
async def delete_goal(goal_id: str):
    success = goal_tree.delete_goal(goal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found")
    return {"status": "deleted"}


@app.get("/goal-tree/summary")
async def get_goal_tree_summary():
    return goal_tree.get_tree_summary()


@app.get("/goal-tree/priority")
async def get_priority_goals(limit: int = 5):
    return {"goals": goal_tree.get_priority_goals(limit)}


@app.get("/goal-tree/overdue")
async def get_overdue_goals():
    return {"overdue": goal_tree.get_overdue_goals()}


@app.get("/goal-tree/categories")
async def get_goal_categories():
    return {"categories": ["Career", "Learning", "Health", "Project"]}


@app.get("/multi-agent/agents")
async def list_agents(agent_type: Optional[str] = None):
    if agent_type:
        agents = multi_agent.get_agents_by_type(agent_type)
        return {"agents": [a.to_dict() for a in agents]}
    return {"agents": multi_agent.list_agents()}


@app.get("/multi-agent/agent/{agent_id}")
async def get_agent(agent_id: str):
    agent = multi_agent.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"agent": agent.to_dict()}


@app.post("/multi-agent/agent")
async def create_agent(data: AgentCreate):
    try:
        agent = multi_agent.add_agent(
            name=data.name,
            agent_type=data.agent_type,
            description=data.description,
            skills=data.skills or []
        )
        return {"status": "success", "agent": agent.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/multi-agent/task")
async def assign_task(data: AgentTaskAssign):
    task = multi_agent.assign_task(
        agent_id=data.agent_id,
        title=data.title,
        description=data.description
    )
    if not task:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"status": "success", "task": task.to_dict()}


@app.post("/multi-agent/task/{task_id}/execute")
async def execute_task(task_id: str):
    try:
        task = multi_agent.execute_task(task_id)
        return {"status": "success", "task": task.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/multi-agent/task/{task_id}")
async def get_task(task_id: str):
    task = multi_agent.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task": task.to_dict()}


@app.get("/multi-agent/tasks")
async def list_tasks(status: Optional[str] = None):
    return {"tasks": multi_agent.list_tasks(status)}


@app.post("/multi-agent/workflow")
async def create_workflow(data: WorkflowCreate):
    workflow = multi_agent.create_workflow(data.goal)
    return {"status": "success", "workflow": workflow}


@app.post("/multi-agent/workflow/execute")
async def execute_workflow(data: WorkflowCreate):
    result = multi_agent.execute_workflow(data.goal)
    return {"status": "success", **result}


@app.get("/multi-agent/workflow/history")
async def get_workflow_history():
    return {"messages": multi_agent.get_workflow_history()}


@app.get("/multi-agent/stats")
async def get_multi_agent_stats():
    return multi_agent.get_stats()


@app.get("/multi-agent/types")
async def get_agent_types():
    return {"types": ["research", "planner", "coding", "reviewer", "search", "analyzer", "summarizer"]}


@app.post("/cognitive/episodic")
async def add_episodic_memory(data: EpisodicMemoryCreate):
    time = datetime.fromisoformat(data.time) if data.time else datetime.now()
    memory = cognitive_memory.add_episodic(
        time=time,
        location=data.location,
        people=data.people or [],
        event=data.event,
        emotion=data.emotion,
        content=data.content,
        importance=data.importance,
        tags=data.tags or []
    )
    return {"status": "success", "memory": memory.to_dict()}


@app.get("/cognitive/episodic")
async def list_episodic_memories(year: Optional[int] = None, emotion: Optional[str] = None):
    return {"memories": cognitive_memory.list_episodic(year, emotion)}


@app.get("/cognitive/episodic/{memory_id}")
async def get_episodic_memory(memory_id: str):
    memory = cognitive_memory.get_episodic(memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"memory": memory.to_dict()}


@app.post("/cognitive/semantic")
async def add_semantic_memory(data: SemanticMemoryCreate):
    memory = cognitive_memory.add_semantic(
        concept=data.concept,
        definition=data.definition,
        relations=data.relations or [],
        examples=data.examples or [],
        source=data.source,
        confidence=data.confidence
    )
    return {"status": "success", "memory": memory.to_dict()}


@app.get("/cognitive/semantic")
async def list_semantic_memories(concept: Optional[str] = None):
    return {"memories": cognitive_memory.list_semantic(concept)}


@app.get("/cognitive/semantic/{memory_id}")
async def get_semantic_memory(memory_id: str):
    memory = cognitive_memory.get_semantic(memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"memory": memory.to_dict()}


@app.post("/cognitive/procedural")
async def add_procedural_memory(data: ProceduralMemoryCreate):
    memory = cognitive_memory.add_procedural(
        skill=data.skill,
        steps=data.steps,
        prerequisites=data.prerequisites or [],
        difficulty=data.difficulty,
        tags=data.tags or []
    )
    return {"status": "success", "memory": memory.to_dict()}


@app.get("/cognitive/procedural")
async def list_procedural_memories(skill: Optional[str] = None, difficulty: Optional[str] = None):
    return {"memories": cognitive_memory.list_procedural(skill, difficulty)}


@app.get("/cognitive/procedural/{memory_id}")
async def get_procedural_memory(memory_id: str):
    memory = cognitive_memory.get_procedural(memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"memory": memory.to_dict()}


@app.post("/cognitive/procedural/{memory_id}/practice")
async def practice_skill(memory_id: str, data: SkillPractice):
    success = cognitive_memory.practice_skill(memory_id, data.practice_quality)
    if not success:
        raise HTTPException(status_code=404, detail="Memory not found")
    memory = cognitive_memory.get_procedural(memory_id)
    return {"status": "success", "mastery_level": memory.mastery_level}


@app.get("/cognitive/search")
async def cognitive_search(query: str):
    return cognitive_memory.search(query)


@app.get("/cognitive/stats")
async def cognitive_stats():
    return cognitive_memory.get_stats()


@app.get("/cognitive/timeline")
async def cognitive_timeline():
    return {"events": cognitive_memory.get_timeline()}


@app.get("/cognitive/types")
async def get_memory_types():
    return {"types": ["episodic", "semantic", "procedural"]}


@app.get("/marketplace/packages")
async def list_packages(agent_type: Optional[str] = None, search_query: Optional[str] = None,
                        featured_only: bool = False, installed_only: bool = False):
    return {"packages": marketplace.list_packages(agent_type, search_query, featured_only, installed_only)}


@app.get("/marketplace/package/{package_id}")
async def get_package(package_id: str):
    package = marketplace.get_package(package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return {"package": package.to_dict()}


@app.post("/marketplace/package/{package_id}/install")
async def install_package(package_id: str):
    success = marketplace.install_package(package_id)
    if not success:
        raise HTTPException(status_code=404, detail="Package not found")
    package = marketplace.get_package(package_id)
    return {"status": "installed", "package": package.to_dict()}


@app.post("/marketplace/package/{package_id}/uninstall")
async def uninstall_package(package_id: str):
    success = marketplace.uninstall_package(package_id)
    if not success:
        raise HTTPException(status_code=404, detail="Package not found or not installed")
    package = marketplace.get_package(package_id)
    return {"status": "uninstalled", "package": package.to_dict()}


@app.get("/marketplace/installed")
async def get_installed_packages():
    return {"packages": marketplace.get_installed_packages()}


@app.get("/marketplace/featured")
async def get_featured_packages():
    return {"packages": marketplace.get_featured_packages()}


@app.get("/marketplace/search")
async def search_marketplace(query: str):
    return {"packages": marketplace.search_packages(query)}


@app.get("/marketplace/stats")
async def get_marketplace_stats():
    return marketplace.get_stats()


@app.get("/marketplace/categories")
async def get_marketplace_categories():
    return {"categories": marketplace.get_categories()}


# ==========================================
# Chat API
# ==========================================
@app.post("/chat")
async def chat(request: ChatRequest):
    """Send a chat message and get a response"""
    # Store user message
    user_memory_id = None
    if request.store_to_memory:
        user_memory = memory_engine.add(
            content=f"User: {request.message}",
            importance=request.importance,
            tags=["chat", "user"]
        )
        user_memory_id = user_memory.id
    
    chat_engine.add_message(
        role="user",
        content=request.message,
        memory_id=user_memory_id
    )
    
    # Generate a simple response (this will be replaced with LLM in later versions)
    assistant_response = _generate_simple_response(request.message)
    
    # Store assistant message
    assistant_memory_id = None
    if request.store_to_memory:
        assistant_memory = memory_engine.add(
            content=f"Assistant: {assistant_response}",
            importance=request.importance * 0.9,
            tags=["chat", "assistant"]
        )
        assistant_memory_id = assistant_memory.id
    
    chat_message = chat_engine.add_message(
        role="assistant",
        content=assistant_response,
        memory_id=assistant_memory_id
    )
    
    return {
        "message": {
            "id": chat_message.id,
            "role": chat_message.role,
            "content": chat_message.content,
            "timestamp": chat_message.timestamp
        },
        "user_memory_id": user_memory_id,
        "assistant_memory_id": assistant_memory_id,
        "status": "success"
    }


@app.get("/chat/history")
async def get_chat_history(limit: int = 50):
    """Get chat history"""
    messages = chat_engine.get_recent(limit)
    return {
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "timestamp": m.timestamp,
                "memory_id": m.memory_id
            }
            for m in messages
        ],
        "total": len(messages)
    }


@app.get("/chat/stats")
async def get_chat_stats():
    """Get chat statistics"""
    return chat_engine.get_stats()


@app.delete("/chat/history")
async def clear_chat_history():
    """Clear chat history"""
    chat_engine.clear()
    return {"status": "cleared"}


# ==========================================
# LLM Chat API (v1.0 - DeepSeek/OpenAI Integration)
# ==========================================
from fastapi.responses import StreamingResponse
from llm.llm_service import llm_service


class LLMChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    system_prompt: Optional[str] = None
    store_to_memory: bool = True


class LLMConfigRequest(BaseModel):
    provider: str = "deepseek"  # deepseek, openai, simulated
    api_key: str
    model: Optional[str] = None
    base_url: Optional[str] = None


@app.post("/chat/llm")
async def chat_with_llm(request: LLMChatRequest):
    """Send a chat message and get AI response using LLM"""
    result = await chat_engine.chat(
        message=request.message,
        session_id=request.session_id,
        system_prompt=request.system_prompt
    )
    
    # Store to memory if requested
    if request.store_to_memory:
        memory_engine.add(
            content=f"User: {request.message}",
            importance=0.6,
            tags=["chat", "user", "llm"]
        )
        memory_engine.add(
            content=f"Assistant: {result['response']}",
            importance=0.5,
            tags=["chat", "assistant", "llm"]
        )
    
    return {
        "response": result["response"],
        "user_message": result["user_message"],
        "assistant_message": result["assistant_message"],
        "session_id": result["session_id"],
        "status": "success"
    }


@app.post("/chat/llm/stream")
async def chat_with_llm_stream(request: LLMChatRequest):
    """Send a chat message and get streaming AI response using LLM (SSE)"""
    
    async def generate():
        async for chunk in chat_engine.chat_stream(
            message=request.message,
            session_id=request.session_id,
            system_prompt=request.system_prompt
        ):
            yield chunk
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.get("/llm/config")
async def get_llm_config():
    """Get current LLM configuration"""
    return llm_service.get_config()


@app.post("/llm/config")
async def set_llm_config(request: LLMConfigRequest):
    """Configure LLM service"""
    config = chat_engine.configure_llm(
        provider=request.provider,
        api_key=request.api_key,
        model=request.model,
        base_url=request.base_url
    )
    return {
        "status": "configured",
        "config": config
    }


@app.get("/llm/status")
async def get_llm_status():
    """Get LLM service status"""
    return {
        "configured": llm_service.is_configured(),
        "provider": llm_service.config.provider,
        "model": llm_service.config.model
    }


# ==================== Vector DB API Endpoints (v1.5) ====================

class VectorDBInit(BaseModel):
    provider: str = 'in_memory'
    host: Optional[str] = 'localhost'
    port: Optional[int] = 6333
    api_key: Optional[str] = None
    dimension: int = 384


@app.post("/vector-db/init")
async def init_vector_db(config: VectorDBInit):
    """Initialize or switch Vector DB provider"""
    success = vector_db_manager.initialize(
        provider_type=config.provider,
        embed_service=embedding_service,
        host=config.host or 'localhost',
        port=config.port or 6333,
        api_key=config.api_key,
        dimension=config.dimension
    )
    if success:
        return {"status": "initialized", "provider": config.provider}
    return {"status": "failed", "error": "Failed to initialize vector DB"}


@app.get("/vector-db/health")
async def vector_db_health():
    """Check Vector DB health status"""
    return vector_db_manager.health_check()


@app.get("/vector-db/stats")
async def vector_db_stats():
    """Get Vector DB statistics"""
    return vector_db_manager.get_stats()


@app.get("/memory/semantic/{query}")
async def semantic_search(query: str, limit: int = 10):
    """Semantic search using vector similarity"""
    results = memory_engine.semantic_search(query, limit)
    return {
        "query": query,
        "results": [m.to_dict() for m in results],
        "count": len(results)
    }


@app.post("/memory/sync-vector-db")
async def sync_memories_to_vector_db():
    """Sync all existing memories to vector database"""
    count = memory_engine.sync_to_vector_db()
    return {"synced": count, "status": "completed"}



def _generate_simple_response(user_message: str) -> str:
    """Generate a simple response (placeholder for LLM)"""
    message_lower = user_message.lower()
    
    if "你好" in message_lower or "hello" in message_lower or "hi" in message_lower:
        return "你好！我是 TitanOS，你的个人 AI 助手。有什么我可以帮你的吗？"
    
    if "记忆" in message_lower or "memory" in message_lower:
        return "我正在记录我们的对话到记忆系统中。你可以在 Memory 页面查看所有记忆！"
    
    if "目标" in message_lower or "goal" in message_lower:
        return "设置目标是个好主意！你可以在 Goals 页面创建和跟踪你的目标。"
    
    if "知识" in message_lower or "knowledge" in message_lower:
        return "知识图谱正在构建中！很快你就能看到我们的知识网络了。"
    
    if "学习" in message_lower or "learn" in message_lower:
        return "学习是进步的关键！我正在记录你的学习过程。"
    
    if "谢谢" in message_lower or "thank" in message_lower:
        return "不客气！很高兴能帮到你 😊"
    
    # Default responses
    default_responses = [
        f"我理解了，你说的是：{user_message[:50]}...",
        "这是个有趣的话题！让我想想...",
        "好的，我记下来了。还有什么我可以帮你的吗？",
        "收到！我正在记录这个对话到你的记忆系统中。"
    ]
    
    import random
    return random.choice(default_responses)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
