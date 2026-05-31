# TitanOS API Reference

## Base URL

```
http://localhost:8000
```

---

## Authentication

大多数接口需要 JWT Token 认证。

### Request Header

```http
Authorization: Bearer <token>
```

---

## 1. Memory API

### 1.1 Add Memory

**POST** `/memory`

添加一条记忆

**Request Body**:
```json
{
  "content": "string (required) - 记忆内容",
  "importance": "number (optional) - 重要性 0-1, default: 0.5",
  "tags": ["string"] (optional) - 标签列表,
  "embedding": [number] (optional) - 向量表示
}
```

**Response**:
```json
{
  "memory": {
    "id": "string - 记忆ID",
    "content": "string - 记忆内容",
    "importance": "number",
    "tags": ["string"],
    "created_at": "string - ISO datetime",
    "access_count": "number",
    "score": "number"
  },
  "status": "created"
}
```

**Error Codes**:
- `400`: Invalid request body

---

### 1.2 Get Memory

**GET** `/memory/{memory_id}`

获取单条记忆详情

**Path Parameters**:
- `memory_id`: string (required) - 记忆ID

**Response**:
```json
{
  "memory": {
    "id": "string",
    "content": "string",
    "importance": "number",
    "tags": ["string"],
    "created_at": "string",
    "access_count": "number",
    "score": "number"
  }
}
```

**Error Codes**:
- `404`: Memory not found

---

### 1.3 List Memories

**GET** `/memory`

获取记忆列表

**Query Parameters**:
- `limit`: number (optional) - 返回数量, default: 20

**Response**:
```json
{
  "memories": [
    {
      "id": "string",
      "content": "string",
      "importance": "number",
      "tags": ["string"],
      "created_at": "string",
      "access_count": "number",
      "score": "number"
    }
  ]
}
```

---

### 1.4 Search Memories

**GET** `/memory/search/{query}`

搜索记忆

**Path Parameters**:
- `query`: string (required) - 搜索关键词

**Query Parameters**:
- `limit`: number (optional) - 返回数量, default: 10

**Response**:
```json
{
  "query": "string",
  "memories": [
    {
      "id": "string",
      "content": "string",
      "score": "number"
    }
  ]
}
```

---

### 1.5 Get Important Memories

**GET** `/memory/important`

获取重要记忆

**Query Parameters**:
- `limit`: number (optional) - 返回数量, default: 20

**Response**:
```json
{
  "memories": [
    {
      "id": "string",
      "content": "string",
      "score": "number"
    }
  ]
}
```

---

### 1.6 Get Memory Stats

**GET** `/memory/stats`

获取记忆统计信息

**Response**:
```json
{
  "total_count": "number",
  "important_count": "number",
  "avg_importance": "number",
  "total_access_count": "number"
}
```

---

### 1.7 Update Memory

**PATCH** `/memory/{memory_id}`

更新记忆

**Path Parameters**:
- `memory_id`: string (required)

**Request Body**:
```json
{
  "importance": "number (optional)",
  "tags": ["string"] (optional)
}
```

**Response**:
```json
{
  "memory": {
    "id": "string",
    "content": "string",
    "importance": "number",
    "tags": ["string"]
  },
  "status": "updated"
}
```

---

### 1.8 Delete Memory

**DELETE** `/memory/{memory_id}`

删除记忆

**Path Parameters**:
- `memory_id`: string (required)

**Response**:
```json
{
  "status": "deleted"
}
```

**Error Codes**:
- `404`: Memory not found

---

## 2. Brain API

### 2.1 Reason

**POST** `/brain/reason`

推理引擎

**Request Body**:
```json
{
  "context": "string (required) - 上下文",
  "question": "string (required) - 问题"
}
```

**Response**:
```json
{
  "thought": "string - 推理过程",
  "answer": "string - 答案",
  "confidence": "number - 置信度"
}
```

---

### 2.2 Chain of Thought

**POST** `/brain/think`

链式思考

**Query Parameters**:
- `problem`: string (required) - 问题
- `steps`: number (optional) - 思考步骤数, default: 5

**Response**:
```json
{
  "problem": "string",
  "thoughts": ["string"]
}
```

---

### 2.3 Deduce

**POST** `/brain/deduce`

逻辑推演

**Query Parameters**:
- `premise`: string (required) - 前提
- `hypothesis`: string (required) - 假设

