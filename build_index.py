from chatbot.loader import load_documents
from chatbot.splitter import split_documents
from chatbot.embeddings import create_embeddings
from chatbot.vectorstore import VectorStore

print("=" * 50)
print("Building Vector Database...")
print("=" * 50)

print("Loading documents...")
documents = load_documents()

print(f"Loaded {len(documents)} documents.")

print("Splitting documents...")
chunks = split_documents(documents)

print(f"Created {len(chunks)} chunks.")

print("Creating embeddings...")
embeddings, chunks = create_embeddings(chunks)

print("Building FAISS index...")
store = VectorStore(embeddings.shape[1])
store.add(embeddings, chunks)

print("Saving vector database...")
store.save("vector_db")

print("\n✅ Vector database built successfully!")
print("Files created:")
print("  vector_db/index.faiss")
print("  vector_db/metadata.pkl")