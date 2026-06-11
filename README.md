# TitanOS v4.0

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

### ⚡ V4.0: Agent System - 预测、帮助、替你执行
- **智能任务管理** - 创建、执行和管理任务，支持优先级和依赖
- **工作流编排** - 创建复杂工作流，支持任务依赖和并行执行
- **技能注册中心** - 内置多种技能（搜索、文件操作、数据分析、代码执行等）
- **智能预测引擎** - 基于历史数据预测任务执行时间
- **智能调度系统** - 支持多种调度策略（优先级、最短优先、依赖排序）
- **自动执行能力** - 自动执行优先级最高的任务
- **智能建议系统** - 提供任务执行建议和工作流优化建议
- **工作流优化** - 关键路径分析、优化分数评估、改进建议

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

### ✅ 第一阶段：MVP（已完成）

#### Task 1: ✅ 接入真实 LLM (DeepSeek API)
- **LLM 服务模块** - 支持 DeepSeek、OpenAI 等多种 LLM 提供商
- **流式输出** - 支持 SSE 流式返回，实时显示 AI 回复
- **历史上下文** - 自动携带历史对话记录
- **API 端点** - `/chat/llm`、`/chat/llm/stream`、`/llm/config`
- **配置管理** - 支持动态配置 API Key、模型等参数

#### Task 2: ✅ Memory Engine
- **记忆存储** - 自动从聊天记录生成长期记忆
- **实体提取** - 提取人物、地点、项目、兴趣、技能、目标
- **记忆评分** - 基于重要性、访问频率计算记忆分数
- **向量搜索** - 支持语义搜索，查找相关记忆
- **API 端点** - `/memory`、`/memory/search`、`/memory/semantic`

#### Task 3: ✅ Memory Timeline
- **动态加载** - 从数据库实时获取记忆数据
- **时间分组** - 按年份、月份自动分组显示
- **类别标签** - 支持 Learning、Project、Achievement、Goal 不同颜色
- **可折叠视图** - 支持展开/折叠时间组
- **API 端点** - `/timeline`、`/timeline/monthly`、`/timeline/events`

### ✅ 第二阶段：TitanOS V1（已完成）

#### Task 4: ✅ Goal Engine
- **目标树管理** - 创建、更新、删除目标
- **自动拆解** - 将大目标拆解为子目标和任务
- **进度追踪** - 实时计算目标完成进度
- **优先级管理** - 支持目标优先级设置
- **API 端点** - `/goal-tree/tree`、`/goal-tree/goal`、`/goal-tree/summary`

#### Task 5: ✅ Growth Score
- **成长分数计算** - 30% Memory + 30% Knowledge + 20% Goal + 20% Skill
- **等级系统** - Newborn → Beginner → Intermediate → Advanced → Expert → Master
- **每日更新** - 自动计算并更新成长分数
- **API 端点** - `/dashboard/growth-score`、`/dashboard/metrics`

#### Task 6: ✅ Dashboard Real Data
- **实时统计** - Total Memories、Knowledge Nodes、Goals、Growth Score
- **数据可视化** - 图表展示各项指标
- **自动刷新** - 支持数据自动更新
- **API 端点** - `/dashboard/summary`、`/dashboard/report`

### ✅ 第三阶段：TitanOS V2（已完成）

#### Task 7: ✅ Knowledge Graph
- **Neo4j 集成** - 图数据库存储实体和关系
- **实体提取** - Person、Skill、Project、Technology、Concept
- **关系构建** - LEARNED、WORKED_ON、INTERESTED_IN、CONNECTED_TO
- **D3.js 可视化** - 支持缩放、拖动、搜索、点击查看详情
- **API 端点** - `/knowledge/graph`、`/knowledge/path`、`/knowledge/analyze`

#### Task 8: ✅ Semantic Search
- **向量数据库** - Qdrant、Weaviate、Pinecone 集成
- **BGE-M3 Embedding** - 高质量文本向量化
- **语义搜索** - 支持自然语言查询记忆
- **API 端点** - `/memory/semantic/{query}`、`/vector-db/init`

### ✅ 第四阶段：TitanOS V3（已完成）

#### Task 9: ✅ Digital Twin Engine
- **数字分身创建** - 创建个性化数字分身
- **五大人格特质** - 开放性、尽责性、外向性、宜人性、神经质
- **行为预测** - 基于性格特质预测行为倾向
- **知识关联** - 将分身与知识图谱实体关联
- **API 端点** - `/digital-twin/profile`、`/digital-twin/{id}/predict`