**Response**:
```json
{
  "premise": "string",
  "hypothesis": "string",
  "valid": "boolean",
  "explanation": "string"
}
```

---

### 2.4 Get Context

**GET** `/brain/context`

获取大脑上下文摘要

**Response**:
```json
{
  "summary": "string"
}
```

---

## 3. Planner API

### 3.1 Create Plan

**POST** `/planner/plan`

创建计划

**Request Body**:
```json
{
  "goal": "string (required) - 目标",
  "description": "string (optional) - 描述"
}
```

**Response**:
```json
{
  "plan": {
    "id": "string",
    "goal": "string",
    "description": "string",
    "milestones": [
      {
        "id": "string",
        "title": "string",
        "tasks": [
          {
            "id": "string",
            "title": "string",
            "status": "pending|running|completed",
            "priority": "number"
          }
        ],
        "progress": "number"
      }
    ],
    "created_at": "string"
  },
  "status": "created"
}
```

---

### 3.2 Get Plan

**GET** `/planner/plan/{plan_id}`

获取计划详情

**Path Parameters**:
- `plan_id`: string (required)

**Response**:
```json
{
  "plan": {
    "id": "string",
    "goal": "string",
    "milestones": [...],
    "created_at": "string"
  }
}
```

**Error Codes**:
- `404`: Plan not found

---

### 3.3 List Plans

**GET** `/planner/plans`

获取所有计划

**Response**:
```json
{
  "plans": [
    {
      "id": "string",
      "goal": "string",
      "progress": "number",
      "created_at": "string"
    }
  ]
}
```

---

### 3.4 Complete Task

**POST** `/planner/complete-task`

完成任务

**Request Body**:
```json
{
  "plan_id": "string (required)",
  "task_id": "string (required)"
}
```

**Response**:
```json
{
  "status": "completed"
}
```

**Error Codes**:
- `404`: Plan or task not found

---

### 3.5 Delete Plan

**DELETE** `/planner/plan/{plan_id}`

删除计划

**Path Parameters**:
- `plan_id`: string (required)

**Response**:
```json
{
  "status": "deleted"
}
```

**Error Codes**:
- `404`: Plan not found

---

## 4. Skills API

### 4.1 List Skills

**GET** `/skills`

获取所有技能

**Response**:
```json
{
  "skills": [
    {
      "name": "string",
      "description": "string",
      "input_schema": {...},
      "output_schema": {...},
      "enabled": "boolean"
    }
  ]
}
```

---

### 4.2 List Enabled Skills

**GET** `/skills/enabled`

获取启用的技能

**Response**:
```json
{
  "skills": [...]
}
```

---

### 4.3 Execute Skill

**POST** `/skills/execute`

执行技能

**Request Body**:
```json
{
  "skill_name": "string (required)",
  "params": {...} (required)
}
```

**Response**:
```json
{
  "result": {...},
  "status": "success",
  "skill_used": "string"
}
```

**Error Codes**:
- `400`: Skill not found or disabled

---

### 4.4 Get Skill

**GET** `/skills/{skill_name}`

获取技能详情

**Path Parameters**:
- `skill_name`: string (required)

**Response**:
```json
{
  "skill": {
    "name": "string",
    "description": "string",
    "input_schema": {...},
    "output_schema": {...},
    "enabled": "boolean"
  }
}
```

**Error Codes**:
- `404`: Skill not found

---

## 5. Knowledge Graph API

### 5.1 Get Relation Types

**GET** `/knowledge/relation-types`

获取所有关系类型

**Response**:
```json
{
  "relation_types": ["KNOWS", "LIKES", "BELONGS_TO", ...]
}
```

---

### 5.2 Create Entity

**POST** `/knowledge/entity`

创建实体

**Request Body**:
```json
{
  "name": "string (required)",
  "entity_type": "string (optional) - default: concept",
  "description": "string (optional)",
  "properties": {...} (optional),
  "memory_id": "string (optional)"
}
```

**Response**:
```json
{
  "entity": {
    "id": "string",
    "name": "string",
    "entity_type": "string",
    "description": "string",
    "properties": {...},
    "memory_id": "string",
    "created_at": "string"
  },
  "status": "created"
}
```

---

### 5.3 Get Entity

**GET** `/knowledge/entity/{entity_id}`

获取实体详情

**Path Parameters**:
- `entity_id`: string (required)

