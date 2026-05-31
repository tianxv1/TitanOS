# TitanOS v0.2

> 世界上第一个能持续成长的个人AI操作系统

## 核心理念

不同于ChatGPT套壳或Agent套壳，TitanOS是一个会成长的AI系统，模拟人类的认知架构：

```
用户 → 感知层 → 记忆层 → 思考层 → 规划层 → 执行层 → 学习层
```

## 系统架构

```
TitanOS/
├── Gateway           # API网关 (FastAPI)
├── Brain            # 推理引擎
├── Memory           # 记忆系统（带遗忘机制）
├── KnowledgeGraph   # 知识图谱 (Neo4j兼容)
├── Planner          # 任务规划器
├── Executor         # 执行器
├── Learning         # 学习引擎（经验驱动成长）
├── SkillStore       # 技能商店
└── DigitalTwin      # 数字分身
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

### Memory Engine (记忆引擎)

AI不是保存所有记忆，而是像人一样遗忘。

```python
score = importance * 0.6 + access_count * 0.3 + recent_score * 0.1
```

- **低分记忆** → 自动删除
- **高分记忆** → 永久保留
- **经验存储** → 任务完成后自动总结

### Brain (推理引擎)

- 问题分析与类型识别
- 链式推理 (Chain of Thought)
- 逻辑推断与假设验证

### Planner (任务规划器)

自动将目标拆解为可执行的任务树：

```json
{
  "goal": "我要考研",
  "milestones": [
    {"title": "确定目标学校", "tasks": [...]},
    {"title": "制定复习计划", "tasks": [...]}
  ]
}
```

### KnowledgeGraph (知识图谱)

将记忆和外部信息结构化为实体关系图：

```
张三 -[喜欢]-> 机器学习
机器学习 -[属于]-> 人工智能
人工智能 -[研究]-> Deep Learning
```

**支持的关系类型**: KNOWS, LIKES, BELONGS_TO, PART_OF, CAUSES, RELATED_TO, LEADS_TO, DEPENDS_ON, WORKS_AT, STUDIES, CREATED_BY, LOCATED_AT

### Learning Engine (经验学习)

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

### Digital Twin (数字分身)

记录用户风格，为AI提供个性化决策：

- **写作风格**: 正式程度、语气、常用短语
- **代码风格**: 语言偏好、命名规范、错误处理方式
- **决策模式**:  ситуация → 决策 → 结果
- **学习习惯**: 学科、时间偏好、学习方法

### Skill Store (技能商店)

类似App Store的技能生态系统：

| 技能 | 描述 |
|------|------|
| search | 搜索互联网获取信息 |
| coding | 辅助编程和代码审查 |
| math | 数学计算和公式推导 |
| translate | 文本翻译 |

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
| v0.5 | 任务规划、Agent |
| v1.0 | 长期学习、经验积累 |
| v2.0 | 数字分身 |
| v3.0 | 持续成长AI |

## 项目特点

1. **真正的AGI架构** - 不是LLM套壳，而是模拟人类认知
2. **会遗忘的系统** - 像人一样管理记忆，节省资源
3. **知识图谱推理** - 结构化实体关系，支持路径搜索
4. **经验驱动成长** - 每次任务都是学习的机会
5. **数字分身** - 逐渐训练出"另一个你"
6. **可扩展的技能系统** - 支持自定义技能注册

## 目录结构

```
TitanOS/
├── backend/
│   ├── app.py                 # FastAPI主入口
│   ├── requirements.txt       # Python依赖
│   ├── memory/               # 记忆系统
│   ├── brain/                # 推理引擎
│   ├── planner/              # 任务规划
│   ├── skills/               # 技能商店
│   ├── knowledge_graph/      # 知识图谱
│   ├── learning/             # 学习引擎
│   └── digital_twin/         # 数字分身
├── frontend/                 # Next.js前端
├── database/                 # 数据存储
└── docs/                     # 文档
```

## License

MIT License
