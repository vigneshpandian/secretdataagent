# SecretDataAgent

A small FastAPI + LangGraph service for turning natural-language questions into SQL against a PostgreSQL database, using Neo4j metadata as business-context and schema guidance.

## What this project does

- Accepts a natural-language question through an HTTP endpoint
- Uses a LangGraph agent to generate PostgreSQL directly from the user request
- Pulls table metadata and business rules from Neo4j
- Validates generated SQL as a single, read-only PostgreSQL statement
- Returns the generated SQL query as part of the API response

## Requirements

- Python 3.14+
- Neo4j instance
- PostgreSQL instance
- A model provider configured via environment variables (for example Gemini or another LangChain-supported provider)

## Setup

1. Create and activate a virtual environment (or use uv):

   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root with values similar to:

   ```env
   LLM_PROVIDER=google_genai
   LLM_MODEL=gemini-2.5-flash

   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password

   POSTGRES_URL=postgresql://user:password@localhost:5432/finance_db
   ```

3. Make sure your Neo4j database contains the metadata graph for the target table, and that PostgreSQL is reachable using `POSTGRES_URL`.

## Run the API

Start the app with either of the following:

```bash
uv run secretdataagent
```

or

```bash
uv run uvicorn secretdataagent:app --reload --host 127.0.0.1 --port 8000
```

The app will run at:

- http://127.0.0.1:8000

## API usage

### Endpoint

- POST /query

### Example request

```bash
curl -X POST "http://127.0.0.1:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show me the total amount by payment status for this month"
  }'
```

### Example response

```json
{
  "query": "Show me the total amount by payment status for this month",
  "result": "SELECT payment_status, SUM(amount) AS total_amount\nFROM \"SecretTransactions\"\nWHERE created_at >= DATE_TRUNC('month', CURRENT_DATE)\nGROUP BY payment_status;"
}
```

The model is instructed to return only executable SQL, without Markdown fences, labels, or explanations.

## Tools

The current workflow binds `validate_sql_query` to the model. It uses `sqlglot` to check PostgreSQL syntax and rejects malformed SQL, multiple statements, and write operations such as `INSERT`, `UPDATE`, `DELETE`, and `DROP`.

`run_sql_query` also validates a query before executing it against PostgreSQL, but it is not currently bound into the LangGraph workflow. Add it to the workflow tool list only when the application should execute generated queries rather than return SQL.

## Run tests

Run the tool tests with:

```bash
uv run python -m unittest discover -s tests -v
```

## Demo database seed script

This project includes a sample PostgreSQL seed script at [postgres_script.sql](postgres_script.sql). It creates a table named `public.secrettransactions` and inserts a small set of fake transaction records.

Use it as a quick local demo dataset when you want to test the API without wiring up a full production database.

### How to load the sample script

```bash
psql -h localhost -U postgres -d finance_db -f postgres_script.sql
```

If your database uses a different username or database name, replace the values in the command above.

> This script is only a sample dataset. It is meant to help you prototype and validate the workflow. It is not a fixed requirement for the application, and it should not be treated as the only valid schema or table design.

## Notes on the schema/table examples

> The table metadata, graph schema, and example values in this repository are for demonstration and local testing. They are examples to show how the agent expects data to be structured, but they are not a universal or absolute rulebook for every database.

In other words, the included table and schema are a sample scaffold, not a bible. Adapt the metadata, columns, allowed values, and business rules to match your real database model and your actual domain rules.

## Project structure

```text
src/
  secretdataagent/
    __init__.py
    neo4j_retriever.py
    postgres_retriever.py
    tools.py
    workflow_graph.py
    graph_schema.txt
tests/
  test_tools.py
```

## Troubleshooting

- If the app cannot connect to Neo4j or Postgres, confirm the environment variables in `.env` are correct.
- If the model does not return SQL as expected, verify that the model provider and model name are supported by LangChain.
- If the agent cannot find schema metadata, check that the Neo4j graph contains the expected `Table`, `Column`, and `BusinessRule` nodes.

## License

This project is intended for learning and experimentation. Adjust as needed for your environment and deployment requirements.
