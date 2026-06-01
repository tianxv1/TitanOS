# TitanOS v1.5

> 世界上第一个能持续成长的个人AI操作系统

[![GitHub stars](https://img.shields.io/github/stars/tianxv1/TitanOS)](https://github.com/tianxv1/TitanOS/stargazers)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)

---

## 🎯 TitanOS 到底长什么样？

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           TitanOS v1.5                                  │
│                   持续成长的个人AI操作系统                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────┬─────────────────────────────────────────────────────────────┐  │
│  │     │  ┌───────────────────────────────────────────────────────┐  │  │
│  │ 💬  │  │  Dashboard: Growth 78%  Memories: 1,234  Goals: 18   │  │  │
│  │ 📊  │  └───────────────────────────────────────────────────────┘  │  │
│  │ 🧠  │  ┌───────────────────────────────────────────────────────┐  │  │
│  │ 📋  │  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐  │  │  │
│  │ 🔗  │  │  │   Chat      │ │  Timeline   │ │    Graph    │  │  │  │
│  │ 👤  │  │  └─────────────┘ └─────────────┘ └─────────────┘  │  │  │
│  └─────┴─────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  🎨 紫青配色 | 📱 桌面应用风格 | 📈 数据可视化 | 🔍 语义搜索              │
└─────────────────────────────────────────────────────────────────────────┘
```

**这是一个AI操作系统，而不是一个API集合。**

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🧠 **认知架构** | 6层认知模型：感知→记忆→思考→规划→执行→学习 |
| 🔄 **持续成长** | 每次交互都在学习，AI会变得越来越懂你 |
| 🎯 **目标驱动** | Goal Tree 树形目标管理，自动拆解与追踪 |
| 🤖 **多代理协作** | Multi-Agent 团队协作，Research→Plan→Code→Review |
| 📊 **成长可见** | Dashboard 可视化成长轨迹，数字分身成熟度 |
| 🧩 **记忆系统** | Episodic/Semantic/Procedural 三种认知记忆 |
| 🌐 **知识图谱** | Neo4j 知识推理，实体关系网络 |
| 🛒 **Agent市场** | 像VS Code Extension一样的Agent生态 |
| 💬 **Chat + Memory** | ✅ V1 已完成：聊天自动存入记忆系统 |
| 🔍 **向量搜索** | ✅ V1.5 已完成：Qdrant/Weaviate/Pinecone 集成 |

---

## 🚀 最近更新

### 🧠 V2.0: Knowledge Graph + Neo4j + LLM 集成
- **Neo4j 图数据库集成** - 支持高性能图查询和路径查找
- **LLM 实体关系提取** - 自动从文本中提取实体和关系
- **知识推理引擎** - 支持实体间路径查找和关系推理
- **Cypher 查询 API** - 直接执行 Cypher 查询
- **文本分析 API** - `/knowledge/analyze` 使用 LLM 分析文本
- **新增 API 端点** - `/knowledge/neo4j/init`、`/knowledge/path`、`/knowledge/analyze`

### 🔍 V1.5: Vector DB 集成 - 语义搜索新时代
- **多种向量数据库支持** - Qdrant、Weaviate、Pinecone
- **统一 Provider 接口** - 轻松切换不同的向量数据库
- **语义搜索** - 使用自然语言搜索记忆，查找相关概念
- **自动 Embedding** - 文本自动转换为向量表示
- **内存向量存储** - 无需外部依赖，快速上手

### 💬 V1: Chat + Memory 集成
- **聊天历史** - 自动保存对话记录
- **记忆同步** - 每次聊天都存入 Memory Engine
- **智能回复** - 简单回复生成器（后续升级 LLM）
- **API 端点** - `/chat` `/chat/history` `/chat/stats`

---

## 🗺️ 详细开发路线图

### ✅ V1 - 已完成：Chat + Memory
- 聊天引擎实现
- 聊天历史自动存入记忆系统
- 完整的 UI 界面（侧边栏、紫青配色）
- Dashboard、Memory Timeline、Knowledge Graph、Digital Twin 全部可视化

### ✅ V1.5 - 已完成：Vector DB 集成 (Qdrant/Weaviate/Pinecone)
- **VectorDBProvider 基类** - 统一的向量数据库接口
- **Qdrant 集成** - 高性能向量数据库，支持 gRPC
- **Weaviate 集成** - 云原生向量搜索引擎
- **Pinecone 集成** - 托管向量数据库服务
- **In-Memory 向量存储** - 无需外部依赖
- **语义搜索 API** - `/memory/semantic/{query}`
- **向量数据库管理** - `/vector-db/init`、`/vector-db/health`、`/vector-db/stats`
- **记忆同步** - 将现有记忆同步到向量数据库
- **前端语义搜索界面** - Memory 页面支持自然语言搜索

### ✅ V2.0 - 已完成：Knowledge Graph + Neo4j、LLM 集成 + React 前端
- **Neo4j 数据库集成** - 图数据库支持，高性能图查询
- **LLM 集成** - 实体关系自动提取
- **知识图谱推理引擎** - 路径查找、关系推理
- **Cypher 查询支持** - 直接执行 Cypher 查询
- **文本分析 API** - 使用 LLM 从文本提取知识
- **知识图谱可视化增强** - 支持多层次展示
- **Next.js + React 前端** - 完整的 React 应用架构迁移

### 🔲 V3 - Knowledge Graph + Neo4j
- Neo4j 数据库集成
- 实体关系自动提取
- 知识图谱推理
- 可视化交互增强

### 🔲 V3 - Digital Twin + Personality Engine
- 建立 Personality Engine（人格引擎）
- 实时更新：性格、能力、兴趣、价值观
- 学习模式分析
- 决策风格识别

### 🔲 V4 - Agent System
- 让 TitanOS 不只是记录你，而是：
  - 预测你
  - 帮助你
  - 替你执行
- 多 Agent 协作系统
- 任务自动化执行

---

## 📊 版本概览表

| 版本 | 状态 | 功能 |
|------|------|------|
| v1.0 | ✅ 已发布 | 核心模块完成（17个模块） |
| v1.1 | ✅ 已完成 | Model Layer、World Model、Plugin SDK |
| v1.2 | ✅ 已完成 | UI 升级、Chat + Memory 集成 |
| **v1.5** | ✅ **已完成** | Vector DB 集成（Qdrant/Weaviate/Pinecone）✨ |
| **v2.0** | ✅ **已完成** | Knowledge Graph + Neo4j、LLM 集成 + React 前端 🧠 |
| v3.0 | 📅 计划 | Digital Twin + Personality Engine |
| v4.0 | 📅 计划 | Agent System - 预测、帮助、替你执行 |

---

## 🔧 Vector DB 架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Vector DB Integration                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                    VectorDBManager                                 │ │
│  │  ┌─────────────────────────────────────────────────────────────┐ │ │
│  │  │                  VectorDBProvider (Interface)                 │ │ │
│  │  │  - connect() / disconnect()                                 │ │ │
│  │  │  - upsert() / search() / delete()                          │ │ │
│  │  │  - create_collection() / collection_exists()               │ │ │
│  │  └─────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                   │                                     │
│         ┌─────────────────────────┼─────────────────────────┐          │
│         │                         │                         │          │
│  ┌──────▼──────┐          ┌──────▼──────┐          ┌──────▼──────┐     │
│  │   Qdrant   │          │   Weaviate  │          │   Pinecone  │     │
│  │  Provider  │          │   Provider  │          │   Provider  │     │
│  └─────────────┘          └─────────────┘          └─────────────┘     │
│         │                         │                         │          │
│  ┌──────▼──────┐          ┌──────▼──────┐          ┌──────▼──────┐     │
│  │ - gRPC     │          │ - REST API  │          │ - Cloud     │     │
│  │ - HNSW     │          │ - GraphQL   │          │ - Serverless│     │
│  │ - Payload  │          │ - Modules   │          │ - Managed   │     │
│  └─────────────┘          └─────────────┘          └─────────────┘     │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                    InMemoryProvider (Default)                      │ │
│  │  - No external dependencies                                        │ │
│  │  - Perfect for development and testing                             │ │
│  │  - Easy to switch to production DB later                           │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 Vector DB API 使用示例

### 初始化向量数据库

```bash
# 使用内置内存向量存储（默认，无需配置）
curl -X POST http://localhost:8000/vector-db/init \
  -H "Content-Type: application/json" \
  -d '{"provider": "in_memory"}'

# 使用 Qdrant
curl -X POST http://localhost:8000/vector-db/init \
  -H "Content-Type: application/json" \
  -d '{"provider": "qdrant", "host": "localhost", "port": 6333}'

# 使用 Weaviate
curl -X POST http://localhost:8000/vector-db/init \
  -H "Content-Type: application/json" \
  -d '{"provider": "weaviate", "host": "localhost", "port": 8080}'

# 使用 Pinecone
curl -X POST http://localhost:8000/vector-db/init \
  -H "Content-Type: application/json" \
  -d '{"provider": "pinecone", "api_key": "your-api-key", "environment": "us-west1-gcp"}'
```

### 语义搜索

```bash
# 自然语言搜索记忆
curl "http://localhost:8000/memory/semantic/What%20did%20I%20learn%20about%20Python?limit=10"

# Response:
{
  "query": "What did I learn about Python?",
  "results": [
    {
      "id": "mem-123",
      "content": "Learned Python basics - variables, loops, functions",
      "importance": 0.8,
      "tags": ["learning", "python"]
    }
  ],
  "count": 1
}
```

### 同步记忆到向量数据库

```bash
# 将所有现有记忆同步到向量数据库
curl -X POST http://localhost:8000/memory/sync-vector-db

# Response:
{
  "synced": 150,
  "status": "completed"
}
```

### 检查向量数据库状态

```bash
# 健康检查
curl http://localhost:8000/vector-db/health

# 统计信息
curl http://localhost:8000/vector-db/stats
```

---

## 🎯 关于前端架构迁移

**当前架构：** `backend/static/` (纯 HTML + CSS + JS)
- ✅ 无需额外依赖
- ✅ 开发速度快
- ✅ 适合 V1-V2 阶段

**未来架构：** `frontend/` (Next.js + React)
- 📅 **V2/V3 阶段后迁移** - 当需要更复杂功能时
- ✅ 更现代化的开发体验
- ✅ 更好的性能和可维护性

---

## ✅ 测试验证 (v1.5)

### API 端点测试

| 端点 | 方法 | 状态 | 说明 |
|------|------|------|------|
| `/memory/stats` | GET | ✅ 200 OK | 记忆统计信息 |
| `/memory/semantic/{query}` | GET | ✅ 200 OK | 语义搜索 |
| `/chat` | POST | ✅ 200 OK | 聊天功能 |
| `/chat/history` | GET | ✅ 200 OK | 聊天历史 |
| `/vector-db/health` | GET | ✅ 200 OK | 向量数据库健康检查 |
| `/vector-db/stats` | GET | ✅ 200 OK | 向量数据库统计 |

### 测试结果示例

```bash
# 测试记忆统计
curl http://localhost:8000/memory/stats

# Response:
{
  "total": 14,
  "avg_importance": 0.57,
  "avg_access_count": 0.0,
  "avg_score": 0.439,
  "top_tags": [["chat", 14], ["user", 7], ["assistant", 7]],
  "vector_db": {
    "total": 0,
    "provider": "in_memory",
    "health": {"status": "healthy"}
  }
}
```

### 语义搜索测试

```bash
# 测试语义搜索
curl "http://localhost:8000/memory/semantic/我最近学了什么?limit=5"

# Response:
{
  "query": "我最近学了什么?",
  "results": [...],
  "count": 3
}
```

---

## ⚠️ 故障排除与端口配置

### 常见问题

#### 1. 前端连接问题
**错误信息:** `net::ERR_ABORTED http://localhost:3000/`

**可能原因:**
- 前端开发服务器未启动
- 端口 3000 被其他程序占用
- 防火墙阻止了连接

**解决方案:**
```bash
# 检查端口是否被占用
netstat -ano | findstr :3000

# 停止占用端口的进程（替换PID）
taskkill /F /PID <PID>

# 重新启动前端服务器
cd frontend
npm run dev
```

#### 2. 后端API连接问题
**错误信息:** `net::ERR_CONNECTION_REFUSED http://127.0.0.1:8000/knowledge/graph`

**可能原因:**
- 后端服务器未启动
- 端口配置不一致
- CORS 配置问题

**解决方案:**
```bash
# 启动后端服务器
cd backend
python app.py

# 或使用 uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000
```

#### 3. Neo4j 连接问题 (`#problems:neo4j_provider.py`)
**错误信息:** Neo4j 连接失败

**可能原因:**
- Neo4j 服务未启动
- 连接配置错误（URI、用户名、密码）
- Neo4j 认证问题

**解决方案:**
```bash
# 启动 Neo4j 服务（根据安装方式）
# Docker 方式
docker start neo4j-container

# 本地安装方式
neo4j start

# 检查连接配置
# 文件: backend/knowledge_graph/neo4j_provider.py
# 默认配置: bolt://localhost:7687
```

### 端口配置说明

| 服务 | 默认端口 | 配置位置 |
|------|----------|----------|
| **前端 (Next.js)** | 3000 | `frontend/package.json` |
| **后端 (FastAPI)** | 8000 | `backend/app.py:1933` |
| **Neo4j** | 7687 | `backend/knowledge_graph/neo4j_provider.py` |
| **Qdrant** | 6333 | `backend/vector_db/qdrant.py` |

### 切换端口号

#### 前端端口
修改 `frontend/package.json`:
```json
{
  "scripts": {
    "dev": "next dev -p 3001"
  }
}
```

#### 后端端口
修改 `backend/app.py` (第 1933 行):
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

#### 前端API配置
修改 `frontend/src/pages/index.tsx`:
```typescript
const API_BASE = 'http://127.0.0.1:8001';
```

修改 `frontend/next.config.js`:
```javascript
env: {
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8001',
},
async rewrites() {
  return [
    {
      source: '/api/:path*',
      destination: 'http://127.0.0.1:8001/:path*',
    },
  ]
}
```

### 完整启动流程

```bash
# 1. 启动 Neo4j（可选，如果使用知识图谱功能）
docker run -p 7687:7687 -p 7474:7474 neo4j

# 2. 启动后端服务
cd backend
python app.py

# 3. 启动前端服务
cd frontend
npm run dev

# 4. 访问应用
# 前端: http://localhost:3000
# 后端API: http://localhost:8000
```

---

## 🐛 已知问题修复记录

### #problems:app.py
**问题描述:** 前端调用了后端不存在的 API 端点

**受影响的端点:**
- `GET /knowledge/graph` - 前端需要获取知识图谱数据
- `POST /knowledge/configure` - 前端需要配置 Neo4j 连接

**修复方案:**
在 `backend/app.py` 中添加了以下缺失的 API 端点：

```python
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
```

### #problems:neo4j_provider.py
**问题描述:** Neo4j Python 驱动中的异常处理错误

**错误信息:**
```
AttributeError: module 'neo4j.exceptions' has no attribute 'Neo4jException'
```

**修复方案:**
在 `backend/knowledge_graph/neo4j_provider.py` 中将具体的异常类型改为通用异常：

```python
# 修复前
except exceptions.Neo4jException as e:
    print(f"Neo4j connection failed: {e}")
    return False

# 修复后
except Exception as e:
    print(f"Neo4j connection failed: {e}")
    return False
```

### #problems:knowledge_graph.py
**问题描述:** KnowledgeGraph 类缺少 `get_graph()` 方法

**修复方案:**
在 `backend/knowledge_graph/knowledge_graph.py` 中添加了 `get_graph()` 方法

---

## 📝 更新日志

### v2.0.2
- 修复 `#problems:app.py` - 添加缺失的 `/knowledge/graph` 和 `/knowledge/configure` API 端点
- 修复 `#problems:neo4j_provider.py` - 修复 Neo4j 异常处理
- 修复 `#problems:knowledge_graph.py` - 添加 `get_graph()` 方法

### v2.0.1
- 修复前端后端端口配置不一致问题
- 添加端口配置说明文档
- 更新故障排除指南
