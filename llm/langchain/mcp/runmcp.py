from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {
        "local_server": {
                "transport": "stdio",
                "command": "python3",
                "args": ["llm/langchain/mcp/mcp_server.py"],
            }
    }
)

import asyncio

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

    from langchain.messages import HumanMessage
    config = {"configurable": {"thread_id": "1"}}

    response = await agent.ainvoke(
        {"messages": [HumanMessage(content="what does lanchain do")]},
        config=config
    )

    from pprint import pprint
    pprint(response["messages"][-1].content)

# Run async main
asyncio.run(main())