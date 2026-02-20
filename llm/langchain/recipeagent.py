from dotenv import load_dotenv
from langchain.tools import tool
from typing import Dict, Any
from tavily import TavilyClient
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from pprint import pprint


load_dotenv()

tavily_client = TavilyClient()


system_prompt = """

You are a personal chef. The user will give you a list of ingredients they have left over in their house.

Using the web search tool, search the web for recipes that can be made with the ingredients they have.

Return recipe suggestions and eventually the recipe instructions to the user, if requested.

"""

@tool
def web_search(query: str) -> Dict[str, Any]:

    """Search the web for information"""

    return tavily_client.search(query)


agent = create_agent(
    model="gpt-5-nano",
    tools=[web_search],
    system_prompt=system_prompt,
    checkpointer=InMemorySaver()
)


config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [HumanMessage(content="I have some leftover pattao and curd what dish can i make ?")]},
    config
)

print(response['messages'][-1].content)



# pprint(response)