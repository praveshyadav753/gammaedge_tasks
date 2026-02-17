import operator
from typing import Annotated
from pprint import pprint
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
import json
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
# from dotenv import load_dotenv
import os
import json
from langchain.messages import AnyMessage
from langchain.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

api_key_groq = os.getenv("GROQ1")
# api_key_groq = 

# Step 1: Define tools and model
model = init_chat_model(
    model_provider="groq",
    model="llama-3.1-8b-instant",
    api_key = api_key_groq,
    temperature=0.3,
)

class State(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

def chatbot(state: State):
    # print(state)
    msg = {"messages": [model.invoke(state["messages"])]}
    return msg



# from here we are building a graph
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)  # first arg is name and second is the func that need to call when it run
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")
graph = graph_builder.compile()

# Run the chatbot
# while True:
#     user_input = input("User: ")
#     if user_input.lower() in ["quit", "exit", "q"]:
#         print("Goodbye!")
#         break
#     for event in graph.stream({"messages": [("user", user_input)]}):
#         for value in event.values():
#             print("Assistant:", value["messages"][-1].content)
#             # print(State)

history =[]
count=0
# while True:
user_input = "hey buddy!"
# if user_input.lower() in ["quit", "exit", "q"]:
#     print("Goodbye!")
#     break
for event in graph.stream({"messages": [("user", user_input)]}):
    # json.loads(event)
    # print(type(event))
    message = event['chatbot']['messages'][0].content

    count +=1





