# TitanOS v1.0

> 世界上第一个能持续成长的个人AI操作系统

## 核心理念

不同于ChatGPT套壳或Agent套壳，TitanOS是一个会成长的AI系统，模拟人类的认知架构：

```
用户 → 感知层 → 记忆层 → 思考层 → 规划层 → 执行层 → 学习层
```

## 系统架构

```
TitanOS v1.0/
├── Gateway              # API网关 (FastAPI)
├── Brain               # 推理引擎
├── Memory              # 记忆系统
│   └── Cognitive Memory # 认知记忆 (Episodic/Semantic/Procedural)
├── KnowledgeGraph      # 知识图谱 (Neo4j兼容)
├── Planner             # 任务规划器
├── Executor            # 执行器
├── Learning            # 学习引擎
├── RAG Engine          # 检索增强生成
├── Agent Runtime       # Agent运行时
├── Reflection System   # 反思系统
├── Knowledge Base      # 知识库
├── Auth                # 用户认证系统
├── Timeline            # 记忆时间线
├── Dashboard           # 成长仪表盘
├── Goal Tree           # 目标树
├── Multi-Agent         # 多代理协作
└── Agent Marketplace   # Agent市场
```

## 快速开始

### 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 启动服务

```bash
python app.py
```

API文档: http://localhost:8000/docs

## 核心模块

### 1. Memory Engine (记忆引擎)

AI不是保存所有记忆，而是像人一样遗忘。

```python
score = importance * 0.6 + access_count * 0.3 + recent_score * 0.1
```

- **低分记忆** → 自动删除
- **高分记忆** → 永久保留
- **经验存储** → 任务完成后自动总结

### 2. Cognitive Memory (认知记忆系统)

模仿人脑的三种记忆机制：

| 记忆类型 | 描述 | 结构 |
|----------|------|------|
| **Episodic**（情景记忆） | 时间、地点、人物、事件、情感 | time, location, people, event, emotion |
| **Semantic**（语义记忆） | 知识概念和定义 | concept, definition, relations, examples |
| **Procedural**（技能记忆） | 操作步骤和技能掌握 | skill, steps, mastery_level |

### 3. Brain (推理引擎)

- 问题分析与类型识别
- 链式推理 (Chain of Thought)
- 逻辑推断与假设验证

### 4. KnowledgeGraph (知识图谱)

将记忆和外部信息结构化为实体关系图：

```
张三 -[喜欢]-> 机器学习
机器学习 -[属于]-> 人工智能
人工智能 -[研究]-> Deep Learning
```

**支持的关系类型**: KNOWS, LIKES, BELONGS_TO, PART_OF, CAUSES, RELATED_TO, LEADS_TO, DEPENDS_ON, WORKS_AT, STUDIES, CREATED_BY, LOCATED_AT

### 5. RAG Engine (检索增强生成)

```
Query → Embedding → Vector Search → Rerank → LLM
```

- 混合搜索（向量 + 关键词）
- 语义重排序
- 上下文构建

### 6. Agent Runtime (Agent运行时)

- 任务/工作流管理
- 技能注册表
- 执行调度

### 7. Reflection System (反思系统)

- 任务后分析
- 错误追踪
- 改进建议生成

### 8. Learning Engine (经验学习)

每次任务完成后自动总结经验：

```python
experience = {
    "task": "写爬虫",
    "result": "成功",
    "time": "15min",
    "lesson": "先检查反爬机制"
}
```

- 自动提取学习模式
- 生成成长报告
- 为Planner和DigitalTwin提供反馈

### 9. Goal Tree (目标树)

树形结构的目标管理：

```
Goal
├── Career
│   ├── Get Promotion
│   └── Learn Management
├── Learning
│   ├── Study AI
│   └── Read 50 Books
├── Health
│   ├── Exercise 3x/week
│   └── Sleep 8 hours
└── Project
    ├── Build TitanOS
    └── Launch MVP
```

- 四种目标类别：Career、Learning、Health、Project
- 多级子目标
- 进度自动传播
- 过期提醒

### 10. Multi-Agent (多代理协作)

多个专业Agent协作完成复杂任务：

```
Research Agent → Planner Agent → Coding Agent → Review Agent
     ↓              ↓              ↓              ↓
  信息收集        任务分解        代码实现       质量审查
```

**内置代理**:
| 代理 | 类型 | 功能 |
|------|------|------|
| SearchAgent | search | 网络搜索 |
| ResearchAgent | research | 深度研究 |
| CrawlerAgent | search | 网页爬取 |
| CodingAgent | coding | 代码编写 |
| ReviewerAgent | reviewer | 代码审查 |
| PlannerAgent | planner | 任务规划 |
| AnalyzerAgent | analyzer | 数据分析 |
| SummarizerAgent | summarizer | 内容总结 |