**Response**:
```json
{
  "entity": {
    "id": "string",
    "name": "string",
    "entity_type": "string",
    "description": "string"
  }
}
```

**Error Codes**:
- `404`: Entity not found

---

### 5.4 Search Entity

**GET** `/knowledge/entity/search/{name}`

搜索实体

**Path Parameters**:
- `name`: string (required)

**Response**:
```json
{
  "entity": {...}
}
```

**Error Codes**:
- `404`: Entity not found

---

### 5.5 Get Entity Neighbors

**GET** `/knowledge/entity/{entity_id}/neighbors`

获取实体邻居

**Path Parameters**:
- `entity_id`: string (required)

**Query Parameters**:
- `depth`: number (optional) - default: 1
- `relation_type`: string (optional)

**Response**:
```json
{
  "entity_id": "string",
  "neighbors": [
    [
      {"entity": {...}},
      {"relation": {...}}
    ]
  ]
}
```

---

### 5.6 Create Relation

**POST** `/knowledge/relation`

创建关系

**Request Body**:
```json
{
  "from_entity_id": "string (required)",
  "to_entity_id": "string (required)",
  "relation_type": "string (required)",
  "weight": "number (optional) - default: 1.0",
  "properties": {...} (optional)
}
```

**Response**:
```json
{
  "relation": {
    "id": "string",
    "from_entity_id": "string",
    "to_entity_id": "string",
    "relation_type": "string",
    "weight": "number",
    "created_at": "string"
  },
  "status": "created"
}
```

**Error Codes**:
- `400`: Failed to create relation

---

### 5.7 Get Entity Relations

**GET** `/knowledge/entity/{entity_id}/relations`

获取实体关系

**Path Parameters**:
- `entity_id`: string (required)

**Query Parameters**:
- `relation_type`: string (optional)

**Response**:
```json
{
  "relations": [
    {
      "id": "string",
      "from_entity_id": "string",
      "to_entity_id": "string",
      "relation_type": "string",
      "weight": "number"
    }
  ]
}
```

---

### 5.8 Query Knowledge

**GET** `/knowledge/query`

查询知识图谱

**Query Parameters**:
- `entity_name`: string (optional)
- `entity_type`: string (optional)
- `relation_type`: string (optional)

**Response**:
```json
{
  "entities": [...],
  "relations": [...]
}
```

---

### 5.9 Get Knowledge Stats

**GET** `/knowledge/stats`

获取知识图谱统计

**Response**:
```json
{
  "entity_count": "number",
  "relation_count": "number",
  "relation_type_counts": {...}
}
```

---

### 5.10 Delete Entity

**DELETE** `/knowledge/entity/{entity_id}`

删除实体

**Path Parameters**:
- `entity_id`: string (required)

**Response**:
```json
{
  "status": "deleted"
}
```

**Error Codes**:
- `404`: Entity not found

---

### 5.11 Extract from Text

**POST** `/knowledge/extract`

从文本提取实体和关系

**Query Parameters**:
- `text`: string (required)

**Response**:
```json
{
  "entities": [...],
  "relations": [...]
}
```

---

### 5.12 Export Cypher

**GET** `/knowledge/cypher`

导出 Cypher 语句

**Response**:
```json
{
  "statements": ["CREATE ..."]
}
```

---

## 6. Learning API

### 6.1 Add Experience

**POST** `/learning/experience`

添加学习经验

**Request Body**:
```json
{
  "task": "string (required)",
  "result": "string (required)",
  "time_taken": "string (required)",
  "lesson": "string (required)",
  "category": "string (optional) - default: general",
  "tags": ["string"] (optional),
  "success": "boolean (optional) - default: true",
  "difficulty": "number (optional) - default: 3"
}
```

**Response**:
```json
{
  "experience": {
    "id": "string",
    "task": "string",
    "result": "string",
    "time_taken": "string",
    "lesson": "string",
    "category": "string",
    "tags": ["string"],
    "success": "boolean",
    "difficulty": "number",
    "created_at": "string"
  },
  "status": "created"
}
```

---

### 6.2 Get Experience

**GET** `/learning/experience/{exp_id}`

获取经验详情

**Path Parameters**:
- `exp_id`: string (required)

**Response**:
```json
{
  "experience": {...}
}
```

**Error Codes**:
- `404`: Experience not found

---

### 6.3 List Experiences

