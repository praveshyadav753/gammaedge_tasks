import os
from dotenv import load_dotenv
# import ChatOpenAI

# from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime

# 1. Setup API Key (ensure this is valid!)
load_dotenv()
api_key = os.getenv("GROQ")
os.environ["GROQ_API_KEY"] = api_key

SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""



@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str

@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    # A punny response (always required)
    punny_response: str
    # Any interesting information about the weather if available
    weather_conditions: str | None = None


@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"
# 2. Initialize Model - Added print to confirm progress
print("Initializing model...")

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.5,
    
)

# 3. Create Agent - Added print to confirm progress
print("Creating agent...")
agent = create_agent(
    model=model,
    tools=[get_user_location,get_weather_for_location],
    system_prompt=SYSTEM_PROMPT,

)

print("Invoking agent (waiting for Groq response)...")
config = {"configurable": {"thread_id": "1"}}
response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather outside in indore?"}]},
    config=config,
    context=Context(user_id="1")
)
    # create_agent returns a state; access the last message content
print("Response received:")
print(response["messages"][-1].content)
# except Exception as e:
#     print(f"An error occurred during invocation: {e}")
# model = ChatOpenAI(
#     model="gpt-5",
#     temperature=0.1,
#     max_tokens=1000,
#     timeout=30
#     # ... (other params)
# )