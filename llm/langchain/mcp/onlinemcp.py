import asyncio
from pprint import pprint
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI API key not found in environment variables")
os.environ["OPENAI_API_KEY"] = api_key

client = MultiServerMCPClient(
    {
        "travel_server": {
            "transport": "streamable_http",
            "url": "https://mcp.kiwi.com"
        }
    }
)


async def main():
    tools = await client.get_tools()
    # print(tools)
    # resources = await client.get_resources("local_server")
    # prompt = await client.get_prompt("time", "prompt")
    # prompt = prompt[0].content

    agent = create_agent(
        model="gpt-5-nano",
        tools=tools,
        # system_prompt=prompt
    )

    config = {"configurable": {"thread_id": "1"}}

    response = await agent.ainvoke(
        {"messages": [HumanMessage(content="give me flights available for indore to delhi for march 13 2026")]},
        config=config
    )

    pprint(response["messages"][-1].content)

# Run async main
asyncio.run(main())

