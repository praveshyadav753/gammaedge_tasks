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
        "local_server": {
                "transport": "stdio",
                "command": "python3",
                "args": ["mcp_server.py"],
            }
}
)

async def main():
    tools = await client.get_tools()
    # resources = await client.get_resources("local_server")
    prompt = await client.get_prompt("local_server", "prompt")
    prompt = prompt[0].content

    agent = create_agent(
        model="gpt-5-nano",
        tools=tools,
        system_prompt=prompt
    )

    config = {"configurable": {"thread_id": "1"}}

    response = await agent.ainvoke(
        {"messages": [HumanMessage(content="what does lanchain do")]},
        config=config
    )

    pprint(response["messages"][-1].content)

# Run async main
asyncio.run(main())