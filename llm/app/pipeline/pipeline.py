from db_op.connect import collection
from utility.getemb import embed_text
from sentence_transformers import SentenceTransformer, util
import torch

async def retrieve_top_n(query_embedding, n=20):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n,
        include=["documents", "metadatas", "distances"]
    )

    if not results["documents"] or not results["documents"][0]:
        return [], [], []
    return (
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    )




model = SentenceTransformer('all-MiniLM-L6-v2')  # lightweight, fast, good for reranking

async def search_pipeline(query: str, threshold=0.4, top_n=20, top_k=5):
    query_embedding_db = await embed_text(query)
    docs, metas, _ = await retrieve_top_n(query_embedding_db, n=top_n)
    
    if not docs:
        return {"answer": "No documents found in database."}

    query_embedding_model = model.encode(query, convert_to_tensor=True)
    doc_embeddings_model = model.encode(docs, convert_to_tensor=True)

    cosine_scores = util.cos_sim(query_embedding_model, doc_embeddings_model)[0]

    scored_results = []
    for doc, meta, score in zip(docs, metas, cosine_scores):
        similarity = float(score) 
        if similarity >= threshold:
            scored_results.append({
                "document": doc,
                "metadata": meta,
                "score": round(similarity, 4)
            })

    scored_results.sort(key=lambda x: x["score"], reverse=True)
    top_results = scored_results[:top_k]

    if not top_results:
        return {"answer": "I don't have enough information to answer that."}

    return {
        "query": query,
        "top_results": top_results
    }