#### Task 10: ✅ Behavior Analytics
- **学习时间统计** - 追踪学习活动时长
- **活跃时间分析** - 分析用户活跃时段
- **项目投入追踪** - 记录项目相关活动
- **目标完成率** - 计算目标完成情况
- **周报/月报** - 自动生成行为分析报告
- **API 端点** - `/analytics/weekly-report`、`/analytics/monthly-report`、`/analytics/summary`

### ✅ 第五阶段：TitanOS V4（已完成）

#### Task 11: ✅ Planner Agent
- **智能规划** - 自动生成周计划、日计划、里程碑
- **自动调整** - 根据进度自动调整计划
- **API 端点** - `/agent/workflow`、`/agent/recommend`

#### Task 12: ✅ Memory Agent
- **自动总结** - 自动总结聊天内容
- **自动生成记忆** - 从对话中提取重要信息
- **自动归档** - 低价值记忆自动清理
- **重要性评分** - 智能评估记忆价值

#### Task 13: ✅ Knowledge Agent
- **发现知识关联** - 自动发现实体间关系
- **更新知识图谱** - 动态更新图谱结构
- **推荐学习路径** - 基于知识图谱推荐学习内容
- **Knowledge Insights** - 生成知识洞察报告

### 🔲 第六阶段：TitanOS 终极版（计划中）

- **Agent Market** - 用户可安装自定义 Agent
- **Multi-Modal** - 支持图片、视频、语音、PDF 输入
- **Life Operating System** - 聊天、记忆、目标、知识、规划、执行全部统一

---

## 📊 版本概览表

| 版本 | 状态 | 功能 |
|------|------|------|
| **MVP** | ✅ **已完成** | Chat + Memory + Timeline + LLM 集成 (DeepSeek/OpenAI) |
| **V1** | ✅ **已完成** | Goal Engine + Growth Score + Dashboard Real Data |
| **V2** | ✅ **已完成** | Knowledge Graph + Neo4j + Semantic Search 🧠 |
| **V3** | ✅ **已完成** | Digital Twin + Personality Engine + Behavior Analytics 👤 |
| **V4** | ✅ **已完成** | Agent System - Planner/Memory/Knowledge Agent ⚡ |
| **终极版** | 🔲 计划中 | Agent Market + Multi-Modal + Life Operating System |

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

---

## ⚡ Agent System - 预测、帮助、替你执行

### 功能概述

TitanOS v4.0 实现了完整的 Agent System，让 TitanOS 不只是记录你，而是：
- **预测你** - 基于历史数据预测任务执行时间
- **帮助你** - 提供智能建议和优化方案
- **替你执行** - 自动执行任务和工作流

### 架构设计

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Agent System Architecture                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        Agent Interface                          │   │
│  │  - Chat Interface     - Command Processing                    │   │
│  │  - Natural Language   - API Endpoints                         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                   │                                     │
│         ┌─────────────────────────┼─────────────────────────┐          │
│         │                         │                         │          │
│  ┌──────▼──────┐          ┌──────▼──────┐          ┌──────▼──────┐     │
│  │   Runtime   │          │    Agent    │          │ Skill       │     │
│  │   Engine    │          │   Manager   │          │ Registry    │     │
│  │             │          │             │          │             │     │
│  │ - Task      │          │ - Predict   │          │ - Search    │     │
│  │   Execution │          │ - Recommend │          │ - File I/O  │     │
│  │ - Workflow  │          │ - Auto-Exec │          │ - Analyze   │     │
│  │ - Schedule  │          │             │          │ - Summarize │     │
│  └─────────────┘          └─────────────┘          └─────────────┘     │
│         │                         │                         │          │
│         └─────────────────────────┼─────────────────────────┘          │
│                                   ▼                                     │
│                    ┌─────────────────────────┐                          │
│                    │      Task Registry      │                          │
│                    │   + Workflow Storage    │                          │
│                    │   + Execution History   │                          │
│                    └─────────────────────────┘                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 核心模块

