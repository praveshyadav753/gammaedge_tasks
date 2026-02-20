from langchain.tools import tool
from typing import Dict, Any
from tavily import TavilyClient
from dotenv import load_dotenv
from langchain.agents import create_agent
import os
from langchain_groq import ChatGroq
import pprint

# Load environment variables
load_dotenv()

# Set GROQ API Key
api_key = os.getenv("GROQ")
if not api_key:
    raise ValueError("GROQ API key not found in environment variables")
os.environ["GROQ_API_KEY"] = api_key

# Tavily client
tavily_client = TavilyClient()

# Tool definition
@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)

# LLM
model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.5,
)

# Create agent (system_prompt must be a STRING)
agent = create_agent(
    model=model,
    tools=[web_search],
    system_prompt="You are an assistant. Answer the question. If you don't know the answer, use the web_search tool."
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "Who is the current mayor of San Francisco?"}]}
)

pprint.pprint(response["messages"])