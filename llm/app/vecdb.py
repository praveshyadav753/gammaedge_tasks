from fastapi import APIRouter
from fastapi import Query
from utility.faisss import FaissStore



documents = ""
vector_store = FaissStore()
vector_store.add_documents(documents)


router = APIRouter(
    prefix="/vecdb",
    tags=["vectordb"]
)

@router.get("/search")
def search(
    query: str = Query(..., description="Search query"),
    top_k: int = Query(5, ge=1, le=20)
):
    results = vector_store.search(query, top_k)

    return {
        "query": query,
        "results": results
    }
