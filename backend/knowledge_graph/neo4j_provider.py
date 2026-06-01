from typing import List, Optional, Dict, Any
from neo4j import GraphDatabase, exceptions
from .entities import Entity, Relation, RELATION_TYPES
import json


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
            with self.driver.session() as session:
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

    def create_entity(self, entity: Entity) -> bool:
        """在 Neo4j 中创建实体"""
        if not self.connected:
            return False

        try:
            with self.driver.session() as session:
                query = """
                    CREATE (e:$label {
                        id: $id,
                        name: $name,
                        description: $description,
                        properties: $properties,
                        created_at: $created_at,
                        memory_id: $memory_id
                    })
                    RETURN e
                """
                session.run(query,
                           label=entity.entity_type,
                           id=entity.id,
                           name=entity.name,
                           description=entity.description,
                           properties=json.dumps(entity.properties),
                           created_at=entity.created_at.isoformat(),
                           memory_id=entity.memory_id or "")
            return True
        except exceptions.Neo4jException as e:
            print(f"Failed to create entity: {e}")
            return False

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """从 Neo4j 获取实体"""
        if not self.connected:
            return None

        try:
            with self.driver.session() as session:
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
        except exceptions.Neo4jException as e:
            print(f"Failed to get entity: {e}")
            return None

    def find_entity_by_name(self, name: str) -> Optional[Entity]:
        """按名称查找实体"""
        if not self.connected:
            return None

        try:
            with self.driver.session() as session:
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
        except exceptions.Neo4jException as e:
            print(f"Failed to find entity: {e}")
            return None

    def create_relation(self, relation: Relation) -> bool:
        """创建关系"""
        if not self.connected:
            return False

        try:
            with self.driver.session() as session:
                query = """
                    MATCH (a), (b)
                    WHERE a.id = $from_id AND b.id = $to_id
                    CREATE (a)-[r:$relation_type {
                        id: $id,
                        weight: $weight,
                        properties: $properties,
                        created_at: $created_at
                    }]->(b)
                    RETURN r
                """
                session.run(query,
                           from_id=relation.from_entity_id,
                           to_id=relation.to_entity_id,
                           relation_type=relation.relation_type,
                           id=relation.id,
                           weight=relation.weight,
                           properties=json.dumps(relation.properties),
                           created_at=relation.created_at.isoformat())
            return True
        except exceptions.Neo4jException as e:
            print(f"Failed to create relation: {e}")
            return False

    def get_relations(self, entity_id: str, relation_type: Optional[str] = None) -> List[Relation]:
        """获取实体的关系"""
        if not self.connected:
            return []

        try:
            with self.driver.session() as session:
                if relation_type:
                    query = """
                        MATCH (a)-[r:$relation_type]-(b)
                        WHERE a.id = $id OR b.id = $id
                        RETURN r, a.id as from_id, b.id as to_id
                    """
                    result = session.run(query, id=entity_id, relation_type=relation_type)
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
        except exceptions.Neo4jException as e:
            print(f"Failed to get relations: {e}")
            return []

    def find_path(self, from_id: str, to_id: str, max_depth: int = 5) -> List[List[Dict]]:
        """查找两个实体之间的路径"""
        if not self.connected:
            return []

        try:
            with self.driver.session() as session:
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
        except exceptions.Neo4jException as e:
            print(f"Failed to find path: {e}")
            return []

    def execute_cypher(self, query: str) -> List[Dict[str, Any]]:
        """执行 Cypher 查询"""
        if not self.connected:
            return []

        try:
            with self.driver.session() as session:
                result = session.run(query)
                return [dict(record) for record in result]
        except exceptions.Neo4jException as e:
            print(f"Cypher query failed: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self.connected:
            return {"error": "Not connected"}

        try:
            with self.driver.session() as session:
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
        except exceptions.Neo4jException as e:
            print(f"Failed to get stats: {e}")
            return {"error": str(e)}

    def batch_import(self, entities: List[Entity], relations: List[Relation]) -> Dict[str, int]:
        """批量导入实体和关系"""
        if not self.connected:
            return {"entities_created": 0, "relations_created": 0}

        entities_created = 0
        relations_created = 0

        try:
            with self.driver.session() as session:
                for entity in entities:
                    try:
                        query = """
                            CREATE (e:$label {
                                id: $id,
                                name: $name,
                                description: $description,
                                properties: $properties,
                                created_at: $created_at,
                                memory_id: $memory_id
                            })
                        """
                        session.run(query,
                                   label=entity.entity_type,
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
                        query = """
                            MATCH (a), (b)
                            WHERE a.id = $from_id AND b.id = $to_id
                            MERGE (a)-[r:$relation_type {id: $id}]->(b)
                            ON CREATE SET r.weight = $weight, r.properties = $properties, r.created_at = $created_at
                        """
                        session.run(query,
                                   from_id=relation.from_entity_id,
                                   to_id=relation.to_entity_id,
                                   relation_type=relation.relation_type,
                                   id=relation.id,
                                   weight=relation.weight,
                                   properties=json.dumps(relation.properties),
                                   created_at=relation.created_at.isoformat())
                        relations_created += 1
                    except:
                        pass

            return {"entities_created": entities_created, "relations_created": relations_created}
        except exceptions.Neo4jException as e:
            print(f"Batch import failed: {e}")
            return {"entities_created": entities_created, "relations_created": relations_created}