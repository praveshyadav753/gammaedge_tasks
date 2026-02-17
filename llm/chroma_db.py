import chromadb
from  datetime import datetime# client = chromadb.Client()

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(
            name="my_collection",
             metadata={
        "description": "my first Chroma collection",
        "created": str(datetime.now())
    })
collections = chroma_client.get_collection(name="my_collection")
print(collections)
collection.add(
    documents=[
        "My name is anthony gonsalves",
        " jeans"
    ],
    ids=["id1", "id2"]
)

results = collection.query(
    query_texts=["what is your name"], # Chroma will embed this for you
    n_results=2 # how many results to return
)

print(results)
