import os
from google import genai
from dotenv import load_dotenv
import numpy as np
from  sentence_transformers import SentenceTransformer
load_dotenv()
import asyncio
api_key = os.getenv("GEN_AI")
client = genai.Client(api_key=api_key)


def get_embeddings(texts: list[str], task_type="SEMANTIC_SIMILARITY"):
    """
    Synchronous embedding generation wrapper.
    """
    import asyncio

    # run async code in sync
    async def async_embed(texts):
        response = await asyncio.to_thread(
            client.models.embed_content,
            model="gemini-embedding-001",
            contents=texts,
            config={
                "task_type": task_type,
                "output_dimensionality": 768
            }
        )
        
        embedding = [e.values for e in response.embeddings]
        return  embedding


    # run the async function synchronously
    return asyncio.run(async_embed(texts))

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

async def embed_text(text: str):
    # embeddings = model.encode(text)
    response =await asyncio.to_thread(model.encode, text)
    return response.tolist()