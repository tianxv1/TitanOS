from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import re


@dataclass
class ExtractedEntity:
    """从文本中提取的实体"""
    name: str
    entity_type: str
    confidence: float = 1.0
    position: Optional[Tuple[int, int]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractedRelation:
    """从文本中提取的关系"""
    from_entity: str
    to_entity: str
    relation_type: str
    confidence: float = 1.0
    sentence: Optional[str] = None


class LLMIntegrator:
    """LLM 集成器 - 用于实体关系提取和知识推理"""

    def __init__(self, model_type: str = "simulated"):
        self.model_type = model_type
        self.patterns = {
            "person": r"(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            "concept": r"(?:[\u4e00-\u9fa5]{2,}|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            "organization": r"(?:[\u4e00-\u9fa5]{2,}|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            "location": r"(?:[\u4e00-\u9fa5]{2,}(?:省|市|区|县|镇|村)|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
            "technology": r"(?:机器学习|深度学习|人工智能|神经网络|大数据|云计算|区块链|Python|Java|React|Vue)"
        }

        # 中文关系模式
        self.relation_patterns = [
            (r"(.+?)属于(.+?)", "BELONGS_TO"),
            (r"(.+?)是(.+?)", "IS_A"),
            (r"(.+?)包括(.+?)", "INCLUDES"),
            (r"(.+?)包含(.+?)", "CONTAINS"),
            (r"(.+?)导致(.+?)", "CAUSES"),
            (r"(.+?)影响(.+?)", "AFFECTS"),
            (r"(.+?)依赖(.+?)", "DEPENDS_ON"),
            (r"(.+?)使用(.+?)", "USES"),
            (r"(.+?)学习(.+?)", "LEARNS"),
            (r"(.+?)研究(.+?)", "RESEARCHES"),
            (r"(.+?)开发(.+?)", "DEVELOPS"),
            (r"(.+?)创建(.+?)", "CREATES"),
            (r"(.+?)发明(.+?)", "INVENTS"),
            (r"(.+?)发现(.+?)", "DISCOVERS"),
            (r"(.+?)位于(.+?)", "LOCATED_AT"),
            (r"(.+?)工作于(.+?)", "WORKS_AT"),
            (r"(.+?)学习于(.+?)", "STUDIES_AT"),
            (r"(.+?)喜欢(.+?)", "LIKES"),
            (r"(.+?)认识(.+?)", "KNOWS"),
            (r"(.+?)了解(.+?)", "KNOWS_ABOUT"),
            (r"(.+?)掌握(.+?)", "MASTERS"),
            (r"(.+?)精通(.+?)", "MASTERS"),
            (r"(.+?)擅长(.+?)", "SKILLED_IN"),
            (r"(.+?)相关于(.+?)", "RELATED_TO"),
        ]

    def extract_entities(self, text: str) -> List[ExtractedEntity]:
        """从文本中提取实体"""
        entities = []
        
        # 使用模式匹配提取技术相关概念
        for entity_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                name = match.group(0).strip()
                if len(name) < 2:
                    continue
                
                # 过滤掉常见的停用词
                if name in ["的", "了", "和", "是", "在", "有", "我", "他", "她", "它", "这", "那", "可以", "会", "可能"]:
                    continue
                
                # 检查是否已存在
                if not any(e.name == name for e in entities):
                    entities.append(ExtractedEntity(
                        name=name,
                        entity_type=entity_type,
                        confidence=0.8,
                        position=(match.start(), match.end())
                    ))

        # 添加自定义关键词识别
        keyword_mapping = {
            "机器学习": "concept",
            "深度学习": "concept",
            "人工智能": "concept",
            "神经网络": "concept",
            "大数据": "concept",
            "云计算": "concept",
            "区块链": "concept",
            "编程": "concept",
            "算法": "concept",
            "数据结构": "concept",
            "Python": "technology",
            "Java": "technology",
            "JavaScript": "technology",
            "React": "technology",
            "Vue": "technology",
            "TensorFlow": "technology",
            "PyTorch": "technology",
            "计算机": "concept",
            "软件": "concept",
            "系统": "concept",
            "模型": "concept",
            "框架": "concept",
            "工具": "concept",
        }

        for keyword, entity_type in keyword_mapping.items():
            if keyword in text:
                if not any(e.name == keyword for e in entities):
                    entities.append(ExtractedEntity(
                        name=keyword,
                        entity_type=entity_type,
                        confidence=0.9
                    ))

        return entities

    def extract_relations(self, text: str, entities: List[ExtractedEntity]) -> List[ExtractedRelation]:
        """从文本中提取实体之间的关系"""
        relations = []
        entity_names = [e.name for e in entities]

        for pattern, relation_type in self.relation_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                from_entity = match.group(1).strip()
                to_entity = match.group(2).strip()

                # 检查实体是否在提取的实体列表中
                if from_entity in entity_names and to_entity in entity_names:
                    # 避免重复关系
                    if not any(
                        r.from_entity == from_entity and r.to_entity == to_entity and r.relation_type == relation_type
                        for r in relations
                    ):
                        relations.append(ExtractedRelation(
                            from_entity=from_entity,
                            to_entity=to_entity,
                            relation_type=relation_type,
                            confidence=0.75,
                            sentence=match.group(0)
                        ))

        return relations

    def extract_from_text(self, text: str) -> Dict[str, Any]:
        """从文本中提取实体和关系"""
        entities = self.extract_entities(text)
        relations = self.extract_relations(text, entities)

        return {
            "entities": [e.__dict__ for e in entities],
            "relations": [r.__dict__ for r in relations],
            "text_length": len(text),
            "extracted_at": datetime.now().isoformat()
        }

    def generate_summary(self, entities: List[Dict], relations: List[Dict]) -> str:
        """根据实体和关系生成摘要"""
        if not entities:
            return "未提取到实体信息"

        summary = "知识图谱摘要：\n\n"
        summary += f"共识别到 {len(entities)} 个实体：\n"
        for entity in entities[:5]:
            summary += f"- {entity['name']} ({entity.get('entity_type', 'concept')})\n"

        if len(entities) > 5:
            summary += f"... 还有 {len(entities) - 5} 个实体\n"

        if relations:
            summary += f"\n共识别到 {len(relations)} 条关系：\n"
            for relation in relations[:5]:
                summary += f"- {relation['from_entity']} →{relation['relation_type']}→ {relation['to_entity']}\n"

            if len(relations) > 5:
                summary += f"... 还有 {len(relations) - 5} 条关系\n"

        return summary

    def reason(self, query: str, entities: List[Dict], relations: List[Dict]) -> str:
        """基于知识图谱进行简单推理"""
        # 简单的推理逻辑
        if "属于什么" in query or "是什么类型" in query:
            for entity_name in [e['name'] for e in entities]:
                if entity_name in query:
                    return f"{entity_name} 属于概念类别，可以进一步探索相关知识。"

        if "关系" in query or "联系" in query:
            if relations:
                return f"已找到 {len(relations)} 条关系，可以帮助理解实体之间的联系。"
            else:
                return "暂未找到明确的关系，可以尝试添加更多信息。"

        if "有哪些" in query or "包含" in query:
            if entities:
                entity_list = ", ".join([e['name'] for e in entities[:5]])
                return f"识别到的实体包括：{entity_list}..."
            else:
                return "暂未识别到实体。"

        return "可以根据知识图谱中的实体和关系进行分析推理。"

    def generate_cypher_query(self, entities: List[str], relation_type: Optional[str] = None) -> str:
        """生成 Cypher 查询语句"""
        if not entities:
            return "MATCH (n) RETURN n LIMIT 10"

        if len(entities) == 1:
            query = f"MATCH (n {{name: '{entities[0]}'}})-[r]-(m) RETURN n, r, m"
        elif len(entities) == 2:
            if relation_type:
                query = f"MATCH (a {{name: '{entities[0]}'}})-[r:{relation_type}]-(b {{name: '{entities[1]}'}}) RETURN a, r, b"
            else:
                query = f"MATCH path = shortestPath((a {{name: '{entities[0]}'}})-[*1..5]-(b {{name: '{entities[1]}'}})) RETURN path"
        else:
            names_str = ", ".join([f"'{e}'" for e in entities])
            query = f"MATCH (n) WHERE n.name IN [{names_str}] RETURN n"

        return query

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """完整分析文本，提取实体、关系并生成洞察"""
        result = self.extract_from_text(text)
        result["summary"] = self.generate_summary(result["entities"], result["relations"])
        result["cypher_query"] = self.generate_cypher_query([e["name"] for e in result["entities"]])
        
        return result