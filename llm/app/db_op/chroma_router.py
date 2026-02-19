from fastapi import APIRouter, HTTPException, UploadFile, File
import uuid
import os
from .connect import collection
# from utility.getemb import get_embeddings as embed_text
from pydantic import BaseModel
from .pdf_reader import load_pdf, chunk_text
from utility.getemb import embed_text
from uuid import uuid4
import shutil

Chroma_router = APIRouter(prefix="/chroma_db", tags=["chromadb"])
UPLOAD_DIR = "uploads"
# UPLOAD_DIR="llm/app/uploads"


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


@Chroma_router.post("/add_document_chunk")
async def add_document_chunks(file: UploadFile = File(...)):
    try:
        file_extension = os.path.splitext(file.filename)[1]
        new_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, new_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        pdf_text = load_pdf(file_path)
        # print("--------------------",pdf_text)
        chunks = chunk_text(pdf_text, chunk_size=500, overlap=50)
        # print(chunks)
        print("adding ....")

        for i, chunk in enumerate(chunks):

            embed_chunk = await embed_text(chunk)
            # print(embed_chunk)
            collection.add(
                ids=[str(uuid4())],
                embeddings=[embed_chunk],
                documents=[chunk],
                metadatas=[{"source": new_filename, "chunk": i}],
            )
        count=collection.count()    
        print(i, "added")
        return {"message": f"Document  added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@Chroma_router.post("/search")
async def search(query: SearchInput):
    query_embedding = await embed_text(query.query)
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=query.n_results,
            query_texts = query.query,
        )
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