**GET** `/learning/experiences`

获取经验列表

**Query Parameters**:
- `limit`: number (optional) - default: 20

**Response**:
```json
{
  "experiences": [...]
}
```

---

### 6.4 Get by Category

**GET** `/learning/experiences/category/{category}`

按类别获取经验

**Path Parameters**:
- `category`: string (required)

**Response**:
```json
{
  "category": "string",
  "experiences": [...]
}
```

---

### 6.5 Get by Tags

**GET** `/learning/experiences/tags/{tags}`

按标签获取经验

**Path Parameters**:
- `tags`: string (required) - 逗号分隔

**Response**:
```json
{
  "tags": ["string"],
  "experiences": [...]
}
```

---

### 6.6 Get Lessons

**GET** `/learning/lessons`

获取学到的教训

**Query Parameters**:
- `limit`: number (optional) - default: 10

**Response**:
```json
{
  "lessons": ["string"]
}
```

---

### 6.7 Get Suggestions

**GET** `/learning/suggestions/{task}`

获取任务建议

**Path Parameters**:
- `task`: string (required)

**Response**:
```json
{
  "task": "string",
  "suggestions": ["string"]
}
```

---

### 6.8 Get Patterns

**GET** `/learning/patterns`

获取学习模式

**Response**:
```json
{
  "patterns": [
    {
      "id": "string",
      "pattern": "string",
      "frequency": "number"
    }
  ]
}
```

---

### 6.9 Get Growth Report

**GET** `/learning/growth-report`

获取成长报告

**Response**:
```json
{
  "total_experiences": "number",
  "success_rate": "number",
  "average_difficulty": "number",
  "top_categories": ["string"],
  "skills_gained": ["string"],
  "learning_trend": "improving|stable|declining"
}
```

---

### 6.10 Provide Feedback

**GET** `/learning/feedback/{exp_id}`

提供反馈

**Path Parameters**:
- `exp_id`: string (required)

**Query Parameters**:
- `feedback`: string (required)
- `rating`: number (optional) - default: 5

**Response**:
```json
{
  "experience": {...},
  "status": "updated"
}
```

**Error Codes**:
- `404`: Experience not found

---

## 7. Digital Twin API

### 7.1 Get Profile

**GET** `/digital-twin/profile`

获取数字分身配置

**Response**:
```json
{
  "profile": {
    "name": "string",
    "writing_style": {
      "formal_level": "number",
      "tone": "string"
    },
    "code_style": {
      "naming_convention": "string"
    },
    "interests": ["string"],
    "strengths": ["string"],
    "weaknesses": ["string"],
    "created_at": "string"
  }
}
```

---

### 7.2 Initialize Twin

**POST** `/digital-twin/initialize`

初始化数字分身

**Query Parameters**:
- `name`: string (optional) - default: "My Digital Twin"

**Response**:
```json
{
  "status": "initialized",
  "profile": {...}
}
```

---

### 7.3 Update Writing Style

**PATCH** `/digital-twin/writing-style`

更新写作风格

**Request Body**:
```json
{
  "writing_formal_level": "number (optional)",
  "writing_tone": "string (optional)"
}
```

**Response**:
```json
{
  "status": "updated",
  "profile": {...}
}
```

---

### 7.4 Add Writing Sample

**POST** `/digital-twin/writing-samples`

添加写作样本

**Query Parameters**:
- `sample`: string (required)

**Response**:
```json
{
  "status": "updated"
}
```

---

### 7.5 Update Code Style

**PATCH** `/digital-twin/code-style`

更新代码风格

**Request Body**:
```json
{
  "code_naming_convention": "string (optional)"
}
```

**Response**:
```json
{
  "status": "updated",
  "profile": {...}
}
```

---

### 7.6 Add Code Sample

**POST** `/digital-twin/code-samples`

添加代码样本

**Query Parameters**:
- `sample`: string (required)
- `language`: string (optional) - default: python

**Response**:
```json
{
  "status": "updated"
}
```

---

### 7.7 Update Interests

**POST** `/digital-twin/interests`

更新兴趣

**Query Parameters**:
- `interests`: ["string"] (required)

**Response**:
```json
{
  "status": "updated"
}
```

---

### 7.8 Update Strengths/Weaknesses

**POST** `/digital-twin/strengths-weaknesses`

更新优势和劣势

