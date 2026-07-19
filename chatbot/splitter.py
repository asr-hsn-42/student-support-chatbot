def split_documents(documents, chunk_size=500, overlap=100):
    """
    Split document text into overlapping chunks.

    Args:
        documents (list): Output from loader.py
        chunk_size (int): Number of characters per chunk
        overlap (int): Overlap between consecutive chunks

    Returns:
        list: Chunks with source information
    """

    chunks = []

    for document in documents:

        text = document["text"]
        source = document["source"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end]

            chunks.append({
                "text": chunk,
                "source": source
            })

            start += chunk_size - overlap

    return chunks