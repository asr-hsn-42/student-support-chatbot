import faiss
import numpy as np
import pickle
import os


class VectorStore:

    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)
        self.chunks = []

    def add(self, embeddings, chunks):
        """
        Store embeddings and their corresponding chunks.
        """

        self.index.add(
            np.array(embeddings).astype("float32")
        )

        self.chunks.extend(chunks)

    def search(self, query_embedding, k=3):
        """
        Search the top k most similar chunks.
        """

        distances, indices = self.index.search(
            np.array([query_embedding]).astype("float32"),
            k
        )

        results = []

        for idx in indices[0]:
            results.append(self.chunks[idx])

        return results

    def save(self, folder_path="vector_db"):
        """
        Save FAISS index and metadata to disk.
        """

        os.makedirs(folder_path, exist_ok=True)

        faiss.write_index(
            self.index,
            os.path.join(folder_path, "index.faiss")
        )

        with open(
            os.path.join(folder_path, "metadata.pkl"),
            "wb"
        ) as f:
            pickle.dump(self.chunks, f)

        print("✅ Vector database saved successfully.")

    @classmethod
    def load(cls, folder_path="vector_db"):
        """
        Load FAISS index and metadata from disk.
        """

        index_path = os.path.join(folder_path, "index.faiss")
        metadata_path = os.path.join(folder_path, "metadata.pkl")

        if not os.path.exists(index_path):
            raise FileNotFoundError("FAISS index not found.")

        if not os.path.exists(metadata_path):
            raise FileNotFoundError("Metadata file not found.")

        index = faiss.read_index(index_path)

        with open(metadata_path, "rb") as f:
            chunks = pickle.load(f)

        store = cls(index.d)

        store.index = index
        store.chunks = chunks

        print("✅ Vector database loaded successfully.")

        return store