### 11. Agent Marketplace (Agent市场)

类似VS Code Extension的Agent生态系统：

```
├── SearchAgent          ⭐ 4.8 (12.5k downloads)  [已安装]
├── ResearchAgent        ⭐ 4.9 (8.9k downloads)   [已安装]
├── CodingAgent         ⭐ 4.7 (15.2k downloads)  [已安装]
├── ReviewerAgent        ⭐ 4.6 (7.8k downloads)   [已安装]
├── PlannerAgent         ⭐ 4.8 (11k downloads)    [已安装]
├── TranslatorAgent     ⭐ 4.6 (9.1k downloads)  [未安装]
├── FinanceAgent         ⭐ 4.7 (6.2k downloads)  [未安装]
└── DebuggerAgent        ⭐ 4.2 (2.8k downloads)  [未安装]
```

- 支持依赖自动安装
- 评分和下载统计
- 分类浏览

### 12. Digital Twin (数字分身)

记录用户风格，为AI提供个性化决策：

- **写作风格**: 正式程度、语气、常用短语
- **代码风格**: 语言偏好、命名规范、错误处理方式
- **决策模式**: situation → 决策 → 结果
- **学习习惯**: 学科、时间偏好、学习方法

### 13. Timeline (记忆时间线)

以时间轴形式展示记忆成长历程：

```
2026
├── 6月
│   ├── 学习深度学习 [重要]
│   └── 参加AI竞赛
├── 5月
│   ├── 开发TitanOS
│   └── 获得Offer
└── 4月
    ├── 学习Python
    └── 学习机器学习
```

### 14. Dashboard (成长仪表盘)

展示个人AI成长状态：

```
┌─────────────────────────────────────┐
│         Growth Dashboard            │
├─────────────────────────────────────┤
│  Growth Score     78/100  ⭐ Expert │
├─────────────────────────────────────┤
│  总记忆数          1,234            │
│  经验数            56               │
│  知识节点          328               │
│  任务完成率        85%              │
│  数字分身成熟度     72%              │
│  学习进度          68%              │
└─────────────────────────────────────┘
```

### 15. Auth (用户认证)

JWT-based用户认证系统：

- 用户注册/登录
- Token刷新
- 密码修改
- 用户资料管理

## API示例

### 记忆系统

```bash
# 添加记忆
POST /memory
{
  "content": "今天学习了深度学习",
  "importance": 0.8,
  "tags": ["学习", "AI"]
}

# 搜索记忆
GET /memory/search/深度学习

# 创建经验记忆
POST /memory/experience
{
  "task": "写爬虫",
  "result": "成功",
  "time_taken": "15min",
  "lesson": "先检查反爬机制"
}
```

### 认知记忆

```bash
# 添加情景记忆
POST /cognitive/episodic
{
  "event": "第一次训练CNN",
  "location": "学校实验室",
  "people": ["导师", "同学"],
  "emotion": "兴奋",
  "content": "成功训练出第一个模型"
}

# 添加语义记忆
POST /cognitive/semantic
{
  "concept": "CNN",
  "definition": "卷积神经网络，深度学习的核心架构",
  "relations": [{"type": "属于", "target": "深度学习"}]
}

# 添加技能记忆
POST /cognitive/procedural
{
  "skill": "训练模型",
  "steps": ["准备数据", "设计网络", "训练", "评估"]
}

# 练习技能
POST /cognitive/procedural/{id}/practice
{"practice_quality": 0.9}
```

### 知识图谱

```bash
# 创建实体
POST /knowledge/entity
{"name": "机器学习", "entity_type": "concept", "description": "AI的一个分支"}

# 创建关系
POST /knowledge/relation
{
  "from_entity_id": "xxx",
  "to_entity_id": "yyy",
  "relation_type": "BELONGS_TO"
}

# 查询实体邻居
GET /knowledge/entity/{entity_id}/neighbors?depth=2

# 从文本提取实体和关系
POST /knowledge/extract
{"text": "机器学习属于人工智能"}
```

### 目标树

```bash
# 创建目标
POST /goal-tree/goal
{
  "title": "学习AI",
  "category": "Learning",
  "priority": 1
}

# 添加子目标
POST /goal-tree/subgoal
{
  "parent_id": "xxx",
  "title": "学习深度学习",
  "priority": 2
}

# 获取目标树
GET /goal-tree/tree?category=Learning

# 获取优先级目标
GET /goal-tree/priority?limit=5
```

### 多代理协作

```bash
# 列出代理
GET /multi-agent/agents

# 分配任务
POST /multi-agent/task
{
  "agent_id": "xxx",
  "title": "研究深度学习",
  "description": "深入研究CNN的原理和应用"
}

# 执行工作流
POST /multi-agent/workflow/execute
{"goal": "开发一个网站"}
```