| 模块 | 功能 | 说明 |
|------|------|------|
| **Agent** | 统一智能接口 | 支持聊天、命令处理、技能调用 |
| **Runtime** | 运行时引擎 | 任务执行、工作流编排、状态管理 |
| **SkillRegistry** | 技能注册中心 | 管理内置和自定义技能 |
| **Task** | 任务数据结构 | 任务定义、状态管理、优先级 |
| **Workflow** | 工作流定义 | 任务组合、依赖管理、执行顺序 |

### 内置技能

| 技能名称 | 功能 | 输入参数 |
|----------|------|----------|
| **search** | Web 搜索 | `query` - 搜索关键词 |
| **read_file** | 读取文件 | `path` - 文件路径 |
| **write_file** | 写入文件 | `path`, `content` |
| **list_files** | 列出文件 | `path`, `pattern` |
| **copy_file** | 复制文件 | `source`, `destination` |
| **delete_file** | 删除文件 | `path` |
| **rename_file** | 重命名文件 | `old_path`, `new_path` |
| **create_directory** | 创建目录 | `path` |
| **read_json** | 读取 JSON | `path` |
| **write_json** | 写入 JSON | `path`, `data`, `pretty` |
| **read_csv** | 读取 CSV | `path`, `delimiter` |
| **write_csv** | 写入 CSV | `path`, `rows`, `headers` |
| **summarize** | 文本摘要 | `text`, `max_length` |
| **analyze** | 代码/文本分析 | `content`, `type` |
| **system_info** | 系统信息 | 无 |
| **text_replace** | 文本替换 | `path`, `old_text`, `new_text` |
| **extract_text** | 正则提取 | `text`, `pattern` |

### 核心功能

#### 1. 任务预测
基于历史执行数据预测任务执行时间：
```python
from backend.agent import Agent

agent = Agent()
task = agent.create_task(name="数据分析", task_type="analyze")
prediction = agent.predict(task.id, target_type="task")
print(f"预测执行时间: {prediction['predicted_duration']}秒")
```

#### 2. 智能调度
支持多种调度策略：
- `priority` - 按优先级排序（默认）
- `shortest_first` - 最短任务优先
- `dependency` - 按依赖关系排序

```python
scheduled_tasks = agent.schedule_tasks(strategy="priority")
```

#### 3. 自动执行
自动执行优先级最高的任务：
```python
result = agent.auto_execute(limit=5)
print(f"已执行 {result['executed_tasks']} 个任务")
```

#### 4. 智能建议
获取任务执行建议和工作流优化建议：
```python
recommendations = agent.recommend()
for rec in recommendations["recommendations"]:
    print(f"- {rec['message']}")
```

#### 5. 工作流优化
分析工作流并提供优化建议：
```python
optimization = agent.optimize(workflow_id)
print(f"优化分数: {optimization['optimization_score']}")
print("建议:", optimization['suggestions'])
```

### API 接口

#### 创建任务
```python
POST /agent/task
{
    "name": "任务名称",
    "task_type": "skill",
    "input_data": {"skill": "search", "params": {"query": "TitanOS"}},
    "priority": "HIGH",
    "dependencies": []
}
```

#### 执行任务
```python
POST /agent/task/{task_id}/execute
```

#### 创建工作流
```python
POST /agent/workflow
{
    "name": "数据分析工作流",
    "description": "数据收集 → 分析 → 报告"
}
```

#### 获取智能建议
```python
GET /agent/recommend
```

#### 自动执行
```python
POST /agent/auto-execute
{
    "limit": 5
}
```

#### 列出技能
```python
GET /agent/skills
```

#### 执行技能
```python
POST /agent/skill/{skill_name}
{
    "params": {...}
}
```

### 命令行交互

Agent 支持命令行风格的交互：

```python
from backend.agent import Agent

agent = Agent()

# 发送命令
result = agent.process_command("create_task", name="搜索任务", task_type="search", input_data={"query": "AI"})
print(result)

# 直接执行技能
result = agent.execute_skill("search", {"query": "TitanOS"})
print(result)

# 获取建议
result = agent.process_command("recommend")
print(result)

# 自动执行
result = agent.process_command("auto_execute", limit=3)
print(result)
```

### 聊天交互

Agent 还支持自然语言聊天：

```python
response = agent.chat("hello")
print(response)

response = agent.chat("help")
print(response)

response = agent.chat("list skills")
print(response)

response = agent.chat("recommend")
print(response)
```

---

## 👤 Digital Twin + Personality Engine

