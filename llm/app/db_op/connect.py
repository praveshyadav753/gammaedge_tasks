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

client = chromadb.Client(
    Settings(
        persist_directory="./chroma_db",
        is_persistent=True
    )
)
default_ef = embedding_functions.DefaultEmbeddingFunction()


collection = client.get_or_create_collection(
    name="files",
    # embedding_function=default_ef
)

collections = client.list_collections()

print("Collections in ChromaDB:")

# for col in collections:
#     print(col.name)
# alldata = collection.get()
# print(collection.count())
# print(alldata)

