# app/utils/text_splitter.py

def split_text(text: str, chunk_size: int = 500, overlap: int = 50):

    if overlap >= chunk_size:
        overlap = 0

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks