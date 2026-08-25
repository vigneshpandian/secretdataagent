import os
from typing import Annotated, TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from secretdataagent.tools import fetch_database_schema, run_sql_query, generate_sql_query, validate_sql_query
from secretdataagent.neo4j_retriever import Neo4jRetriever
from dotenv import load_dotenv

load_dotenv(override=True)

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

class LangGraphWorkflow:
    def __init__(self):
        tools = [validate_sql_query]
        load_dotenv(override=True)
        # Read provider settings from env (Defaults to google_genai / gemini-2.5-flash)
        model_name = os.getenv("LLM_MODEL", "gemini-2.5-flash")
        model_provider = os.getenv("LLM_PROVIDER", "google_genai")
        print(os.getenv("NEO4J_URI", "bolt://localhost:7687"))
        # Agnostic model instantiation
        base_llm = init_chat_model(
            model=model_name,
            model_provider=model_provider,
            temperature=0
        )
        self.llm = base_llm.bind_tools(tools)
        self.graph = self._build_graph(tools)
        self.neo4j_retriever = Neo4jRetriever()

    def _build_graph(self, tools):
        workflow = StateGraph(AgentState)

        def chatbot_node(state: AgentState):
            return {"messages": [self.llm.invoke(state["messages"])]}

        workflow.add_node("agent", chatbot_node)
        workflow.add_node("tools", ToolNode(tools))

        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", tools_condition)
        workflow.add_edge("tools", "agent")

        return workflow.compile()

    def run(self, user_query: str):
        # Print the ASCII graph representation to the terminal
        self.graph.get_graph().print_ascii()
        # 3. Dynamic Schema Injection: Fetch schema from Neo4j in advance
        
        schema_context = self.neo4j_retriever.get_table_schema_context(table_name="SecretTransactions")
        print(f"Schema Context Retrieved:\n{schema_context}\n")
        # General, table-agnostic system prompt
        system_instruction = (
            "You are an expert SQL Assistant.\n"
            "Below is the database schema, categorical allowed values, and mandatory business rules:\n\n"
            f"=== DATABASE METADATA & RULES ===\n{schema_context}\n=================================\n\n"
            "EXECUTION RULES:\n"
            "Generate the executable PostgreSQL SQL statement directly.\n"
            "Return only SQL. Do not include Markdown fences, labels, explanations, or other text.\n"
          
        )

        initial_state = {
            "messages": [
                ("system", system_instruction),
                ("user", user_query)
            ]
        }
        
        output = self.graph.invoke(initial_state)
        last_message = output["messages"][-1]
        
        # Safely parse string response from Gemini / LangChain content blocks
        content = last_message.content
        if isinstance(content, list):
            # Aggregate text blocks if Gemini returns a list of dictionaries/objects
            text_parts = []
            for part in content:
                if isinstance(part, dict) and "text" in part:
                    text_parts.append(part["text"])
                elif hasattr(part, "text"):
                    text_parts.append(part.text)
                elif isinstance(part, str):
                    text_parts.append(part)
            return "\n".join(text_parts)
            
        return str(content)