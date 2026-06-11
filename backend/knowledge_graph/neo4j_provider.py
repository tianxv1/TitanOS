from typing import List, Optional, Dict, Any
from neo4j import GraphDatabase
from .entities import Entity, Relation, RELATION_TYPES
import json
import uuid


class Neo4jProvider:
    """Neo4j 图数据库集成提供器"""

    def __init__(self, uri: str = "bolt://localhost:7687",
                 username: str = "neo4j", password: str = "password",
                 database: str = "neo4j"):
        self.uri = uri
        self.username = username
        self.password = password
        self.database = database
        self.driver = None
        self.connected = False

    def connect(self) -> bool:
        """连接到 Neo4j 数据库"""
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password),
                database=self.database
            )
            with self.driver.session(database=self.database) as session:
                session.run("RETURN 1")
            self.connected = True
            return True
        except Exception as e:
            print(f"Neo4j connection failed: {e}")
            return False

    def disconnect(self):
        """断开连接"""
        if self.driver:
            self.driver.close()
            self.connected = False

    def _validate_label(self, label: str) -> bool:
        """验证标签名称是否合法"""
        if not label or not isinstance(label, str):
            return False
        return label.replace("_", "").isalnum()

    def create_entity(self, entity: Entity) -> bool:
        """在 Neo4j 中创建实体"""
        if not self.connected:
            return False

        try:
            label = entity.entity_type
            if not self._validate_label(label):
                print(f"Invalid label: {label}")
                return False

            with self.driver.session(database=self.database) as session:
                query = f"""
                    CREATE (e:`{label}` {{
                        id: $id,
                        name: $name,
                        description: $description,
                        properties: $properties,
                        created_at: $created_at,
                        memory_id: $memory_id
                    }})
                    RETURN e
                """
                session.run(query,
                           id=entity.id,
                           name=entity.name,
                           description=entity.description,
                           properties=json.dumps(entity.properties),
                           created_at=entity.created_at.isoformat(),
                           memory_id=entity.memory_id or "")
            return True
        except Exception as e:
            print(f"Failed to create entity: {e}")
            return False

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """从 Neo4j 获取实体"""
        if not self.connected:
            return None

        try:
            with self.driver.session(database=self.database) as session:
                query = """
                    MATCH (e) WHERE e.id = $id
                    RETURN e, labels(e) as labels
                """
                result = session.run(query, id=entity_id).single()
                if result:
                    record = result["e"]
                    labels = result["labels"]
                    return Entity(
                        id=record["id"],
                        name=record["name"],
                        entity_type=labels[0] if labels else "concept",
                        description=record["description"],
                        properties=json.loads(record["properties"]) if record["properties"] else {},
                        memory_id=record.get("memory_id")
                    )
            return None
        except Exception as e:
            print(f"Failed to get entity: {e}")
            return None

    def find_entity_by_name(self, name: str) -> Optional[Entity]:
        """按名称查找实体"""
        if not self.connected:
            return None

        try:
            with self.driver.session(database=self.database) as session:
                query = """
                    MATCH (e) WHERE e.name = $name
                    RETURN e, labels(e) as labels
                """
                result = session.run(query, name=name).single()
                if result:
                    record = result["e"]
                    labels = result["labels"]
                    return Entity(
                        id=record["id"],
                        name=record["name"],
                        entity_type=labels[0] if labels else "concept",
                        description=record["description"],
                        properties=json.loads(record["properties"]) if record["properties"] else {}
                    )
            return None
        except Exception as e:
            print(f"Failed to find entity: {e}")
            return None

    def create_relation(self, relation: Relation) -> bool:
        """创建关系"""
        if not self.connected:
            return False

        try:
            rel_type = relation.relation_type
            if not self._validate_label(rel_type):
                print(f"Invalid relation type: {rel_type}")
                return False

            with self.driver.session(database=self.database) as session:
                query = f"""
                    MATCH (a), (b)
                    WHERE a.id = $from_id AND b.id = $to_id
                    CREATE (a)-[r:`{rel_type}` {{
                        id: $id,
                        weight: $weight,
                        properties: $properties,
                        created_at: $created_at
                    }}]->(b)
                    RETURN r
                """
                session.run(query,
                           from_id=relation.from_entity_id,
                           to_id=relation.to_entity_id,
                           id=relation.id,
                           weight=relation.weight,
                           properties=json.dumps(relation.properties),
                           created_at=relation.created_at.isoformat())
            return True
        except Exception as e:
            print(f"Failed to create relation: {e}")
            return False

    def get_relations(self, entity_id: str, relation_type: Optional[str] = None) -> List[Relation]:
        """获取实体的关系"""
        if not self.connected:
            return []

        try:
            with self.driver.session(database=self.database) as session:
                if relation_type:
                    if not self._validate_label(relation_type):
                        print(f"Invalid relation type: {relation_type}")
                        return []
                    
                    query = f"""
                        MATCH (a)-[r:`{relation_type}`]-(b)
                        WHERE a.id = $id OR b.id = $id
                        RETURN r, a.id as from_id, b.id as to_id
                    """
                    result = session.run(query, id=entity_id)
                else:
                    query = """
                        MATCH (a)-[r]-(b)
                        WHERE a.id = $id OR b.id = $id
                        RETURN r, a.id as from_id, b.id as to_id
                    """
                    result = session.run(query, id=entity_id)

                relations = []
                for record in result:
                    r = record["r"]
                    from_id = record["from_id"]
                    to_id = record["to_id"]
                    relations.append(Relation(
                        id=r["id"],
                        from_entity_id=from_id,
                        to_entity_id=to_id,
                        relation_type=r.type,
                        weight=r["weight"],
                        properties=json.loads(r["properties"]) if r["properties"] else {}
                    ))
                return relations
        except Exception as e:
            print(f"Failed to get relations: {e}")
            return []

    def find_path(self, from_id: str, to_id: str, max_depth: int = 5) -> List[List[Dict]]:
        """查找两个实体之间的路径"""
        if not self.connected:
            return []

        try:
            with self.driver.session(database=self.database) as session:
                query = """
                    MATCH path = shortestPath((a)-[*1..$max_depth]-(b))
                    WHERE a.id = $from_id AND b.id = $to_id
                    RETURN nodes(path) as nodes, relationships(path) as rels
                """
                result = session.run(query, from_id=from_id, to_id=to_id, max_depth=max_depth).single()
                if result:
                    paths = []
                    nodes = result["nodes"]
                    rels = result["rels"]
                    path_data = []
                    for i, node in enumerate(nodes):
                        path_data.append({
                            "type": "node",
                            "id": node["id"],
                            "name": node["name"],
                            "labels": list(node.labels)
                        })
                        if i < len(rels):
                            rel = rels[i]
                            path_data.append({
                                "type": "relation",
                                "id": rel["id"],
                                "type": rel.type,
                                "weight": rel["weight"]
                            })
                    paths.append(path_data)
                    return paths
            return []
        except Exception as e:
            print(f"Failed to find path: {e}")
            return []

    def execute_cypher(self, query: str) -> List[Dict[str, Any]]:
        """执行 Cypher 查询"""
        if not self.connected:
            return []

        try:
            with self.driver.session(database=self.database) as session:
                result = session.run(query)
                return [dict(record) for record in result]
        except Exception as e:
            print(f"Cypher query failed: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self.connected:
            return {"error": "Not connected"}

        try:
            with self.driver.session(database=self.database) as session:
                node_count = session.run("MATCH (n) RETURN count(n) as count").single()["count"]
                rel_count = session.run("MATCH ()-[r]->() RETURN count(r) as count").single()["count"]

                label_stats = session.run("""
                    MATCH (n)
                    RETURN labels(n)[0] as label, count(n) as count
                    ORDER BY count DESC
                """)
                entity_types = {record["label"]: record["count"] for record in label_stats}

                rel_type_stats = session.run("""
                    MATCH ()-[r]->()
                    RETURN type(r) as type, count(r) as count
                    ORDER BY count DESC
                """)
                relation_types = {record["type"]: record["count"] for record in rel_type_stats}

            return {
                "total_nodes": node_count,
                "total_relations": rel_count,
                "entity_types": entity_types,
                "relation_types": relation_types,
                "status": "connected"
            }
        except Exception as e:
            print(f"Failed to get stats: {e}")
            return {"error": str(e)}

    def batch_import(self, entities: List[Entity], relations: List[Relation]) -> Dict[str, int]:
        """批量导入实体和关系"""
        if not self.connected:
            return {"entities_created": 0, "relations_created": 0}

        entities_created = 0
        relations_created = 0

        try:
            with self.driver.session(database=self.database) as session:
                for entity in entities:
                    try:
                        label = entity.entity_type
                        if not self._validate_label(label):
                            continue
                        
                        query = f"""
                            CREATE (e:`{label}` {{
                                id: $id,
                                name: $name,
                                description: $description,
                                properties: $properties,
                                created_at: $created_at,
                                memory_id: $memory_id
                            }})
                        """
                        session.run(query,
                                   id=entity.id,
                                   name=entity.name,
                                   description=entity.description,
                                   properties=json.dumps(entity.properties),
                                   created_at=entity.created_at.isoformat(),
                                   memory_id=entity.memory_id or "")
                        entities_created += 1
                    except:
                        pass

                for relation in relations:
                    try:
                        rel_type = relation.relation_type
                        if not self._validate_label(rel_type):
                            continue
                            
                        query = f"""
                            MATCH (a), (b)
                            WHERE a.id = $from_id AND b.id = $to_id
                            MERGE (a)-[r:`{rel_type}` {{id: $id}}]->(b)
                            ON CREATE SET r.weight = $weight, r.properties = $properties, r.created_at = $created_at
                        """
                        session.run(query,
                                   from_id=relation.from_entity_id,
                                   to_id=relation.to_entity_id,
                                   id=relation.id,
                                   weight=relation.weight,
                                   properties=json.dumps(relation.properties),
                                   created_at=relation.created_at.isoformat())
                        relations_created += 1
                    except:
                        pass

            return {"entities_created": entities_created, "relations_created": relations_created}
        except Exception as e:
            print(f"Batch import failed: {e}")
            return {"entities_created": entities_created, "relations_created": relations_created}

    # ============ 数字分身相关方法 ============

    def create_digital_twin(self, twin_id: str, name: str, personality_data: Dict[str, Any]) -> bool:
        """创建数字分身节点"""
        if not self.connected:
            return False

        try:
            with self.driver.session(database=self.database) as session:
                query = """
                    CREATE (dt:DigitalTwin {
                        id: $id,
                        name: $name,
                        personality: $personality,
                        created_at: timestamp(),
                        last_updated: timestamp()
                    })
                    RETURN dt
                """
                session.run(query,
                           id=twin_id,
                           name=name,
                           personality=json.dumps(personality_data))
            return True
        except Exception as e:
            print(f"Failed to create digital twin: {e}")
            return False

    def update_digital_twin(self, twin_id: str, updates: Dict[str, Any]) -> bool:
        """更新数字分身信息"""
        if not self.connected:
            return False

        try:
            with self.driver.session(database=self.database) as session:
                set_clause = ", ".join([f"dt.{key} = ${key}" for key in updates.keys() if key != "personality"])
                query = f"""
                    MATCH (dt:DigitalTwin {{id: $twin_id}})
                    SET dt.last_updated = timestamp()
                    {f", dt.personality = $personality" if "personality" in updates else ""}
                    {f", {set_clause}" if set_clause else ""}
                """
                params = {"twin_id": twin_id, "last_updated": "timestamp()"}
                params.update(updates)
                if "personality" in params:
                    params["personality"] = json.dumps(params["personality"])
                session.run(query, **params)
            return True
        except Exception as e:
            print(f"Failed to update digital twin: {e}")
            return False

    def get_digital_twin(self, twin_id: str) -> Optional[Dict[str, Any]]:
        """获取数字分身信息"""
        if not self.connected:
            return None

        try:
            with self.driver.session(database=self.database) as session:
                query = """
                    MATCH (dt:DigitalTwin {id: $id})
                    RETURN dt
                """
                result = session.run(query, id=twin_id).single()
                if result:
                    dt = result["dt"]
                    return {
                        "id": dt["id"],
                        "name": dt["name"],
                        "personality": json.loads(dt["personality"]) if dt["personality"] else {},
                        "created_at": dt.get("created_at"),
                        "last_updated": dt.get("last_updated")
                    }
            return None
        except Exception as e:
            print(f"Failed to get digital twin: {e}")
            return None

    def get_all_digital_twins(self) -> List[Dict[str, Any]]:
        """获取所有数字分身"""
        if not self.connected:
            return []

        try:
            with self.driver.session(database=self.database) as session:
                query = """
                    MATCH (dt:DigitalTwin)
                    RETURN dt
                    ORDER BY dt.created_at DESC
                """
                results = []
                for record in session.run(query):
                    dt = record["dt"]
                    results.append({
                        "id": dt["id"],
                        "name": dt["name"],
                        "personality": json.loads(dt["personality"]) if dt["personality"] else {},
                        "created_at": dt.get("created_at"),
                        "last_updated": dt.get("last_updated")
                    })
                return results
        except Exception as e:
            print(f"Failed to get digital twins: {e}")
            return []

    def add_twin_knowledge(self, twin_id: str, entity_id: str, confidence: float = 1.0) -> bool:
        """为数字分身添加知识关联"""
        if not self.connected:
            return False

        try:
            with self.driver.session(database=self.database) as session:
                query = """
                    MATCH (dt:DigitalTwin {id: $twin_id}), (e) WHERE e.id = $entity_id
                    MERGE (dt)-[r:KNOWS {confidence: $confidence, created_at: timestamp()}]->(e)
                    ON MATCH SET r.confidence = $confidence
                    RETURN r
                """
                session.run(query, twin_id=twin_id, entity_id=entity_id, confidence=confidence)
            return True
        except Exception as e:
            print(f"Failed to add twin knowledge: {e}")
            return False

    def get_twin_knowledge(self, twin_id: str) -> List[Dict[str, Any]]:
        """获取数字分身的知识关联"""
        if not self.connected:
            return []

        try:
            with self.driver.session(database=self.database) as session:
                query = """
                    MATCH (dt:DigitalTwin {id: $twin_id})-[r:KNOWS]->(e)
                    RETURN e, r.confidence, r.created_at
                    ORDER BY r.confidence DESC
                """
                results = []
                for record in session.run(query, twin_id=twin_id):
                    e = record["e"]
                    results.append({
                        "entity_id": e["id"],
                        "entity_name": e["name"],
                        "entity_type": list(e.labels)[0] if e.labels else "concept",
                        "confidence": record["confidence"],
                        "created_at": record["created_at"]
                    })
                return results
        except Exception as e:
            print(f"Failed to get twin knowledge: {e}")
            return []

    def record_twin_interaction(self, twin_id: str, interaction_type: str,
                                context: str, response: str, feedback: float = 0.0) -> bool:
        """记录数字分身的交互记录"""
        if not self.connected:
            return False

        try:
            with self.driver.session(database=self.database) as session:
                query = """
                    MATCH (dt:DigitalTwin {id: $twin_id})
                    CREATE (i:Interaction {
                        id: $interaction_id,
                        type: $type,
                        context: $context,
                        response: $response,
                        feedback: $feedback,
                        timestamp: timestamp()
                    })
                    CREATE (dt)-[r:HAS_INTERACTION]->(i)
                    RETURN i
                """
                session.run(query,
                           twin_id=twin_id,
                           interaction_id=str(uuid.uuid4()),
                           type=interaction_type,
                           context=context,
                           response=response,
                           feedback=feedback)
            return True
        except Exception as e:
            print(f"Failed to record interaction: {e}")
            return False

    def get_twin_interactions(self, twin_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """获取数字分身的交互历史"""
        if not self.connected:
            return []

        try:
            with self.driver.session(database=self.database) as session:
                query = """
                    MATCH (dt:DigitalTwin {id: $twin_id})-[r:HAS_INTERACTION]->(i:Interaction)
                    RETURN i
                    ORDER BY i.timestamp DESC
                    LIMIT $limit
                """
                results = []
                for record in session.run(query, twin_id=twin_id, limit=limit):
                    i = record["i"]
                    results.append({
                        "id": i["id"],
                        "type": i["type"],
                        "context": i["context"],
                        "response": i["response"],
                        "feedback": i["feedback"],
                        "timestamp": i["timestamp"]
                    })
                return results
        except Exception as e:
            print(f"Failed to get interactions: {e}")
            return []

    def find_personality_matches(self, personality_profile: Dict[str, float],
                                 similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """查找具有相似性格的数字分身"""
        if not self.connected:
            return []

        try:
            with self.driver.session(database=self.database) as session:
                query = """
                    MATCH (dt:DigitalTwin)
                    RETURN dt.id as id, dt.name as name, dt.personality as personality_str
                    LIMIT 20
                """
                results = []
                for record in session.run(query):
                    try:
                        personality = json.loads(record["personality_str"]) if record["personality_str"] else {}
                        similarity = self._calculate_personality_similarity(
                            personality_profile,
                            personality
                        )
                        if similarity >= similarity_threshold:
                            results.append({
                                "id": record["id"],
                                "name": record["name"],
                                "personality": personality,
                                "similarity": similarity
                            })
                    except json.JSONDecodeError:
                        continue
                
                results.sort(key=lambda x: x["similarity"], reverse=True)
                return results[:10]
        except Exception as e:
            print(f"Failed to find personality matches: {e}")
            return []

    def _calculate_personality_similarity(self, p1: Dict[str, float], p2: Dict[str, float]) -> float:
        """计算性格相似度"""
        traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
        diff_sum = sum(abs(p1.get(t, 0.5) - p2.get(t, 0.5)) for t in traits)
        return max(0.0, 1.0 - (diff_sum / len(traits)))

    def delete_digital_twin(self, twin_id: str) -> bool:
        """删除数字分身"""
        if not self.connected:
            return False

        try:
            with self.driver.session(database=self.database) as session:
                query = """
                    MATCH (dt:DigitalTwin {id: $id})
                    OPTIONAL MATCH (dt)-[r]-()
                    DELETE r, dt
                """
                session.run(query, id=twin_id)
            return True
        except Exception as e:
            print(f"Failed to delete digital twin: {e}")
            return False