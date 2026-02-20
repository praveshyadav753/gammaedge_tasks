from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

# from langchain.chat_models import OpenAIChat
from langchain_core.messages import HumanMessage
import base64
import os
from pprint import pprint

load_dotenv()

# Path to your image
image_path = "llm/langchain/scenaryimg.jpg"

# Load API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI API key not found in environment variables")
os.environ["OPENAI_API_KEY"] = api_key

try:
    # Read image and encode in Base64
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    # Multimodal human message
    multimodal_question = HumanMessage(
        content=[
            {"type": "text", "text": "Tell me about this"},
            {"type": "image", "base64": img_b64, "mime_type": "image/png"},
        ]
    )

    # Initialize GPT-5 Nano
    model = init_chat_model(model="gpt-5-nano", temperature=0.5, streaming=False)

    # Create agent with system prompt
    agent = create_agent(
        model=model,
        system_prompt="You are an image analyzer. Analyze the Base64 image and describe the scene in detail.",
    )

    response = agent.invoke({"messages": [multimodal_question]})

    pprint(response["messages"][-1].content)
except Exception as e:
    print("Error:", e)
