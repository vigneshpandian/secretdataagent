from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from secretdataagent.workflow_graph import LangGraphWorkflow
import uvicorn

load_dotenv(override=True)  # Load environment variables from .env file

# Add a function wrapper for the script entry
def main():
    uvicorn.run("secretdataagent:app", host="127.0.0.1", port=8000, reload=True)

app = FastAPI(
    title="Graph RAG Text-to-SQL API",
    description="Provider-Agnostic Text-to-SQL Service using LangGraph and Neo4j Context.",
    version="1.0.0"
)

agent_workflow = LangGraphWorkflow()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    result: str

@app.post("/query", response_model=QueryResponse, summary="Execute Natural Language Query")
async def execute_query(payload: QueryRequest):
    try:
        answer = agent_workflow.run(payload.query)
        return QueryResponse(query=payload.query, result=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))