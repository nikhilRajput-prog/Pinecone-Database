from .pdf_loader import load_pdf
from .chunker import create_chunks
from .embeddings import create_embeddings
from .pinecone_db import create_index, get_index


PDF_PATH = "data/document.pdf"


def ingest():

    print("Creating Pinecone index...")

    create_index()

    print("Loading PDF...")

    pages = load_pdf(PDF_PATH)

    print(f"Pages loaded: {len(pages)}")

    print("Creating chunks...")

    chunks = create_chunks(pages)

    print(f"Total chunks: {len(chunks)}")

    index = get_index()

    batch_size = 100

    for start in range(0, len(chunks), batch_size):

        batch = chunks[start:start + batch_size]

        texts = [
            chunk["text"]
            for chunk in batch
        ]

        print(
            f"Embedding chunks "
            f"{start} - {start + len(batch)}"
        )

        embeddings = create_embeddings(texts)

        vectors = []

        for chunk, embedding in zip(
            batch,
            embeddings
        ):

            vectors.append({
                "id": chunk["id"],

                "values": embedding,

                "metadata": {
                    "text": chunk["text"],
                    "page": chunk["page"]
                }
            })

        index.upsert(
            vectors=vectors
        )

        print("Uploaded batch.")

    print("Ingestion completed.")


if __name__ == "__main__":

    ingest()