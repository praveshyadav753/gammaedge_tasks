from fastapi import FastAPI, HTTPException,de
from pydantic import BaseModel
import asyncio
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from sklearn.metrics.pairwise import cosine_similarity
from  middleware import cust_logging,timeout_middlewar
import uvicorn
from dotenv import load_dotenv
import logging

from google import genai
import os

load_dotenv()

api_key = os.getenv("GEN_AI")
client = genai.Client(api_key=api_key)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.middleware("http")(cust_logging)
app.middleware('http')(timeout_middlewar)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmbeddingRequest(BaseModel):
    text: str


class SimilarityInput(BaseModel):
    text: list[str]


class SimilarityRequest(BaseModel):
    text1: str
    text2: str


class SearchRequest(BaseModel):
    query: str
    documents: list[str]


class ScoreResult(BaseModel):
    score: float


class RankedResult(BaseModel):
    document: str
    score: float


class SearchResult(BaseModel):
    results: list[RankedResult]


async def get_model(texts: list[str], task_type="SEMANTIC_SIMILARITY"):
    if not api_key:
        raise HTTPException(status_code=500, detail="API Key missing")
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/embedding")
async def generate_embedding(request: EmbeddingRequest):
    vectors = await get_model(
        [request.text],
        task_type="RETRIEVAL_QUERY"
    )
    vector = vectors[0]
    return {
        "embeddings": vector.tolist(),
        "dimensions": len(vector)
    }


@app.post("/similarities")
async def calculate_cosine(request: SimilarityInput):
    vectors = await get_model(
        request.text,
        task_type="SEMANTIC_SIMILARITY"
    )
    matrix = cosine_similarity(vectors)
    return {"matrix": matrix.tolist()}


@app.post("/similarity", response_model=ScoreResult)
async def similarity_endpoint(request: SimilarityRequest):
    vectors = await get_model(
        [request.text1, request.text2],
        task_type="SEMANTIC_SIMILARITY"
    )
    score = float(
        cosine_similarity(
            vectors[0].reshape(1, -1),
            vectors[1].reshape(1, -1)
        )[0][0]
    )
    return {"score": score}


@app.post("/search", response_model=SearchResult)
async def search_documents(request: SearchRequest):
    if not request.documents:
        return {"results": []}

    query_vector = (
        await get_model(
            [request.query],
            task_type="RETRIEVAL_QUERY"
        )
    )[0]

    doc_vectors = await get_model(
        request.documents,
        task_type="RETRIEVAL_DOCUMENT"
    )

    results = []

    for doc, doc_vector in zip(request.documents, doc_vectors):
        score = float(
            cosine_similarity(
                query_vector.reshape(1, -1),
                doc_vector.reshape(1, -1)
            )[0][0]
        )
        results.append({
            "document": doc,
            "score": score
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return {"results": results}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
