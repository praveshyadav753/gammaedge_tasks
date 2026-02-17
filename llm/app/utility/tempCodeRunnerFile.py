from loader import load_documents
from faisss import FaissStore

docs = load_documents()
store = FaissStore()
store.add_documents(docs)
store.save()

print("Book indexed successfully!")
