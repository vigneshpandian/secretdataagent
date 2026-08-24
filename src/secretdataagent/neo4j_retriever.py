from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

class Neo4jRetriever:
    def __init__(self, uri: str = None, auth: tuple = None):
        # Ensure environment variables are loaded from .env
        load_dotenv(override=True)
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        print(f"Connecting to Neo4j at {self.uri}")
        self.auth = auth or (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
        self.driver = GraphDatabase.driver(self.uri, auth=self.auth)

    def close(self):
        self.driver.close()

    def get_table_schema_context(self, table_name: str = "SecretTransactions") -> str:
        """Retrieves columns, allowed values, synonyms, and business rules for the LLM context."""
        query = """
        MATCH (t:Table {name: $table_name})
        OPTIONAL MATCH (t)-[:HAS_COLUMN]->(c:Column)
        OPTIONAL MATCH (c)-[:HAS_ALLOWED_VALUE]->(v:Value)
        OPTIONAL MATCH (c)-[:HAS_SYNONYM]->(s:Synonym)
        OPTIONAL MATCH (t)-[:APPLIES_RULE]->(r:BusinessRule)
        RETURN t, 
               collect(distinct c) as columns, 
               collect(distinct v) as allowed_values, 
               collect(distinct s) as synonyms, 
               collect(distinct r) as rules
        """
        with self.driver.session() as session:
            result = session.run(query, table_name=table_name)
            record = result.single()
            if not record:
                return "No schema metadata found."
            
            schema_str = f"Table: {table_name}\nColumns:\n"
            for col in record["columns"]:
                schema_str += f" - {col['name']} ({col['dataType']}): {col.get('description', '')}\n"
            
            schema_str += "\nAllowed Values:\n"
            for val in record["allowed_values"]:
                schema_str += f" - {val.get('val')}: {val.get('meaning')}\n"

            schema_str += "\nBusiness Rules (MUST COMPLY):\n"
            for rule in record["rules"]:
                schema_str += f" - Rule [{rule.get('name')}]: {rule.get('description', '')} | Condition: {rule.get('sqlCondition', rule.get('sqlTemplate', ''))}\n"

            return schema_str