**Request Body**:
```json
{
  "strengths": ["string"] (optional),
  "weaknesses": ["string"] (optional)
}
```

**Response**:
```json
{
  "status": "updated"
}
```

---

### 7.9 Record Decision

**POST** `/digital-twin/decision`

记录决策

**Query Parameters**:
- `situation`: string (required)
- `decision`: string (required)
- `reasoning`: string (required)
- `outcome`: string (required)

**Response**:
```json
{
  "status": "recorded"
}
```

---

### 7.10 Suggest Decision

**GET** `/digital-twin/decision/{situation}`

获取决策建议

**Path Parameters**:
- `situation`: string (required)

**Response**:
```json
{
  "situation": "string",
  "suggestion": "string"
}
```

---

### 7.11 Get Response Style

**GET** `/digital-twin/response-style/{context}`

获取响应风格

**Path Parameters**:
- `context`: string (required)

**Response**:
```json
{
  "context": "string",
  "style": {
    "formal_level": "number",
    "tone": "string"
  }
}
```

---

### 7.12 Get Learning Recommendations

**GET** `/digital-twin/learning-recommendations`

获取学习建议

**Response**:
```json
{
  "recommendations": ["string"]
}
```

---

### 7.13 Get Interests Overview

**GET** `/digital-twin/interests-overview`

获取兴趣概览

**Response**:
```json
{
  "interests": ["string"],
  "interest_scores": {...}
}
```

---

## 8. RAG API

### 8.1 Query RAG

**POST** `/rag/query`

查询RAG

**Request Body**:
```json
{
  "question": "string (required)",
  "top_k": "number (optional) - default: 5",
  "use_rerank": "boolean (optional) - default: true",
  "use_hybrid": "boolean (optional) - default: true",
  "include_citations": "boolean (optional) - default: true"
}
```

**Response**:
```json
{
  "answer": "string",
  "context": "string",
  "citations": [
    {
      "index": "number",
      "source": "string",
      "content": "string",
      "relevance_score": "number"
    }
  ],
  "sources": ["string"],
  "total_results": "number"
}
```

---

### 8.2 Add Text

**POST** `/rag/add-text`

添加文本

**Request Body**:
```json
{
  "text": "string (required)",
  "source": "string (optional) - default: user_input",
  "metadata": {...} (optional),
  "chunk_size": "number (optional) - default: 500",
  "overlap": "number (optional) - default: 50"
}
```

**Response**:
```json
{
  "status": "added",
  "chunks_created": "number",
  "chunks": [...]
}
```

---

### 8.3 Add Document

**POST** `/rag/add-document`

添加文档

**Request Body**:
```json
{
  "title": "string (required)",
  "content": "string (required)",
  "source_type": "string (optional) - default: markdown",
  "metadata": {...} (optional)
}
```

**Response**:
```json
{
  "status": "added",
  "document": {...}
}
```

---

### 8.4 Search RAG

**GET** `/rag/search`

搜索RAG

**Query Parameters**:
- `query`: string (required)
- `top_k`: number (optional) - default: 10

**Response**:
```json
{
  "query": "string",
  "results": [
    {
      "content": "string",
      "source": "string",
      "score": "number",
      "highlights": ["string"]
    }
  ]
}
```

---

### 8.5 Get RAG Stats

**GET** `/rag/stats`

获取RAG统计

**Response**:
```json
{
  "retrieval_stats": {...},
  "reranker_model": "string",
  "context_max_tokens": "number"
}
```

---

### 8.6 Delete by Source

**DELETE** `/rag/delete/{source}`

按来源删除

**Path Parameters**:
- `source`: string (required)

**Response**:
```json
{
  "status": "deleted",
  "chunks_deleted": "number"
}
```

---

## 9. Agent API

### 9.1 List Agent Skills

**GET** `/agent/skills`

获取代理技能

**Response**:
```json
{
  "skills": [...]
}
```

---

### 9.2 Create Task

**POST** `/agent/task`

创建任务

**Request Body**:
```json
{
  "name": "string (required)",
  "task_type": "string (optional) - default: general",
  "input_data": {...} (optional),
  "priority": "number (optional) - default: 2",
  "dependencies": ["string"] (optional)
}
```

**Response**:
```json
{
  "task": {
    "id": "string",
    "name": "string",
    "task_type": "string",
    "status": "pending",
    "priority": "number",
    "created_at": "string"
  },
  "status": "created"
}
```

