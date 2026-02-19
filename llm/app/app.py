from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from middleware import cust_logging,timeout_middlewar
import asyncio
import vecdb
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn
from dotenv import load_dotenv
import logging
from db_op.chroma_router import Chroma_router
from google import genai
import os



load_dotenv()

api_key = os.getenv("GEN_AI")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("semantic-api")

if not api_key:
    logger.warning("GEN_AI API key not found in environment variables.")

client = genai.Client(api_key=api_key)



app = FastAPI(title="Semantic Similarity API")

# Middleware

app.middleware("http")(cust_logging)
app.middleware("http")(timeout_middlewar)

# async def timeout_middleware(request: Request, call_next):
    # try:
    #     response = await asyncio.wait_for(
    #         call_next(request),
    #         timeout=30
    #     )
    #     return response
    # except asyncio.TimeoutError:
    #     logger.warning(f"Request timeout: {request.url}")
    #     return JSONResponse(
    #         status_code=504,
    #         content={"detail": "Request timeout"},
    #     )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vecdb.router)
app.include_router(Chroma_router)

# Pydantic Models


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



async def get_embeddings(texts: list[str], task_type="SEMANTIC_SIMILARITY"):
    if not api_key:
        raise HTTPException(status_code=500, detail="API key missing")

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

    except Exception:
        logger.exception("Embedding generation failed")
        raise HTTPException(
            status_code=500,
            detail="Embedding generation failed"
        )


@app.get("/health")
async def health():
    return {"status": "running"}


@app.post("/embedding")
async def generate_embedding(request: EmbeddingRequest):
    vectors = await get_embeddings(
        [request.text],
        task_type="RETRIEVAL_QUERY"
    )
    vector = vectors[0]

    return {
        "embedding": vector.tolist(),
        "dimensions": len(vector)
    }


@app.post("/similarities")
async def calculate_similarity_matrix(request: SimilarityInput):
    vectors = await get_embeddings(
        request.text,
        task_type="SEMANTIC_SIMILARITY"
    )

    matrix = cosine_similarity(vectors)

    return {"matrix": matrix.tolist()}


@app.post("/similarity", response_model=ScoreResult)
async def similarity_endpoint(request: SimilarityRequest):
    vectors = await get_embeddings(
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
        await get_embeddings(
            [request.query],
            task_type="RETRIEVAL_QUERY"
        )
    )[0]

    doc_vectors = await get_embeddings(
        request.documents,
        task_type="RETRIEVAL_DOCUMENT"
    )

    scores = cosine_similarity(
        query_vector.reshape(1, -1),
        np.array(doc_vectors)
    )[0]

    results = [
        RankedResult(document=doc, score=float(score))
        for doc, score in zip(request.documents, scores)
    ]

    results.sort(key=lambda x: x.score, reverse=True)

    return {"results": results}



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001)