### Agent市场

```bash
# 浏览代理
GET /marketplace/packages

# 搜索代理
GET /marketplace/search?query=coding

# 安装代理
POST /marketplace/package/{id}/install

# 获取精选代理
GET /marketplace/featured
```

### 成长仪表盘

```bash
# 获取成长指标
GET /dashboard/metrics

# 获取详细报告
GET /dashboard/report

# 获取成长分数
GET /dashboard/growth-score
```

### 经验学习

```bash
# 添加经验
POST /learning/experience
{
  "task": "完成项目开发",
  "result": "成功上线",
  "time_taken": "2h",
  "lesson": "要先做好技术方案评审",
  "category": "development",
  "success": true
}

# 获取成长报告
GET /learning/growth-report

# 获取建议
GET /learning/suggestions/写爬虫
```

### 数字分身

```bash
# 初始化
POST /digital-twin/initialize?name=我的分身

# 添加写作样本
POST /digital-twin/writing-samples
{"sample": "这是一个测试文本..."}

# 添加代码样本
POST /digital-twin/code-samples
{"sample": "def solution(): pass", "language": "python"}

# 记录决策
POST /digital-twin/decision
{
  "situation": "技术选型",
  "decision": "选择FastAPI",
  "reasoning": "异步性能好",
  "outcome": "开发效率提升"
}

# 获取个性化回复风格
GET /digital-twin/response-style/提问
```

### 推理引擎

```bash
# 思考推理
POST /brain/reason
{
  "context": "深度学习是机器学习的一个分支",
  "question": "深度学习和机器学习是什么关系"
}

# 链式思考
POST /brain/think
{"problem": "如何提高代码质量", "steps": 5}
```

### 任务规划

```bash
# 创建计划
POST /planner/plan
{"goal": "我要考研"}

# 完成任务
POST /planner/complete-task
{"plan_id": "...", "task_id": "..."}
```

### 技能执行

```bash
# 执行技能
POST /skills/execute
{
  "skill_name": "coding",
  "params": {
    "task": "实现快速排序",
    "language": "python"
  }
}
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | FastAPI + Python |
| 记忆存储 | JSON文件 / PostgreSQL |
| 知识图谱 | Neo4j (Cypher兼容) |
| 向量检索 | Milvus |
| 缓存 | Redis |
| 前端 | Next.js + TypeScript + TailwindCSS |
| 部署 | Docker / Kubernetes |

## 发展规划

| 版本 | 功能 |
|------|------|
| v0.1 | 聊天、记忆、知识库 |
| v0.5 | 任务规划、Agent、RAG |
| v0.8 | 多代理协作、目标树 |
| v1.0 | 认知记忆、Agent市场、成长仪表盘 |
| v2.0 | 数字分身完善 |
| v3.0 | 持续成长AI |

## 项目特点

1. **真正的AGI架构** - 不是LLM套壳，而是模拟人类认知
2. **会遗忘的系统** - 像人一样管理记忆，节省资源
3. **知识图谱推理** - 结构化实体关系，支持路径搜索
4. **经验驱动成长** - 每次任务都是学习的机会
5. **数字分身** - 逐渐训练出"另一个你"
6. **认知记忆系统** - Episodic/Semantic/Procedural三种记忆
7. **多代理协作** - 专业Agent团队协作
8. **Agent市场** - 像App Store一样的Agent生态
9. **目标树管理** - Career/Learning/Health/Project
10. **成长仪表盘** - 可视化成长轨迹

## 目录结构

```
TitanOS/
├── backend/
│   ├── app.py                 # FastAPI主入口
│   ├── requirements.txt       # Python依赖
│   ├── memory/               # 记忆系统
│   │   └── cognitive/        # 认知记忆
│   ├── brain/                # 推理引擎
│   ├── planner/              # 任务规划
│   ├── skills/               # 技能商店
│   ├── knowledge_graph/      # 知识图谱
│   ├── learning/             # 学习引擎
│   ├── digital_twin/         # 数字分身
│   ├── rag/                  # RAG引擎
│   ├── agent/                # Agent运行时
│   ├── reflection/           # 反思系统
│   ├── knowledge_base/       # 知识库
│   ├── auth/                 # 用户认证
│   ├── timeline/             # 记忆时间线
│   ├── dashboard/            # 成长仪表盘
│   ├── goal_tree/            # 目标树
│   ├── multi_agent/          # 多代理协作
│   └── marketplace/          # Agent市场
├── frontend/                 # Next.js前端
├── database/                 # 数据存储
└── docs/                     # 文档
    ├── API_REFERENCE.md      # API文档
    ├── DATABASE_DESIGN.md    # 数据库设计
    └── DEPLOYMENT.md         # 部署指南
```

## License

MIT License
