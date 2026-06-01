from typing import List, Optional, Dict, Any, Tuple
from .entities import Entity, Relation, RELATION_TYPES
from .neo4j_provider import Neo4jProvider
from .llm_integrator import LLMIntegrator
import json
import os


class KnowledgeGraph:
    def __init__(self, storage_path: str = "database/knowledge_graph.json",
                 use_neo4j: bool = False, neo4j_config: Optional[Dict] = None,
                 llm_model: str = "simulated"):
        self.storage_path = storage_path
        self.entities: Dict[str, Entity] = {}
        self.relations: Dict[str, Relation] = {}
        self.entity_index: Dict[str, List[str]] = {}
        
        # Neo4j 集成
        self.use_neo4j = use_neo4j
        self.neo4j_provider = None
        if use_neo4j and neo4j_config:
            self.neo4j_provider = Neo4jProvider(**neo4j_config)
            self.neo4j_provider.connect()
        
        # LLM 集成
        self.llm_integrator = LLMIntegrator(model_type=llm_model)
        
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for e_data in data.get("entities", []):
                        entity = Entity.from_dict(e_data)
                        self.entities[entity.id] = entity
                        self._index_entity(entity)

                    for r_data in data.get("relations", []):
                        relation = Relation.from_dict(r_data)
                        self.relations[relation.id] = relation
            except Exception:
                pass

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "entities": [e.to_dict() for e in self.entities.values()],
            "relations": [r.to_dict() for r in self.relations.values()],
            "saved_at": str(self._get_timestamp())
        }
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

    def _index_entity(self, entity: Entity):
        name_lower = entity.name.lower()
        if name_lower not in self.entity_index:
            self.entity_index[name_lower] = []
        if entity.id not in self.entity_index[name_lower]:
            self.entity_index[name_lower].append(entity.id)

        if entity.entity_type not in self.entity_index:
            self.entity_index[entity.entity_type] = []
        if entity.id not in self.entity_index[entity.entity_type]:
            self.entity_index[entity.entity_type].append(entity.id)

    def add_entity(self, name: str, entity_type: str = "concept",
                   description: str = "", properties: Optional[Dict] = None,
                   memory_id: Optional[str] = None) -> Entity:
        existing = self.find_entity_by_name(name)
        if existing:
            return existing

        entity = Entity(
            name=name,
            entity_type=entity_type,
            description=description,
            properties=properties or {},
            memory_id=memory_id
        )
        self.entities[entity.id] = entity
        self._index_entity(entity)
        
        # 同步到 Neo4j
        if self.use_neo4j and self.neo4j_provider:
            self.neo4j_provider.create_entity(entity)
        
        self._save()
        return entity

    def find_entity_by_name(self, name: str) -> Optional[Entity]:
        # 先从内存查找
        name_lower = name.lower()
        entity_ids = self.entity_index.get(name_lower, [])
        if entity_ids:
            return self.entities.get(entity_ids[0])
        
        # 如果启用了 Neo4j，从 Neo4j 查找
        if self.use_neo4j and self.neo4j_provider:
            entity = self.neo4j_provider.find_entity_by_name(name)
            if entity:
                self.entities[entity.id] = entity
                self._index_entity(entity)
                return entity
        
        return None

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        # 先从内存查找
        if entity_id in self.entities:
            return self.entities[entity_id]
        
        # 如果启用了 Neo4j，从 Neo4j 查找
        if self.use_neo4j and self.neo4j_provider:
            entity = self.neo4j_provider.get_entity(entity_id)
            if entity:
                self.entities[entity_id] = entity
                self._index_entity(entity)
                return entity
        
        return None

    def update_entity(self, entity_id: str, **kwargs) -> Optional[Entity]:
        entity = self.entities.get(entity_id)
        if not entity:
            return None

        if "name" in kwargs:
            entity.name = kwargs["name"]
        if "entity_type" in kwargs:
            entity.entity_type = kwargs["entity_type"]
        if "description" in kwargs:
            entity.description = kwargs["description"]
        if "properties" in kwargs:
            entity.properties.update(kwargs["properties"])

        entity.updated_at = self._get_timestamp()
        self._save()
        return entity

    def delete_entity(self, entity_id: str) -> bool:
        if entity_id not in self.entities:
            return False

        relations_to_delete = [
            rid for rid, r in self.relations.items()
            if r.from_entity_id == entity_id or r.to_entity_id == entity_id
        ]
        for rid in relations_to_delete:
            del self.relations[rid]

        del self.entities[entity_id]
        self._save()
        return True

    def add_relation(self, from_entity_id: str, to_entity_id: str,
                     relation_type: str, weight: float = 1.0,
                     properties: Optional[Dict] = None) -> Optional[Relation]:
        if relation_type not in RELATION_TYPES:
            relation_type = "RELATED_TO"

        existing = self.find_relation(from_entity_id, to_entity_id, relation_type)
        if existing:
            return existing

        relation = Relation(
            from_entity_id=from_entity_id,
            to_entity_id=to_entity_id,
            relation_type=relation_type,
            weight=weight,
            properties=properties or {}
        )
        self.relations[relation.id] = relation
        
        # 同步到 Neo4j
        if self.use_neo4j and self.neo4j_provider:
            self.neo4j_provider.create_relation(relation)
        
        self._save()
        return relation

    def find_relation(self, from_id: str, to_id: str,
                      relation_type: Optional[str] = None) -> Optional[Relation]:
        for relation in self.relations.values():
            if relation.from_entity_id == from_id and relation.to_entity_id == to_id:
                if relation_type is None or relation.relation_type == relation_type:
                    return relation
        return None

    def get_relations(self, entity_id: str,
                      relation_type: Optional[str] = None) -> List[Relation]:
        results = []
        for relation in self.relations.values():
            if relation.from_entity_id == entity_id or relation.to_entity_id == entity_id:
                if relation_type is None or relation.relation_type == relation_type:
                    results.append(relation)
        
        # 如果启用了 Neo4j，补充从 Neo4j 获取的关系
        if self.use_neo4j and self.neo4j_provider:
            neo4j_relations = self.neo4j_provider.get_relations(entity_id, relation_type)
            for rel in neo4j_relations:
                if rel.id not in self.relations:
                    results.append(rel)
        
        return results

    def get_neighbors(self, entity_id: str, depth: int = 1,
                      relation_type: Optional[str] = None) -> List[Tuple[Entity, Relation]]:
        neighbors = []
        visited = {entity_id}
        self._find_neighbors_recursive(entity_id, depth, visited, neighbors, relation_type)
        return neighbors

    def _find_neighbors_recursive(self, entity_id: str, remaining_depth: int,
                                  visited: set, results: list,
                                  relation_type: Optional[str] = None):
        if remaining_depth <= 0:
            return

        for relation in self.relations.values():
            if relation.from_entity_id == entity_id:
                neighbor_id = relation.to_entity_id
                if neighbor_id not in visited:
                    neighbor = self.entities.get(neighbor_id)
                    if neighbor:
                        visited.add(neighbor_id)
                        results.append((neighbor, relation))
                        self._find_neighbors_recursive(neighbor_id, remaining_depth - 1,
                                                       visited, results, relation_type)
            elif relation.to_entity_id == entity_id:
                neighbor_id = relation.from_entity_id
                if neighbor_id not in visited:
                    neighbor = self.entities.get(neighbor_id)
                    if neighbor:
                        visited.add(neighbor_id)
                        results.append((neighbor, relation))
                        self._find_neighbors_recursive(neighbor_id, remaining_depth - 1,
                                                       visited, results, relation_type)

    def find_path(self, from_entity_id: str, to_entity_id: str,
                  max_depth: int = 5) -> List[List[Tuple[Entity, Relation]]]:
        # 先尝试内存中的路径查找
        paths = []
        visited = set()

        def dfs(current_id: str, target_id: str, path: List[Tuple[Entity, Relation]], depth: int):
            if depth > max_depth:
                return
            if current_id == target_id:
                paths.append(path.copy())
                return

            for relation in self.relations.values():
                if relation.from_entity_id == current_id and relation.from_entity_id not in visited:
                    neighbor = self.entities.get(relation.to_entity_id)
                    if neighbor:
                        visited.add(current_id)
                        path.append((neighbor, relation))
                        dfs(relation.to_entity_id, target_id, path, depth + 1)
                        path.pop()
                        visited.remove(current_id)

                elif relation.to_entity_id == current_id and relation.to_entity_id not in visited:
                    neighbor = self.entities.get(relation.from_entity_id)
                    if neighbor:
                        visited.add(current_id)
                        path.append((neighbor, relation))
                        dfs(relation.from_entity_id, target_id, path, depth + 1)
                        path.pop()
                        visited.remove(current_id)

        dfs(from_entity_id, to_entity_id, [], 0)
        
        # 如果启用了 Neo4j，补充从 Neo4j 获取的路径
        if self.use_neo4j and self.neo4j_provider and not paths:
            neo4j_paths = self.neo4j_provider.find_path(from_entity_id, to_entity_id, max_depth)
            if neo4j_paths:
                # 将 Neo4j 路径转换为本地格式
                for path_data in neo4j_paths:
                    local_path = []
                    for item in path_data:
                        if item["type"] == "node":
                            entity = self.get_entity(item["id"])
                            if entity:
                                local_path.append((entity, None))
                        elif item["type"] == "relation":
                            # 找到对应的关系
                            for rel in self.relations.values():
                                if rel.id == item["id"]:
                                    # 更新路径中的关系
                                    if local_path:
                                        local_path[-1] = (local_path[-1][0], rel)
                                    break
                    paths.append([p for p in local_path if p[1] is not None])
        
        return paths

    def query(self, entity_name: Optional[str] = None,
              entity_type: Optional[str] = None,
              relation_type: Optional[str] = None) -> Dict[str, Any]:
        results = {
            "entities": [],
            "relations": []
        }

        if entity_name:
            entity = self.find_entity_by_name(entity_name)
            if entity:
                results["entities"].append(entity.to_dict())
                results["relations"] = [r.to_dict() for r in self.get_relations(entity.id, relation_type)]

        elif entity_type:
            entity_ids = self.entity_index.get(entity_type, [])
            for eid in entity_ids:
                entity = self.entities.get(eid)
                if entity:
                    results["entities"].append(entity.to_dict())

        elif relation_type:
            for relation in self.relations.values():
                if relation.relation_type == relation_type:
                    results["relations"].append(relation.to_dict())

        else:
            results["entities"] = [e.to_dict() for e in self.entities.values()]
            results["relations"] = [r.to_dict() for r in self.relations.values()]

        return results

    def extract_from_text(self, text: str, use_llm: bool = True) -> Dict[str, Any]:
        """使用 LLM 从文本中提取实体和关系"""
        if use_llm and self.llm_integrator:
            return self.llm_integrator.analyze_text(text)
        
        # 回退到简单提取
        extracted = {
            "entities": [],
            "relations": []
        }

        import re
        patterns = {
            "person": r"(?:[A-Z][a-z]+ [A-Z][a-z]+)",
            "concept": r"(?:[A-Z][a-z]+(?: [A-Z][a-z]+)*)",
            "organization": r"(?:[A-Z][a-z]+(?: [A-Z][a-z]+)*)",
        }

        concept_keywords = ["机器学习", "深度学习", "人工智能", "计算机", "编程", "算法"]
        for keyword in concept_keywords:
            if keyword in text:
                entity = self.add_entity(keyword, "concept", f"从文本提取: {text[:100]}")
                extracted["entities"].append(entity.to_dict())

        if "属于" in text or "属于" in text:
            parts = re.split(r"属于", text)
            if len(parts) == 2:
                entity1 = self.add_entity(parts[0].strip(), "concept")
                entity2 = self.add_entity(parts[1].strip(), "concept")
                relation = self.add_relation(entity1.id, entity2.id, "BELONGS_TO")
                if relation:
                    extracted["entities"].append(entity1.to_dict())
                    extracted["entities"].append(entity2.to_dict())
                    extracted["relations"].append(relation.to_dict())

        return extracted

    def get_stats(self) -> Dict[str, Any]:
        entity_types: Dict[str, int] = {}
        relation_types: Dict[str, int] = {}

        for entity in self.entities.values():
            entity_types[entity.entity_type] = entity_types.get(entity.entity_type, 0) + 1

        for relation in self.relations.values():
            relation_types[relation.relation_type] = relation_types.get(relation.relation_type, 0) + 1

        stats = {
            "total_entities": len(self.entities),
            "total_relations": len(self.relations),
            "entity_types": entity_types,
            "relation_types": relation_types,
            "use_neo4j": self.use_neo4j,
            "neo4j_connected": self.neo4j_provider.connected if self.neo4j_provider else False
        }

        # 如果启用了 Neo4j，补充 Neo4j 统计
        if self.use_neo4j and self.neo4j_provider:
            neo4j_stats = self.neo4j_provider.get_stats()
            stats["neo4j"] = neo4j_stats

        return stats

    def get_graph(self) -> Dict[str, Any]:
        """获取知识图谱的完整数据（用于前端可视化）"""
        nodes = []
        edges = []
        
        # 构建节点列表
        for entity in self.entities.values():
            nodes.append({
                "id": entity.id,
                "label": entity.name,
                "type": entity.entity_type,
                "description": entity.description,
                "properties": entity.properties
            })
        
        # 构建边列表
        for relation in self.relations.values():
            edges.append({
                "id": relation.id,
                "source": relation.from_entity_id,
                "target": relation.to_entity_id,
                "type": relation.relation_type,
                "weight": relation.weight,
                "properties": relation.properties
            })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "total_nodes": len(nodes),
            "total_edges": len(edges)
        }

    def export_to_cypher(self) -> List[str]:
        cypher_statements = []

        for entity in self.entities.values():
            props = json.dumps(entity.properties, ensure_ascii=False)
            statement = (
                f"CREATE (e:{entity.entity_type} {{"
                f"id: '{entity.id}', "
                f"name: '{entity.name}', "
                f"description: '{entity.description}', "
                f"properties: {props}"
                f"}})"
            )
            cypher_statements.append(statement)

        for relation in self.relations.values():
            statement = (
                f"MATCH (a), (b) WHERE a.id = '{relation.from_entity_id}' AND b.id = '{relation.to_entity_id}' "
                f"CREATE (a)-[r:{relation.relation_type} {{weight: {relation.weight}}}]->(b)"
            )
            cypher_statements.append(statement)

        return cypher_statements

    def sync_to_neo4j(self) -> Dict[str, int]:
        """同步本地数据到 Neo4j"""
        if not self.use_neo4j or not self.neo4j_provider:
            return {"error": "Neo4j not configured"}

        entities = list(self.entities.values())
        relations = list(self.relations.values())
        
        return self.neo4j_provider.batch_import(entities, relations)

    def execute_cypher(self, query: str) -> List[Dict[str, Any]]:
        """执行 Cypher 查询（仅当启用 Neo4j 时可用）"""
        if not self.use_neo4j or not self.neo4j_provider:
            return [{"error": "Neo4j not configured"}]
        
        return self.neo4j_provider.execute_cypher(query)