from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

app = FastAPI(title="TitanOS API", version="0.2.0", description="Personal AI Operating System v0.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_engine = MemoryEngine()
reasoning_engine = ReasoningEngine()
planner = Planner()
skill_store = SkillStore()
knowledge_graph = KnowledgeGraph()
learning_engine = LearningEngine()
digital_twin = DigitalTwin()


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


@app.get("/")
async def root():
    return {
        "name": "TitanOS",
        "version": "0.2.0",
        "description": "Personal AI Operating System - Memory, Reasoning, Planning, Learning & Digital Twin"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "modules": {
            "memory": "active",
            "brain": "active",
            "planner": "active",
            "skills": "active",
            "knowledge_graph": "active",
            "learning": "active",
            "digital_twin": "active"
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


@app.get("/memory/{memory_id}")
async def get_memory(memory_id: str):
    memory = memory_engine.access(memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"memory": memory.to_dict()}


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


@app.post("/digital-twin/sync-learning")
async def sync_with_learning():
    success = digital_twin.sync_with_learning_engine(learning_engine)
    return {"synced": success, "profile": digital_twin.get_profile()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
