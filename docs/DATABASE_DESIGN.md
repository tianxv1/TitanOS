# TitanOS Database Design

## Overview

TitanOS 使用多数据库架构来支持不同类型的数据存储需求：

| Database | Purpose | Technology |
|----------|---------|------------|
| PostgreSQL | 结构化数据存储 (Users, Memories, Plans, Tasks, Experiences, Goals) | PostgreSQL 16+ |
| Neo4j | 知识图谱存储 (Entities, Relations) | Neo4j 5.x |
| Milvus | 向量存储 (Embeddings) | Milvus 2.x |
| SQLite | 开发环境轻量级存储 | SQLite 3.x |

---

## 1. PostgreSQL Schema

### 1.1 Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    avatar_url VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

**Fields**:
- `id`: 用户唯一标识
- `username`: 用户名
- `email`: 邮箱地址
- `password_hash`: 密码哈希 (bcrypt)
- `full_name`: 全名
- `avatar_url`: 头像URL
- `is_active`: 是否激活
- `created_at`: 创建时间
- `updated_at`: 更新时间

---

### 1.2 Memories Table

```sql
CREATE TABLE memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    importance FLOAT DEFAULT 0.5,
    tags TEXT[],
    embedding_vector VECTOR(384),
    access_count INTEGER DEFAULT 0,
    score FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accessed_at TIMESTAMP,
    memory_type VARCHAR(20) DEFAULT 'episodic'  -- episodic, semantic, procedural
);

CREATE INDEX idx_memories_user_id ON memories(user_id);
CREATE INDEX idx_memories_created_at ON memories(created_at);
CREATE INDEX idx_memories_score ON memories(score);
CREATE INDEX idx_memories_type ON memories(memory_type);
```

**Fields**:
- `id`: 记忆唯一标识
- `user_id`: 所属用户
- `content`: 记忆内容
- `importance`: 重要性 (0-1)
- `tags`: 标签数组
- `embedding_vector`: 向量表示
- `access_count`: 访问次数
- `score`: 综合评分
- `created_at`: 创建时间
- `accessed_at`: 最后访问时间
- `memory_type`: 记忆类型

---

### 1.3 Plans Table

```sql
CREATE TABLE plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    goal TEXT NOT NULL,
    description TEXT,
    progress FLOAT DEFAULT 0.0,
    status VARCHAR(20) DEFAULT 'active',  -- active, completed, paused
    priority INTEGER DEFAULT 2,
    deadline TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_plans_user_id ON plans(user_id);
CREATE INDEX idx_plans_status ON plans(status);
CREATE INDEX idx_plans_priority ON plans(priority);
```

**Fields**:
- `id`: 计划唯一标识
- `user_id`: 所属用户
- `goal`: 目标描述
- `description`: 详细描述
- `progress`: 进度 (0-1)
- `status`: 状态
- `priority`: 优先级 (1-5)
- `deadline`: 截止日期
- `created_at`: 创建时间
- `updated_at`: 更新时间

---

### 1.4 Milestones Table

```sql
CREATE TABLE milestones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID NOT NULL REFERENCES plans(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    progress FLOAT DEFAULT 0.0,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_milestones_plan_id ON milestones(plan_id);
```

---

