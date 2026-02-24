# combined_server.py
import asyncio
from fastmcp import FastMCP
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent, AgentState
from langchain.messages import HumanMessage, ToolMessage
from langchain.tools import tool
from langgraph.types import Command
from langchain_community.utilities import SQLDatabase

mcp = FastMCP("combined_mcp_server")


multi_client = MultiServerMCPClient({
    "kiwi_flights": {
        "transport": "stdio",
        "command": "python",
        "args": ["kiwi_mcp_server.py"],  # your Kiwi MCP server file
    }
})


class WeddingState(AgentState):
    origin: str
    destination: str
    guest_count: str
    genre: str


async def get_kiwi_tools():
    """Fetch tools exposed by Kiwi MCP server"""
    return await multi_client.get_tools()

@tool
async def search_flights(runtime):
    """Delegate flight search to Kiwi MCP server"""
    origin = runtime.state["origin"]
    destination = runtime.state["destination"]

    kiwi_tools = await get_kiwi_tools()
    flight_tool = next(t for t in kiwi_tools if t.name == "search_flights")
    return await flight_tool.invoke({
        "origin": origin,
        "destination": destination
    })

# Local venue search
from tavily import TavilyClient
tavily_client = TavilyClient()

@mcp.tool()
def search_venues(runtime):
    location = runtime.state["destination"]
    guests = runtime.state["guest_count"]
    return tavily_client.search(f"Wedding venues in {location} for {guests} guests")

# Local playlist tool
db = SQLDatabase.from_uri("sqlite:///resources/Chinook.db")

@mcp.tool()
def generate_playlist(runtime):
    genre = runtime.state["genre"]
    try:
        return db.run(f"SELECT Name, Composer FROM tracks WHERE GenreId=(SELECT GenreId FROM genres WHERE Name='{genre}') LIMIT 20;")
    except Exception as e:
        return {"error": str(e)}

# Tool to update state
@tool
def update_state(origin, destination, guest_count, genre, runtime):
    return Command(update={
        "origin": origin,
        "destination": destination,
        "guest_count": guest_count,
        "genre": genre,
        "messages": [ToolMessage("State updated", tool_call_id=runtime.tool_call_id)]
    })


coordinator = create_agent(
    model="gpt-4o-mini",
    tools=[search_flights, search_venues, generate_playlist, update_state],
    state_schema=WeddingState,
    system_prompt="""
    You are a wedding coordinator.
    First update state from user input (origin, destination, guest_count, genre).
    Then delegate flights to Kiwi MCP, venues to Tavily, and playlist to Chinook DB.
    Finally combine the results into one wedding plan.
    """
)

if __name__ == "__main__":
    mcp.run(transport="stdio")