from fastapi import APIRouter, HTTPException
from .connect import collection
from utility.getemb import get_embeddings as embed_text
from pydantic import BaseModel
from .pdf_reader import load_pdf,chunk_text

Chroma_router = APIRouter(prefix="/chroma_db", tags=["chromadb"])


class DocumentInput(BaseModel):
    id: str
    content: str
    metadata: dict = None


class SearchInput(BaseModel):
    query: str
    n_results: int = 2


@Chroma_router.post("/add_document")
def add_document(doc: DocumentInput):
    try:
        text = load_pdf("llm.pdf")
        print("adding ....")
        collection.add(
            documents=[text], ids=["document_1"], metadatas=[{"source": "document.pdf"}]
        )
        return {"message": f"Document {doc.id} added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@Chroma_router.get("/add_document_chunk")   
def add_document_chunks(): 
    try:
        pdf_text = load_pdf("llm.pdf")  
        chunks = chunk_text(pdf_text, chunk_size=500, overlap=50)
        print("adding ....")

        for i,chunk in enumerate(chunks):

            collection.add(
        ids=[str(i)],  
        documents=[chunk],
        metadatas=[{"source": 'document.pdf', "chunk": i}]
         )
        print(i,"added")   
        return {"message": f"Document  added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@Chroma_router.post("/search")
# def search_documents(search_input: SearchInput):
#     try:
#         results = collection.query(
#             query_texts=[search_input.query],
#             n_results=search_input.n_results
#         )
#         return {"results": results}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
def search(query: SearchInput):
    # query_embedding = embed_text(query)
    
    results = collection.query(query_texts=[query.query], n_results=query.n_results)
    print(results)
    if results["ids"] and results["ids"][0]:    
        return {
        "query": query,
        "result": {
            "id": results["ids"][0][0],
            "document": results["documents"][0][0],
            "metadata": results["metadatas"][0][0],
            "distance": results["distances"][0][0],
        },
    }
