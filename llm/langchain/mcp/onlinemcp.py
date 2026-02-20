from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.messages import HumanMessage

load_dotenv()

client = MultiServerMCPClient(
    {
       
   
  
    "travel_server": {
                "transport": "streamable_http",
                "url": "https://mcp.kiwi.com"
            }
  

  }
    
)


import asyncio

async def main():
    tools = await client.get_tools()
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
        {"messages": [HumanMessage(content="where i am")]},
        config=config
    )

    from pprint import pprint
    pprint(response["messages"][-1].content)

# Run async main
asyncio.run(main())

