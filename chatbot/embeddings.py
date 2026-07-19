from config import EMBEDDING_MODEL
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(EMBEDDING_MODEL)


def create_embeddings(chunks):
    """
    Convert text chunks into embeddings.

    Args:
        chunks (list): Output from splitter.py

    Returns:
        tuple: (embeddings, chunks)
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    return embeddings, chunks