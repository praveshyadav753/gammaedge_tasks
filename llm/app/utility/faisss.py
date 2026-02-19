import faiss
import numpy as np
import pickle
from .getemb import get_embeddings

class FaissStore:
    def __init__(self, dimension=1536):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []

    async def add_documents(self, documents):
        texts = [doc["text"] for doc in documents]
        embeddings = await get_embeddings(texts)

        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(documents)

    def search(self, query, top_k=5):
        query_vector = np.array([get_embeddings([query])[0]]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        results = [self.metadata[idx] for idx in indices[0]]
        return results

    def save(self):
        faiss.write_index(self.index, "app/index/faiss.index")
        with open("app/index/metadata.pkl", "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):
        self.index = faiss.read_index("app/index/faiss.index")
        with open("app/index/metadata.pkl", "rb") as f:
            self.metadata = pickle.load(f)
