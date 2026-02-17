from google import genai
from dotenv import load_dotenv
from fastapi import HTTPException
import asyncio
import os
from google.genai import types



load_dotenv()

api_key = os.getenv("GEN_AI")

client = genai.Client(api_key=api_key)


async def get_response(query: query):
    if not api_key:
        raise HTTPException(status_code=500, detail="API Key missing")
    try:
        response = client.models.generate_content_stream(
            model="gemini-3-flash-preview",
            contents=query,
            stream=True,
            config=types.GenerateContentConfig(temperature=0.1),
        )
        for chunk in response:
           yield chunk.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
