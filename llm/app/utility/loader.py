from pathlib import Path
import pypdf

current_file_path = Path(__file__).resolve()

current_dir = current_file_path.parent.parent
BOOK_PATH = current_dir/"llm.pdf"

def chunk_text(text, chunk_size=99, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def load_documents():
    with open(BOOK_PATH, "r", encoding="utf-8", errors="ignore") as f:       
        text = f.read()

    chunks = chunk_text(text)
    documents = []

    for i, chunk in enumerate(chunks):
        documents.append({
            "id": f"chunk_{i}",
            "text": chunk,
            "source": "mybook"
        })

    return documents
