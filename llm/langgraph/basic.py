from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from typing_extensions import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEN_AI")

if not api_key:
    raise ValueError("GEN_AI API key not found in environment variables")
os.environ["GOOGLE_API_KEY"] = api_key
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_ENDPOINT"]= os.getenv("LANGSMITH_ENDPOINT")

class MessagesState(TypedDict):
    messages: Annotated[list, add_messages]

@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

@tool
def add(a: int, b: int) -> int: 
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    
    return a + b

@tool
def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    if b == 0:
        return "Error: Cannot divide by zero"
    return a / b

tools = [add, multiply, divide]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
llm_with_tools = llm.bind_tools(tools)

sys_msg = SystemMessage(content="You are a helpful assistant that performs arithmetic step by step.")

def assistant(state: MessagesState):
    response = llm_with_tools.invoke([sys_msg] + state["messages"])
    return {"messages": [response]}

builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

react_graph = builder.compile()

result = react_graph.invoke(
    {"messages": [HumanMessage(content="What is (3 * 4) + 5 divided by 2?")]}
)

print("\nFinal Answer:\n")
print(result["messages"][-1].content)