---

### 9.3 Execute Task

**POST** `/agent/execute/{task_id}`

执行任务

**Path Parameters**:
- `task_id`: string (required)

**Response**:
```json
{
  "task": {...},
  "status": "completed|failed"
}
```

---

### 9.4 Get Task

**GET** `/agent/task/{task_id}`

获取任务详情

**Path Parameters**:
- `task_id`: string (required)

**Response**:
```json
{
  "task": {...}
}
```

**Error Codes**:
- `404`: Task not found

---

### 9.5 List Tasks

**GET** `/agent/tasks`

获取任务列表

**Query Parameters**:
- `status`: string (optional) - pending|running|completed|failed

**Response**:
```json
{
  "tasks": [...]
}
```

---

### 9.6 Create Workflow

**POST** `/agent/workflow`

创建工作流

**Request Body**:
```json
{
  "name": "string (required)",
  "description": "string (optional)"
}
```

**Response**:
```json
{
  "workflow": {
    "id": "string",
    "name": "string",
    "description": "string",
    "tasks": [],
    "created_at": "string",
    "status": "created"
  },
  "status": "created"
}
```

---

### 9.7 Add Task to Workflow

**POST** `/agent/workflow/{workflow_id}/add-task/{task_id}`

添加任务到工作流

**Path Parameters**:
- `workflow_id`: string (required)
- `task_id`: string (required)

**Response**:
```json
{
  "status": "added"
}
```

**Error Codes**:
- `404`: Workflow or task not found

---

### 9.8 Execute Workflow

**POST** `/agent/workflow/{workflow_id}/execute`

执行工作流

**Path Parameters**:
- `workflow_id`: string (required)

**Response**:
```json
{
  "workflow": {...},
  "results": {...},
  "status": "completed|failed"
}
```

---

### 9.9 List Workflows

**GET** `/agent/workflows`

获取工作流列表

**Response**:
```json
{
  "workflows": [...]
}
```

---

### 9.10 Get Workflow

**GET** `/agent/workflow/{workflow_id}`

获取工作流详情

**Path Parameters**:
- `workflow_id`: string (required)

**Response**:
```json
{
  "workflow": {...}
}
```

**Error Codes**:
- `404`: Workflow not found

---

### 9.11 Get Execution History

**GET** `/agent/history`

获取执行历史

**Query Parameters**:
- `limit`: number (optional) - default: 50

**Response**:
```json
{
  "history": [
    {
      "task_id": "string",
      "task_name": "string",
      "status": "string",
      "timestamp": "string",
      "output": {...}
    }
  ]
}
```

---

## 10. Reflection API

### 10.1 Reflect

**POST** `/reflection/reflect`

创建反思

**Request Body**:
```json
{
  "task_id": "string (required)",
  "task_name": "string (required)",
  "what_happened": "string (required)",
  "what_went_well": ["string"] (optional),
  "what_could_improve": ["string"] (optional),
  "mistakes": ["string"] (optional),
  "lessons_learned": ["string"] (optional),
  "confidence_level": "number (optional) - default: 3"
}
```

**Response**:
```json
{
  "reflection": {
    "id": "string",
    "task_id": "string",
    "task_name": "string",
    "what_happened": "string",
    "what_went_well": ["string"],
    "what_could_improve": ["string"],
    "mistakes": ["string"],
    "lessons_learned": ["string"],
    "confidence_level": "number",
    "created_at": "string"
  },
  "status": "created"
}
```

---

### 10.2 Get Reflection

**GET** `/reflection/{reflection_id}`

获取反思

**Path Parameters**:
- `reflection_id`: string (required)

**Response**:
```json
{
  "reflection": {...}
}
```

**Error Codes**:
- `404`: Reflection not found

---

### 10.3 Get Recent Reflections

**GET** `/reflection/recent`

获取最近反思

**Query Parameters**:
- `limit`: number (optional) - default: 20

**Response**:
```json
{
  "reflections": [...]
}
```

---

### 10.4 Get Pending Improvements

**GET** `/reflection/improvements/pending`

获取待改进项

**Query Parameters**:
- `limit`: number (optional) - default: 10

**Response**:
```json
{
  "improvements": [
    {
      "id": "string",
      "reflection_id": "string",
      "original_mistake": "string",
      "improvement_action": "string",
      "expected_outcome": "string",
      "status": "pending",
      "created_at": "string"
    }
  ]
}
```

