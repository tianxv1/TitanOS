# TitanOS Architecture

## System Overview

TitanOS is a personal AI operating system designed to simulate human cognitive architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│              (Web Chat / API / Future Mobile App)                │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         GATEWAY LAYER                           │
│                    (FastAPI + CORS + Auth)                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      COGNITIVE ENGINE                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Brain   │  │  Planner │  │  Agent   │  │   RAG    │        │
│  │Reasoning │  │  Task    │  │ Runtime  │  │  Engine  │        │
│  │  Engine  │  │ Planner  │  │Executor  │  │Retrieval │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ Learning │  │Reflection│  │Digital   │  │  Goal    │        │
│  │ Engine   │  │ System   │  │Twin      │  │ Engine   │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       MEMORY LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Memory  │  │Knowledge │  │Personal  │  │ Vector   │        │
│  │  Engine  │  │  Graph   │  │Knowledge │  │  Store   │        │
│  │(JSON/SQL)│  │ (Neo4j)  │  │  Base    │  │(Milvus)  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Modules

### 1. Memory Engine

**Purpose**: Simulates human memory with forgetting mechanism

**Location**: `backend/memory/`

**Components**:
- `memory_node.py` - Memory data structure
- `memory_score.py` - Scoring algorithm
- `memory_engine.py` - Core memory operations

**Algorithm**:
```
score = importance × 0.6 + access_count × 0.3 + recent_score × 0.1

If score < threshold:
    Delete memory  # Automatic forgetting
```

**Storage**: JSON files (MVP), PostgreSQL (Production)

---

### 2. Brain (Reasoning Engine)

**Purpose**: Provides reasoning and analysis capabilities

**Location**: `backend/brain/`

**Features**:
- Question analysis
- Chain of Thought reasoning
- Logical deduction
- Problem decomposition

---

### 3. Planner

**Purpose**: Automatic task decomposition

**Location**: `backend/planner/`

**Data Model**:
```
Plan
├── Goal
├── Milestones[]
│   ├── Tasks[]
│   └── Progress
└── Deadline

Task
├── Title
├── Status (pending/running/completed)
├── Priority (1-5)
└── Dependencies
```

**Built-in Templates**:
- Exam preparation
- Learning plans
- Career development
- Project management
- Health/fitness

---

### 4. RAG Engine

**Purpose**: Retrieval-Augmented Generation pipeline

**Location**: `backend/rag/`

**Pipeline**:
```
Query
  │
  ▼
┌─────────────────┐
│ Embedding       │ ← Text → Vector
└─────────────────┘
  │
  ▼
┌─────────────────┐
│ Vector Search   │ ← Top-K retrieval
└─────────────────┘
  │
  ▼
┌─────────────────┐
│ Reranker        │ ← Relevance scoring
└─────────────────┘
  │
  ▼
┌─────────────────┐
│ Context Builder │ ← Prompt construction
└─────────────────┘
  │
  ▼
LLM → Answer
```

**Components**:
- `embedding.py` - Embedding service
- `retrieval.py` - Retrieval engine
- `reranker.py` - Re-ranking
- `rag_engine.py` - Main orchestration

---

### 5. Agent Runtime

**Purpose**: Task execution engine

**Location**: `backend/agent/`

**Architecture**:
```
Agent Runtime
├── Task Registry
├── Skill Registry
│   ├── Search Skill
│   ├── Code Skill
│   ├── Analyze Skill
│   └── Summarize Skill
├── Workflow Engine
└── Scheduler
```

**Execution Flow**:
```
Task Created
    │
    ▼
Check Dependencies
    │
    ├── Yes → Wait
    │
    └── No → Execute
              │
              ▼
          Skill Handler
              │
              ▼
          Task Complete
```

---

### 6. Reflection System

**Purpose**: Learning from experience

**Location**: `backend/reflection/`

**Process**:
```
Task Completed
    │
    ▼
What happened?
    │
    ▼
What went well?
    │
    ▼
What could improve?
    │
    ▼
Mistakes identified
    │
    ▼
Improvements generated
    │
    ▼
Feedback to Planner/Agent
```

