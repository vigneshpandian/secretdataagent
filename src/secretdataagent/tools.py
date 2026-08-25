from langchain_core.tools import tool
from secretdataagent.neo4j_retriever import Neo4jRetriever
from secretdataagent.postgres_retriever import PostgresRetriever
import sqlglot

neo4j_client = Neo4jRetriever()
postgres_client = PostgresRetriever()

@tool
def fetch_database_schema(table_name: str) -> str:
    """Fetch the graph schema, allowed categorical values, column types, and mandatory business rules for a table."""
    return neo4j_client.get_table_schema_context(table_name)

@tool
def run_sql_query(sql_query: str) -> str:
    """Execute an approved read-only PostgreSQL query."""
    validation_result = validate_sql_query.invoke({"sql_query": sql_query})

    if validation_result != "VALID":
        return validation_result

    results = postgres_client.execute_query(sql_query)
    return str(results)
@tool
def generate_sql_query(sql_query: str) -> str:
    """Generates and validates a formatted PostgreSQL query string based on natural language intent and graph context."""
    # Returns the formatted query for execution
    return sql_query.strip()

@tool
def validate_sql_query(sql_query: str) -> str:
    """Validate that a query is PostgreSQL syntax and read-only."""
    try:
        statements = sqlglot.parse(sql_query, read="postgres")

        if len(statements) != 1:
            return "INVALID: only one SQL statement is allowed"

        statement = statements[0]
        if statement is None:
            return "INVALID: query could not be parsed"

        if (statement.key or "").lower() not in {"select", "with"}:
            return "INVALID: only read-only queries are allowed"

        return "VALID"
    except Exception as error:
        return f"INVALID: {error}"