### 功能概述

TitanOS v3.0 实现了完整的数字分身和性格引擎系统，包括：

- **数字分身创建与管理**: 创建个性化的数字分身，存储在本地和 Neo4j 图数据库中
- **五大人格特质模型**: 开放性、尽责性、外向性、宜人性、神经质
- **行为预测**: 基于性格特质预测行为倾向
- **性格分析**: 详细的性格特质解读和综合分析
- **知识关联**: 将数字分身与知识图谱中的实体关联
- **交互记录**: 记录和追踪数字分身的交互历史
- **相似分身匹配**: 在图数据库中查找性格相似的数字分身

### 架构设计

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Digital Twin + Personality Engine                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────┐      ┌──────────────────────────────────────┐   │
│  │   DigitalTwin    │      │           Neo4j Graph Database       │   │
│  │     Profile      │──────│  ┌─────────────┐  ┌───────────────┐  │   │
│  ├──────────────────┤      │  │DigitalTwin  │  │ Interaction   │  │   │
│  │  Personality     │      │  │   Nodes     │  │    Nodes      │  │   │
│  │   Traits (Big 5) │      │  └──────┬──────┘  └───────┬───────┘  │   │
│  ├──────────────────┤      │         │                  │         │   │
│  │ Writing Style    │      │    KNOWS │         HAS_INTERACTION    │   │
│  ├──────────────────┤      │         │                  │         │   │
│  │  Code Style      │      │         ▼                  ▼         │   │
│  ├──────────────────┤      │  ┌─────────────┐  ┌───────────────┐  │   │
│  │ Learning Habits  │      │  │  Knowledge  │  │   Entity     │  │   │
│  └──────────────────┘      │  │    Entity   │  │   Relation   │  │   │
│                            │  └─────────────┘  └───────────────┘  │   │
│                            └──────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 核心特性

| 模块 | 功能 | 说明 |
|------|------|------|
| **Personality Profile** | 五大人格特质 | 开放性、尽责性、外向性、宜人性、神经质 |
| **Writing Style** | 写作风格分析 | 正式程度、句子长度、表情符号使用 |
| **Code Style** | 代码风格分析 | 语言偏好、命名规范、注释风格 |
| **Behavior Engine** | 行为预测 | 基于性格特质预测行为倾向 |
| **Knowledge Link** | 知识关联 | 将分身与知识实体连接 |
| **Interaction Log** | 交互记录 | 记录所有交互历史 |

### API 接口

```python
# 创建数字分身
POST /digital_twin/create
{
    "name": "My Avatar",
    "personality": {
        "openness": 0.7,
        "conscientiousness": 0.8,
        "extraversion": 0.5,
        "agreeableness": 0.6,
        "neuroticism": 0.3
    }
}

# 获取性格摘要
GET /digital_twin/{id}/personality/summary

# 预测行为
POST /digital_twin/{id}/predict
{
    "scenario": "团队合作项目"
}

# 查找相似分身
GET /digital_twin/{id}/similar?threshold=0.7
```

### 性格特质解读

| 特质 | 低分值 | 中分值 | 高分值 |
|------|--------|--------|--------|
| **开放性** | 注重实际 | 平衡传统与创新 | 富有想象力 |
| **尽责性** | 灵活随性 | 有条理但灵活 | 高度组织化 |
| **外向性** | 内向独处 | 平衡社交与独处 | 外向社交 |
| **宜人性** | 果断自信 | 合作但有原则 | 富有同情心 |
| **神经质** | 情绪稳定 | 情绪适中 | 情绪敏感 |

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

### v4.0
- **Agent System 智能代理系统**
  - 统一智能交互接口（Agent 类）
  - 智能任务管理（创建、执行、取消）
  - 工作流编排（任务组合、依赖管理）
  - 技能注册中心（17+ 内置技能）
  - 智能预测引擎（基于历史数据预测执行时间）
  - 智能调度系统（优先级、最短优先、依赖排序）
  - 自动执行能力（自动执行优先级任务）
  - 智能建议系统（任务建议、工作流优化）
  - 工作流优化（关键路径分析、优化分数评估）
  - 命令行和聊天交互支持

### v3.0
- **Digital Twin 数字分身系统**
  - 创建和管理个性化数字分身
  - 支持本地存储和 Neo4j 图数据库存储
  - 分身与知识图谱实体关联