---

### 10.5 Apply Improvement

**POST** `/reflection/improvement/apply`

应用改进

**Request Body**:
```json
{
  "improvement_id": "string (required)",
  "actual_outcome": "string (required)",
  "success": "boolean (required)"
}
```

**Response**:
```json
{
  "status": "updated"
}
```

**Error Codes**:
- `404`: Improvement not found

---

### 10.6 Get Suggestions

**GET** `/reflection/suggestions/{task_name}`

获取建议

**Path Parameters**:
- `task_name`: string (required)

**Response**:
```json
{
  "task_name": "string",
  "suggestions": ["string"]
}
```

---

### 10.7 Get Growth Report

**GET** `/reflection/growth-report`

获取成长报告

**Response**:
```json
{
  "metrics": {
    "total_reflections": "number",
    "total_improvements": "number",
    "successful_improvements": "number",
    "common_mistakes": ["string"],
    "top_lessons": ["string"],
    "improvement_rate": "number",
    "confidence_trend": ["number"]
  },
  "trend_direction": "improving|stable|declining",
  "suggestions": ["string"]
}
```

---

### 10.8 Delete Reflection

**DELETE** `/reflection/{reflection_id}`

删除反思

**Path Parameters**:
- `reflection_id`: string (required)

**Response**:
```json
{
  "status": "deleted"
}
```

**Error Codes**:
- `404`: Reflection not found

---

## 11. Knowledge Base API

### 11.1 Add Markdown

**POST** `/knowledge-base/markdown`

添加Markdown文档

**Request Body**:
```json
{
  "content": "string (required)",
  "title": "string (optional)",
  "metadata": {...} (optional)
}
```

**Response**:
```json
{
  "status": "added",
  "document": {...}
}
```

---

### 11.2 Add Text

**POST** `/knowledge-base/text`

添加文本文档

**Request Body**:
```json
{
  "content": "string (required)",
  "title": "string (optional)",
  "metadata": {...} (optional)
}
```

**Response**:
```json
{
  "status": "added",
  "document": {...}
}
```

---

### 11.3 Add Web Content

**POST** `/knowledge-base/web`

添加网页内容

**Request Body**:
```json
{
  "url": "string (required)",
  "content": "string (required)",
  "title": "string (optional)"
}
```

**Response**:
```json
{
  "status": "added",
  "document": {...}
}
```

---

### 11.4 Query KB

**GET** `/knowledge-base/query`

查询知识库

**Query Parameters**:
- `question`: string (required)
- `top_k`: number (optional) - default: 5

**Response**:
```json
{
  "answer": "string",
  "context": "string",
  "citations": [...]
}
```

---

### 11.5 Search KB

**GET** `/knowledge-base/search`

搜索知识库

**Query Parameters**:
- `query`: string (required)
- `top_k`: number (optional) - default: 10

**Response**:
```json
{
  "query": "string",
  "results": [...]
}
```

---

### 11.6 List Documents

**GET** `/knowledge-base/documents`

获取文档列表

**Response**:
```json
{
  "documents": [
    {
      "id": "string",
      "title": "string",
      "source_type": "string",
      "chunk_count": "number",
      "created_at": "string"
    }
  ]
}
```

---

### 11.7 Get Document

**GET** `/knowledge-base/document/{doc_id}`

获取文档详情

**Path Parameters**:
- `doc_id`: string (required)

**Response**:
```json
{
  "document": {...}
}
```

**Error Codes**:
- `404`: Document not found

---

### 11.8 Delete Document

**DELETE** `/knowledge-base/document/{doc_id}`

删除文档

**Path Parameters**:
- `doc_id`: string (required)

**Response**:
```json
{
  "status": "deleted"
}
```

**Error Codes**:
- `404`: Document not found

---

### 11.9 Get KB Stats

**GET** `/knowledge-base/stats`

获取知识库统计

**Response**:
```json
{
  "total_documents": "number",
  "total_chunks": "number",
  "source_types": {...},
  "rag_stats": {...}
}
```

---

## 12. Health Check

### 12.1 Health Check

**GET** `/health`

健康检查

**Response**:
```json
{
  "status": "healthy",
  "version": "0.3.0",
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
    "knowledge_base": "active"
  }
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## Version

API Version: 0.3.0
