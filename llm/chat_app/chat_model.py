from google import genai
from dotenv import load_dotenv
import asyncio
import os
from google.genai import types



load_dotenv()

api_key = os.getenv("GEN_AI")

client = genai.Client(api_key=api_key)


async def get_response(query):
    if not api_key:
        raise Exception("API Key missing")
    try:
        response = await client.aio.models.generate_content_stream(
            model="gemini-3-flash-preview",
            contents=query,
            config=types.GenerateContentConfig(temperature=0.1),
        )
        async for chunk in response:
           yield chunk.text
    except Exception as e:
        raise Exception(str(e))