**Benefits**:
- Continuous improvement
- Mistake tracking
- Strategy optimization

---

### 7. Knowledge Graph

**Purpose**: Structured knowledge representation

**Location**: `backend/knowledge_graph/`

**Model**:
```
(Entity) -[Relation]-> (Entity)

Example:
(张三) -[喜欢]-> (机器学习)
(机器学习) -[属于]-> (人工智能)
(人工智能) -[研究]-> (深度学习)
```

**Relation Types**: 12 predefined types (KNOWS, LIKES, BELONGS_TO, etc.)

---

### 8. Learning Engine

**Purpose**: Experience-based growth

**Location**: `backend/learning/`

**Features**:
- Experience storage
- Pattern extraction
- Growth metrics
- Strategy suggestions

---

### 9. Digital Twin

**Purpose**: User profile and personalization

**Location**: `backend/digital_twin/`

**Components**:
- Writing style profile
- Code style profile
- Decision patterns
- Learning habits
- Personality traits

---

## Data Flow

### Query Flow
```
User Query
    │
    ▼
Gateway (Auth + Rate Limit)
    │
    ▼
Brain (Analyze intent)
    │
    ▼
Planner (If planning needed)
    │
    ▼
RAG Engine (If retrieval needed)
    │
    ▼
Agent Runtime (If execution needed)
    │
    ▼
Memory/Learning (Update knowledge)
    │
    ▼
Response to User
```

### Task Execution Flow
```
Goal Definition
    │
    ▼
Planner (Decompose to tasks)
    │
    ▼
Agent Runtime
    │
    ▼
For each task:
    │
    ├─→ Check dependencies
    │
    ├─→ Execute via Skill
    │
    ├─→ Store result
    │
    └─→ Trigger Reflection
    │
    ▼
Reflection (Learn from execution)
    │
    ▼
Update Digital Twin
    │
    ▼
Goal Complete
```

---

## API Design

### RESTful Endpoints

```
/memory/
├── POST   /memory/              # Add memory
├── GET    /memory/              # List memories
├── GET    /memory/{id}          # Get memory
├── GET    /memory/search/{q}    # Search
└── DELETE /memory/{id}          # Delete

/brain/
├── POST   /brain/reason         # Reasoning
└── POST   /brain/think          # Chain of thought

/planner/
├── POST   /planner/plan         # Create plan
├── GET    /planner/plans        # List plans
└── POST   /planner/complete     # Complete task

/rag/
├── POST   /rag/query             # RAG query
└── POST   /rag/add               # Add to knowledge base

/agent/
├── POST   /agent/task            # Create task
├── POST   /agent/execute/{id}    # Execute task
└── GET    /agent/workflows       # List workflows

/learning/
├── POST   /learning/experience   # Add experience
└── GET    /learning/growth       # Get growth report

/reflection/
├── POST   /reflection/reflect   # Create reflection
└── GET    /reflection/report     # Get growth metrics
```

---

## Scalability Considerations

### Current (MVP)
- JSON file storage
- In-memory vector store
- Single-threaded execution

### Production Ready
- PostgreSQL + Redis for memory
- Milvus for vector search
- Neo4j for knowledge graphs
- Kubernetes for orchestration
- Celery for async task execution

---

## Security

- Input validation on all endpoints
- Rate limiting
- CORS configuration
- Sanitization of user inputs

---

## Future Architecture (v3.0)

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS AI AGENT                          │
├─────────────────────────────────────────────────────────────────┤
│  Self-Directed Learning    │    Creative Problem Solving        │
│  ├─ Identify knowledge gaps│    ├─ Novel solution generation    │
│  ├─ Acquire new skills    │    ├─ Cross-domain reasoning       │
│  └─ Update goals          │    └─ Innovation generation        │
├─────────────────────────────────────────────────────────────────┤
│  Long-Term Memory         │    Emotional Intelligence           │
│  ├─ Persistent storage    │    ├─ User mood detection           │
│  ├─ Knowledge consolidation│    ├─ Empathetic responses         │
│  └─ Lifelong learning     │    └─ Relationship building         │
└─────────────────────────────────────────────────────────────────┘
```

---

Last Updated: 2026-05-31