- **Personality Engine 性格引擎**
  - 五大人格特质模型（开放性、尽责性、外向性、宜人性、神经质）
  - 详细的性格特质分析和解读
  - 基于性格的行为预测
  - 性格相似度匹配算法

- **Neo4j 扩展**
  - 添加数字分身影射节点 (`DigitalTwin`)
  - 交互记录节点 (`Interaction`)
  - KNOWS 关系（分身-知识关联）
  - HAS_INTERACTION 关系（交互历史）

- **响应式写作风格分析**
  - 正式程度检测
  - 句子长度偏好
  - 表情符号使用检测

### v2.0.2
- 修复 `#problems:app.py` - 添加缺失的 `/knowledge/graph` 和 `/knowledge/configure` API 端点
- 修复 `#problems:neo4j_provider.py` - 修复 Neo4j 异常处理
- 修复 `#problems:knowledge_graph.py` - 添加 `get_graph()` 方法

### v2.0.1
- 修复前端后端端口配置不一致问题
- 添加端口配置说明文档
- 更新故障排除指南

### v2.0
- 核心完成：Knowledge Graph + Neo4j 集成
- LLM 实体关系提取
- Next.js + React 前端迁移完成
- 知识推理和路径查找

---

## 🚀 快速开始

### 系统要求
- Python 3.8+
- Node.js 16+ (前端)
- PostgreSQL / MongoDB (可选)
- Neo4j 5.0+ (知识图谱功能)

### 安装步骤

#### 1. 克隆项目
```bash
git clone https://github.com/tianxv1/TitanOS.git
cd TitanOS
```

#### 2. 后端设置
```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动后端服务
python app.py
# 或使用 uvicorn
# uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

后端服务将在 `http://localhost:8000` 运行。

#### 3. 前端设置
```bash
cd frontend

# 安装依赖
npm install

# 启动前端开发服务器
npm run dev
```

前端应用将在 `http://localhost:3000` 运行。

#### 4. 可选：启动 Neo4j
```bash
# 使用 Docker
docker run -p 7687:7687 -p 7474:7474 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest

# 或本地安装
neo4j start
```

### 验证安装
```bash
# 检查后端 API
curl http://localhost:8000/memory/stats

# 检查前端
# 打开浏览器访问 http://localhost:3000
```

---

## 🏗️ 项目结构

### 后端架构 (`backend/`)

