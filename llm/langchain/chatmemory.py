from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pprint import pprint
# from langchain_openai import ChatOpenAI
import os

load_dotenv()

api_key = os.getenv("GROQ")
if not api_key:
    raise ValueError("GROQ API key not found in environment variables")
os.environ["GROQ_API_KEY"] = api_key

# question = HumanMessage(content="Hello my name is Seán and my favourite colour is green")

# question = HumanMessage(content="What's my favourite colour?")

# response = agent.invoke(
#     {"messages": [question]}
# )

# pprint(response)

from langgraph.checkpoint.memory import InMemorySaver
from langchain_groq import ChatGroq


model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
)

agent = create_agent(
    model = model,
    checkpointer=InMemorySaver(),
)

question = HumanMessage(
    content="Hello my name is pravesh and my favourite colour is green"
)
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [question]},
    config,
)
pprint(response)
question = HumanMessage(content="What's my favourite colour?")

response = agent.invoke(
    {"messages": [question]},
    config,
)

pprint(response["messages"])
