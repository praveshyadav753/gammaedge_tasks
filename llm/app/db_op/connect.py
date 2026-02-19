# ingest.py
import chromadb
from pathlib import Path
from chromadb.config import Settings
from .pdf_reader import load_pdf
from utility.getemb import get_embeddings as embed_text
from chromadb.utils import embedding_functions

current_file_path = Path(__file__).resolve()

current_dir = current_file_path.parent.parent
BOOK_PATH = current_dir/"llm.pdf"
client = chromadb.Client(Settings(persist_directory="./chroma_db"))
# collection = client.get_or_create_collection(name="llm")

default_ef = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="single_pdf",
    embedding_function=default_ef
)
collections = client.list_collections()
print("Collections in ChromaDB:")
for col in collections:
    print(col.name)

def ingest():
    # client = chromadb.Client(Settings(persist_directory="./chroma_db"))
    # collection = client.get_or_create_collection(name="llm")

    text = load_pdf("llm.pdf")
    embedding = embed_text([text])[0]

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=["document_1"],
        metadatas=[{"source": "document.pdf"}]
    )

    print("PDF successfully ingested.")

# if __name__ == "__main__":
#     ingest()
