from .config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk.strip())

        start += chunk_size - overlap

    return chunks


def create_chunks(pages):

    all_chunks = []

    chunk_id = 0

    for page in pages:

        chunks = chunk_text(page["text"])

        for chunk in chunks:

            all_chunks.append({
                "id": f"chunk-{chunk_id}",
                "text": chunk,
                "page": page["page"]
            })

            chunk_id += 1

    return all_chunks