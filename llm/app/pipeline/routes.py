from fastapi import APIRouter
from pydantic import BaseModel,Field
from typing import Optional
from pipeline.pipeline import search_pipeline



pipeline_router = APIRouter(prefix="/pipeline",tags=["pipeline_query"])

class Querydata(BaseModel):
    query: str
    threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    top_n: int = Field(default=20, ge=1)
    top_k: int = Field(default=5, ge=1)

@pipeline_router.post('/get')
async def run_pipeline(query: Querydata):
   result = await search_pipeline(query.query,query.threshold,query.top_n,query.top_k)
   return result



