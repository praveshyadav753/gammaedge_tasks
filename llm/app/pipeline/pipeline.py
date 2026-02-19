import openai
from chromadb import Client
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Set up OpenAI API key
openai.api_key = "your-openai-api-key"

# Connect to Chroma (assuming you've already set up your collection)
chroma_client = Client()
collection = chroma_client.get_collection("my_docs")

# Function to embed text using OpenAI embeddings
def embed_text(text: str):
    response = openai.Embedding.create(
        model="text-embedding-3-small",
        input=text
    )
    return response['data'][0]['embedding']

# Function to retrieve top-N documents from ChromaDB
def retrieve_top_n(query_embedding, n=20):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n,
        include=["documents", "metadatas", "distances"]
    )
    return results['documents'][0], results['metadatas'][0], results['distances'][0]

# Re-ranking function (optional: you could use a more complex model)
def rerank_documents(query, docs, distances):
    # Here we simply use cosine similarity between the query and top-20 results
    query_embedding = embed_text(query)
    doc_embeddings = [embed_text(doc) for doc in docs]
    similarities = cosine_similarity([query_embedding], doc_embeddings)
    
    # Zip docs with their similarity score and sort by similarity
    reranked_docs = sorted(zip(docs, similarities[0], distances), key=lambda x: x[1], reverse=True)
    
    return reranked_docs

# Search pipeline function
def search_pipeline(query: str, threshold=0.7, top_n=20, top_k=5):
    # Step 1: Embed the query
    query_embedding = embed_text(query)

    # Step 2: Retrieve top-N documents from ChromaDB
    docs, metas, distances = retrieve_top_n(query_embedding, n=top_n)

    # Step 3: Threshold check (if best score is too low, return a fallback message)
    best_score = 1 - distances[0]  # if using cosine distance
    if best_score < threshold:
        return {"answer": "I don't have enough information to answer that."}
    
    # Step 4: Re-rank documents based on query similarity
    reranked_docs = rerank_documents(query, docs, distances)
    
    # Step 5: Return top-K (e.g., top 5)
    top_k_docs = reranked_docs[:top_k]
    return {
        "query": query,
        "top_results": [
            {"document": doc, "score": score, "metadata": meta} 
            for doc, score, meta in top_k_docs
        ]
    }

# Example query
query = "What are the benefits of machine learning?"
result = search_pipeline(query)
print(result)
