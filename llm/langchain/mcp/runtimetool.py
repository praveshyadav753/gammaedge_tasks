import os
from pprint import pprint
from dotenv import load_dotenv
from langchain.agents import create_agent
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
from langchain.messages import HumanMessage


load_dotenv()


@dataclass
class ColourContext:
    favourite_colour: str = "blue"
    least_favourite_colour: str = "yellow"




# agent = create_agent(
#     model="gpt-5-nano",
#     context_schema=ColourContext
# )    

# response = agent.invoke(
#     {"messages": [HumanMessage(content="What is my favourite colour?")]},
#     context=ColourContext()
# )


# pprint(response)


@tool
def get_favourite_colour(runtime: ToolRuntime) -> str:
    """Get the favourite colour of the user"""
    return runtime.context.favourite_colour

@tool
def get_least_favourite_colour(runtime: ToolRuntime) -> str:
    """Get the least favourite colour of the user"""
    return runtime.context.least_favourite_colour

agent = create_agent(
    model="gpt-5-nano",
    tools=[get_favourite_colour, get_least_favourite_colour],
    context_schema=ColourContext
)

response = agent.invoke(
    {"messages": [HumanMessage(content="What is my favourite colour?")]},
    context=ColourContext()
)

pprint(response)