### 1.5 Tasks Table

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    milestone_id UUID REFERENCES milestones(id) ON DELETE CASCADE,
    plan_id UUID NOT NULL REFERENCES plans(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',  -- pending, running, completed, failed, cancelled
    priority INTEGER DEFAULT 2,
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_tasks_plan_id ON tasks(plan_id);
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
```

---

### 1.6 Experiences Table

```sql
CREATE TABLE experiences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    task TEXT NOT NULL,
    result TEXT NOT NULL,
    time_taken VARCHAR(50),
    lesson TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'general',
    tags TEXT[],
    success BOOLEAN DEFAULT true,
    difficulty INTEGER DEFAULT 3,
    feedback TEXT,
    rating INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_experiences_user_id ON experiences(user_id);
CREATE INDEX idx_experiences_category ON experiences(category);
CREATE INDEX idx_experiences_success ON experiences(success);
```

---

### 1.7 Goals Table

```sql
CREATE TABLE goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    parent_id UUID REFERENCES goals(id),
    goal_type VARCHAR(20) DEFAULT 'short_term',  -- short_term, long_term, career, learning, health, project
    priority INTEGER DEFAULT 2,
    progress FLOAT DEFAULT 0.0,
    status VARCHAR(20) DEFAULT 'active',
    deadline TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_goals_user_id ON goals(user_id);
CREATE INDEX idx_goals_type ON goals(goal_type);
CREATE INDEX idx_goals_parent_id ON goals(parent_id);
```

---

### 1.8 Skills Table

```sql
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    input_schema JSONB,
    output_schema JSONB,
    enabled BOOLEAN DEFAULT true,
    usage_count INTEGER DEFAULT 0,
    success_rate FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_skills_user_name ON skills(user_id, name);
```

---

### 1.9 Reflections Table

```sql
CREATE TABLE reflections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    task_id UUID,
    task_name VARCHAR(200) NOT NULL,
    what_happened TEXT NOT NULL,
    what_went_well TEXT[],
    what_could_improve TEXT[],
    mistakes TEXT[],
    lessons_learned TEXT[],
    confidence_level INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_reflections_user_id ON reflections(user_id);
CREATE INDEX idx_reflections_created_at ON reflections(created_at);
```

---

### 1.10 Improvements Table

```sql
CREATE TABLE improvements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reflection_id UUID NOT NULL REFERENCES reflections(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    original_mistake TEXT NOT NULL,
    improvement_action TEXT NOT NULL,
    expected_outcome TEXT,
    actual_outcome TEXT,
    status VARCHAR(20) DEFAULT 'pending',  -- pending, applied, success, failed
    applied_count INTEGER DEFAULT 0,
    success_rate FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    applied_at TIMESTAMP
);

CREATE INDEX idx_improvements_reflection_id ON improvements(reflection_id);
CREATE INDEX idx_improvements_user_id ON improvements(user_id);
CREATE INDEX idx_improvements_status ON improvements(status);
```

---

### 1.11 Documents Table

```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    source_type VARCHAR(20) DEFAULT 'text',  -- text, markdown, web, pdf
    source_url VARCHAR(255),
    file_path VARCHAR(255),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_documents_user_id ON documents(user_id);
CREATE INDEX idx_documents_source_type ON documents(source_type);
```

---

### 1.12 Document Chunks Table

```sql
CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding_vector VECTOR(384),
    chunk_index INTEGER DEFAULT 0,
    source VARCHAR(255),
    source_type VARCHAR(20) DEFAULT 'text',
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_chunks_document_id ON document_chunks(document_id);
```

---

## 2. Neo4j Schema

### 2.1 Entity Node

```cypher
(:Entity {
    id: "uuid",
    name: "string",
    entity_type: "string",  // person, concept, event, location, organization
    description: "string",
    properties: "map",
    memory_id: "uuid",
    created_at: "datetime",
    updated_at: "datetime"
})
```

### 2.2 Relation Types

| Relation Type | Description |
|---------------|-------------|
| KNOWS | 知道/了解 |
| LIKES | 喜欢 |
| BELONGS_TO | 属于 |
| PART_OF | 部分 |
| CAUSES | 导致 |
| FOLLOWS | 跟随 |
| USES | 使用 |
| CREATED_BY | 由...创建 |
| LOCATED_AT | 位于 |
| WORKS_AT | 工作于 |
| STUDIES_AT | 学习于 |
| INTERESTED_IN | 对...感兴趣 |

### 2.3 Relation Properties

```cypher
-[RELATION_TYPE {
    id: "uuid",
    weight: "float",
    properties: "map",
    created_at: "datetime"
}]->
```

### 2.4 KnowledgeNode

```cypher
(:KnowledgeNode {
    id: "uuid",
    content: "string",
    category: "string",
    source: "string",
    confidence: "float",
    created_at: "datetime"
})
```

### 2.5 MemoryNode

```cypher
(:MemoryNode {
    id: "uuid",
    content: "string",
    importance: "float",
    access_count: "integer",
    score: "float",
    memory_type: "string",
    created_at: "datetime",
    accessed_at: "datetime"
})
```

---

## 3. Milvus Schema

### 3.1 Collection: memory_embeddings

| Field | Type | Description |
|-------|------|-------------|
| id | Primary key | 唯一标识 |
| user_id | VARCHAR | 用户ID |
| memory_id | VARCHAR | 记忆ID |
| embedding | FLOAT_VECTOR(384) | 向量 |
| content | VARCHAR | 内容摘要 |
| created_at | VARCHAR | 创建时间 |

### 3.2 Collection: document_embeddings

| Field | Type | Description |
|-------|------|-------------|
| id | Primary key | 唯一标识 |
| user_id | VARCHAR | 用户ID |
| document_id | VARCHAR | 文档ID |
| chunk_id | VARCHAR | 块ID |
| embedding | FLOAT_VECTOR(384) | 向量 |
| content | VARCHAR | 内容 |
| source | VARCHAR | 来源 |
| created_at | VARCHAR | 创建时间 |

### 3.3 Collection: experience_embeddings

| Field | Type | Description |
|-------|------|-------------|
| id | Primary key | 唯一标识 |
| user_id | VARCHAR | 用户ID |
| experience_id | VARCHAR | 经验ID |
| embedding | FLOAT_VECTOR(384) | 向量 |
| lesson | VARCHAR | 学到的教训 |
| category | VARCHAR | 类别 |
| created_at | VARCHAR | 创建时间 |

---

## 4. Entity Relationship Diagram

```
User
├── has_many ──→ Memory
├── has_many ──→ Plan
│   ├── has_many ──→ Milestone
│   │   └── has_many ──→ Task
├── has_many ──→ Experience
├── has_many ──→ Goal
│   └── has_many ──→ Goal (sub-goals)
├── has_many ──→ Reflection
│   └── has_many ──→ Improvement
├── has_many ──→ Document
│   └── has_many ──→ DocumentChunk
└── has_many ──→ Skill

Memory ←──→ KnowledgeGraph (via Neo4j)
Embedding ←──→ VectorStore (via Milvus)
```

---

## 5. Data Flow

```
User Input
    │
    ├─→ PostgreSQL (Structured Data)
    │       ├─→ User
    │       ├─→ Memory
    │       ├─→ Plan/Task
    │       ├─→ Experience
    │       └─→ Goal
    │
    ├─→ Neo4j (Graph Data)
    │       ├─→ Entity
    │       ├─→ Relation
    │       └─→ KnowledgeNode
    │
    └─→ Milvus (Vector Data)
            ├─→ Memory Embedding
            ├─→ Document Embedding
            └─→ Experience Embedding
```

---

## 6. Index Recommendations

### PostgreSQL Indexes

| Table | Index | Purpose |
|-------|-------|---------|
| users | idx_users_email | 登录查询优化 |
| memories | idx_memories_user_id | 用户记忆查询 |
| memories | idx_memories_score | 重要记忆排序 |
| plans | idx_plans_status | 状态筛选 |
| tasks | idx_tasks_status | 任务状态查询 |
| experiences | idx_experiences_category | 类别筛选 |

### Neo4j Indexes

```cypher
CREATE INDEX entity_name_idx FOR (e:Entity) ON (e.name);
CREATE INDEX entity_type_idx FOR (e:Entity) ON (e.entity_type);
CREATE INDEX knowledge_category_idx FOR (k:KnowledgeNode) ON (k.category);
```

### Milvus Indexes

| Collection | Index Type | Parameters |
|------------|------------|------------|
| memory_embeddings | IVF_FLAT | nlist=100 |
| document_embeddings | IVF_FLAT | nlist=100 |
| experience_embeddings | IVF_FLAT | nlist=100 |

---

## 7. Migration Scripts

### Directory Structure

```
backend/
└── migrations/
    ├── 001_create_users_table.sql
    ├── 002_create_memories_table.sql
    ├── 003_create_plans_tables.sql
    ├── 004_create_experiences_table.sql
    ├── 005_create_goals_table.sql
    ├── 006_create_reflections_tables.sql
    ├── 007_create_documents_tables.sql
    └── 008_create_skills_table.sql
```

---

## 8. Development vs Production

| Environment | Database | Configuration |
|-------------|----------|---------------|
| Development | SQLite | Single file |
| Testing | PostgreSQL | Docker container |
| Production | PostgreSQL + Neo4j + Milvus | Distributed |

---

## 9. Backup Strategy

### PostgreSQL
- Daily full backup
- Hourly incremental backup
- Point-in-time recovery

### Neo4j
- Daily database dump
- WAL logging for point-in-time recovery

### Milvus
- Scheduled backups to object storage
- Replica set for high availability

---

## 10. Security Considerations

1. **Encryption**: All data at rest encrypted
2. **Access Control**: Role-based access to databases
3. **Connection Pooling**: Limited connections with timeouts
4. **Audit Logs**: Query logging for security audits
5. **Parameterized Queries**: Prevent SQL injection

---

Last Updated: 2026-05-31
