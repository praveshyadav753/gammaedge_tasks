import os
from google import genai
from dotenv import load_dotenv
import numpy as np

load_dotenv()
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
        return [np.array(e.values) for e in response.embeddings]

    # run the async function synchronously
    return asyncio.run(async_embed(texts))


# Example usage:

# text = "This is a test sentence."
# vector = get_embeddings([text])[0]  # get first (and only) vector
# print(vector.shape)
