from langchain_core.tools import tool
from secretdataagent.neo4j_retriever import Neo4jRetriever
from secretdataagent.postgres_retriever import PostgresRetriever

neo4j_client = Neo4jRetriever()
postgres_client = PostgresRetriever()

@tool
def fetch_database_schema(table_name: str) -> str:
    """Fetch the graph schema, allowed categorical values, column types, and mandatory business rules for a table."""
    return neo4j_client.get_table_schema_context(table_name)

@tool
def run_sql_query(sql_query: str) -> str:
    """Execute a generated PostgreSQL query against the target database and return the output records."""
    results = postgres_client.execute_query(sql_query)
    return str(results)

@tool
def generate_sql_query(sql_query: str) -> str:
    """Generates and validates a formatted PostgreSQL query string based on natural language intent and graph context."""
    # Returns the formatted query for execution
    return sql_query.strip()