| 模块 | 功能描述 |
|------|--------|
| **agent/** | 智能体运行时、技能注册、任务管理 |
| **analytics/** | 行为分析、周报月报、活动统计 |
| **auth/** | 用户认证、JWT、用户存储 |
| **brain/** | 推理引擎、思维链生成 |
| **chat/** | 聊天引擎、对话管理、LLM 集成 |
| **dashboard/** | 仪表盘统计、数据聚合 |
| **digital_twin/** | 数字分身、用户画像、风格学习 |
| **goal_tree/** | 目标树、目标分解、追踪 |
| **knowledge_base/** | 知识库管理、文档处理 |
| **knowledge_graph/** | Neo4j 集成、实体关系、图谱推理 |
| **learning/** | 学习引擎、经验积累、模式识别 |
| **llm/** | LLM 服务、DeepSeek/OpenAI 集成、流式输出 |
| **marketplace/** | Agent 市场、插件管理 |
| **memory/** | 记忆引擎、三种认知记忆、评分系统 |
| **multi_agent/** | 多智能体协调、团队协作 |
| **planner/** | 任务规划、时间线、里程碑 |
| **rag/** | 检索增强生成、向量搜索、重排序 |
| **reflection/** | 反思系统、错误分析、改进追踪 |
| **skills/** | 技能商店、代码执行、搜索集成 |
| **timeline/** | 时间线管理、事件记录 |
| **vector_db/** | 向量数据库管理、多种提供商支持 |
| **world_model/** | 世界模型、因果关系、事件预测 |

### 前端架构 (`frontend/`)

```
frontend/
├── app/                    # Next.js App Router
│   ├── page.tsx           # 首页
│   ├── chat/              # 聊天页面
│   ├── dashboard/         # 仪表盘
│   ├── goals/             # 目标管理
│   ├── knowledge-graph/   # 知识图谱可视化
│   ├── memory/            # 记忆查看
│   └── settings/          # 设置页面
├── components/            # React 组件
│   ├── Sidebar.tsx       # 侧边栏导航
│   └── ...               # 其他组件
├── lib/
│   └── api.ts            # API 客户端
└── public/               # 静态资源
```

### 数据库架构 (`database/`)

| 文件 | 用途 |
|------|------|
| `chat_history.json` | 聊天记录存储 |
| `marketplace.json` | Agent 市场数据 |
| `memories.json` | 记忆数据库 |
| **Neo4j** | 知识图谱存储 |
| **Qdrant/Weaviate/Pinecone** | 向量数据库 |

---

## 💻 核心 API 端点

### 聊天相关
```
POST   /chat                    - 发送消息
GET    /chat/history           - 获取聊天历史
GET    /chat/stats             - 聊天统计
POST   /chat/llm               - LLM 聊天 (DeepSeek/OpenAI)
POST   /chat/llm/stream        - LLM 流式聊天 (SSE)
```

### LLM 配置
```
GET    /llm/config             - 获取 LLM 配置
POST   /llm/config             - 配置 LLM 服务
GET    /llm/status             - 获取 LLM 状态
```

### 记忆相关
```
GET    /memory/stats           - 记忆统计
POST   /memory/add             - 添加记忆
GET    /memory/search          - 全文搜索
GET    /memory/semantic/{query} - 语义搜索
POST   /memory/sync-vector-db  - 同步到向量数据库
```

### 时间线
```
GET    /timeline               - 按年获取时间线
GET    /timeline/monthly       - 按月获取时间线
GET    /timeline/events        - 获取所有事件
GET    /timeline/milestones    - 获取里程碑事件
```

### 知识图谱
```
GET    /knowledge/graph        - 获取图谱数据
POST   /knowledge/analyze      - LLM 文本分析
POST   /knowledge/configure    - 配置 Neo4j 连接
GET    /knowledge/path         - 查询路径
```

### 向量数据库
```
POST   /vector-db/init        - 初始化向量 DB
GET    /vector-db/health      - 健康检查
GET    /vector-db/stats       - 统计信息
```

### 数字分身
```
GET    /digital-twin/profile  - 获取用户画像
POST   /digital-twin/update   - 更新数字分身
```

### 目标管理
```
GET    /goals                 - 获取所有目标
POST   /goals                 - 创建新目标
PUT    /goals/{id}            - 更新目标
DELETE /goals/{id}            - 删除目标
```

### 行为分析
```
GET    /analytics/metrics           - 获取行为指标
POST   /analytics/activity          - 记录活动
GET    /analytics/weekly-report     - 获取周报
GET    /analytics/monthly-report    - 获取月报
GET    /analytics/chart-data        - 获取图表数据
GET    /analytics/category-breakdown - 获取类别分解
GET    /analytics/hourly-distribution - 获取每小时分布
GET    /analytics/summary           - 获取分析摘要
```

---

## 🔧 配置指南

### 后端环境变量

创建 `backend/.env` 文件：

```env
# FastAPI 配置
DEBUG=True
HOST=0.0.0.0
PORT=8000

# LLM 配置 (DeepSeek / OpenAI)
DEEPSEEK_API_KEY=your-deepseek-api-key  # DeepSeek API Key
OPENAI_API_KEY=your-openai-api-key      # OpenAI API Key (可选)
LLM_PROVIDER=deepseek  # deepseek | openai | simulated

# Neo4j 配置
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_DATABASE=neo4j

# 向量数据库选择
VECTOR_DB_PROVIDER=in_memory  # in_memory | qdrant | weaviate | pinecone

# Qdrant 配置
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Weaviate 配置
WEAVIATE_HOST=localhost
WEAVIATE_PORT=8080

# Pinecone 配置
PINECONE_API_KEY=your-api-key
PINECONE_ENVIRONMENT=us-west1-gcp
```

### 前端环境变量

创建 `frontend/.env.local` 文件：

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=TitanOS
NEXT_PUBLIC_VERSION=2.0
```

---

## 📚 技术栈

### 后端
- **框架:** FastAPI (异步 Web 框架)
- **数据库:**
  - JSON (轻量级存储)
  - Neo4j (知识图谱)
  - PostgreSQL/MongoDB (可选)
- **向量数据库:** Qdrant / Weaviate / Pinecone
- **LLM 集成:** OpenAI / Anthropic / 本地模型
- **认证:** JWT + Passlib
- **异步:** Python asyncio

### 前端
- **框架:** Next.js 12 + React 18
- **样式:** Tailwind CSS + PostCSS
- **UI 组件:** Lucide React (图标)
- **语言:** TypeScript
- **API 客户端:** fetch / axios

### DevOps
- **容器化:** Docker / Docker Compose
- **API 文档:** OpenAPI / Swagger

---

## 🧪 测试与验证

### 单元测试
```bash
cd backend
python -m pytest tests/ -v
```

### 集成测试
```bash
# 验证 API 端点
curl -X GET http://localhost:8000/memory/stats

# 验证前端连接
curl -X GET http://localhost:3000
```

### 性能测试
```bash
# 使用 Apache Bench
ab -n 1000 -c 100 http://localhost:8000/memory/stats
```

---

## 🤝 贡献指南

我们欢迎各种形式的贡献！详见 [CONTRIBUTING.md](CONTRIBUTING.md)

### 快速贡献流程

1. **Fork 项目**
   ```bash
   git clone https://github.com/your-username/TitanOS.git
   ```

2. **创建特性分支**
   ```bash
   git checkout -b feature/your-feature
   ```

3. **提交更改**
   ```bash
   git add .
   git commit -m "feat: describe your feature"
   git push origin feature/your-feature
   ```

4. **创建 Pull Request**
   - 详细描述你的更改
   - 提供测试证明
   - 等待审核

### 代码风格
- **Python:** PEP 8 + Black 格式化
- **TypeScript:** ESLint + Prettier 格式化
- **提交信息:** Conventional Commits (`feat:`, `fix:`, `docs:`)

---

## 📖 文档

- [架构设计](ARCHITECTURE.md) - 系统架构详解
- [开发路线图](ROADMAP.md) - 功能开发计划
- [API 文档](docs/API_REFERENCE.md) - 完整 API 参考
- [数据库设计](docs/DATABASE_DESIGN.md) - 数据模型说明
- [部署指南](docs/DEPLOYMENT.md) - 生产部署步骤

---

## 🔍 故障排除快速指南

### 常见错误解决方案

| 错误 | 原因 | 解决方案 |
|-----|------|--------|
| `ERR_ABORTED http://localhost:3000/` | 前端未启动 | `cd frontend && npm run dev` |
| `ERR_CONNECTION_REFUSED :8000` | 后端未启动 | `cd backend && python app.py` |
| `Neo4j connection failed` | Neo4j 未启动 | `docker run -p 7687:7687 neo4j` |
| `Module not found` | 依赖未安装 | `pip install -r requirements.txt` 或 `npm install` |
| `Port already in use` | 端口被占用 | 修改端口配置或释放占用进程 |

详细故障排除见 **⚠️ 故障排除与端口配置** 章节。

---

## 📊 项目统计

```
总模块数: 21+
代码行数: 20,000+
API 端点: 60+
支持数据库: 5+ (JSON, Neo4j, Qdrant, Weaviate, Pinecone)
前端组件: 12+
LLM 提供商: 3 (DeepSeek, OpenAI, Simulated)
测试覆盖率: 70%+
```

---

## 🎯 未来展望

### 即将推出 (V3.0+)
- 🤖 **自主代理** - AI 自动执行任务
- 👤 **人格引擎** - 深度个性化学习
- 🌐 **多语言支持** - 国际化
- 📱 **移动应用** - iOS/Android
- 🔐 **端到端加密** - 隐私保护
- ⚡ **性能优化** - 边缘计算支持

---

## 📝 许可证

本项目采用 [MIT 许可证](LICENSE)

---

## 🙋 获取帮助

- **GitHub Issues:** [报告 Bug / 功能请求](https://github.com/tianxv1/TitanOS/issues)
- **Discussions:** [社区讨论](https://github.com/tianxv1/TitanOS/discussions)
- **邮件:** contact@titanos.ai
- **文档:** [完整文档](https://titanos.ai/docs)

---

## 🌟 致谢

感谢所有贡献者和使用者的支持！

```
⭐ 如果这个项目对你有帮助，请给我们一个 Star 吧！
```

---

**最后更新:** 2026年6月8日  
**当前版本:** v4.0 (Agent System - 预测、帮助、替你执行)  
**维护者:** TitanOS Team
