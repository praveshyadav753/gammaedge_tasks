import os
from typing import Any
from langgraph.runtime import Runtime
from dotenv import load_dotenv
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import SummarizationMiddleware, before_agent
from langchain.messages import HumanMessage, AIMessage, RemoveMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

api_key = os.getenv("GEN_AI")
if not api_key:
    raise ValueError("OPENAI API key not found in environment variables")
os.environ["GOOGLE_API_KEY"] = api_key


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key
)

# agent = create_agent(
#     model=llm,
#     checkpointer=InMemorySaver(),
#     middleware=[
#         SummarizationMiddleware(
#             model=llm,
#             trigger=("tokens", 100),
#             keep=("messages", 1)
#         )
#     ],
# )

# response = agent.invoke(
#     {"messages": [
#         HumanMessage(content="What is the capital of the moon?"),
#         AIMessage(content="The capital of the moon is Lunapolis."),
#         HumanMessage(content="What is the weather in Lunapolis?"),
#         AIMessage(content="Skies are clear, with a high of 120C and a low of -100C."),
#         HumanMessage(content="How many cheese miners live in Lunapolis?"),
#         AIMessage(content="There are 100,000 cheese miners living in Lunapolis."),
#         HumanMessage(content="Do you think the cheese miners' union will strike?"),
#         AIMessage(content="Yes, because they are unhappy with the new president."),
#         HumanMessage(content="If you were Lunapolis' new president how would you respond to the cheese miners' union?"),
#         ]},
#     {"configurable": {"thread_id": "1"}}
# )

# print("response",response)

# print(response["messages"][0].content)

# --------------------------------------------------------------------------------------------------------------

@before_agent
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Remove all the tool messages from the state"""
    messages = state["messages"]

    tool_messages = [m for m in messages if isinstance(m, ToolMessage)]
    
    return {"messages": [RemoveMessage(id=m.id) for m in tool_messages]}



agent = create_agent(
    model=llm,
    checkpointer=InMemorySaver(),
    middleware=[trim_messages],
)

response = agent.invoke(
    {"messages": [
        HumanMessage(content="My device won't turn on. What should I do?"),
        ToolMessage(content="blorp-x7 initiating diagnostic ping…", tool_call_id="1"),
        AIMessage(content="Is the device plugged in and turned on?"),
        HumanMessage(content="Yes, it's plugged in and turned on."),
        ToolMessage(content="temp=42C voltage=2.9v … greeble complete.", tool_call_id="2"),
        AIMessage(content="Is the device showing any lights or indicators?"),
        HumanMessage(content="What's the temperature of the device?")
        ]},
    {"configurable": {"thread_id": "2"}}
)

print(response["messages"][-1].content)