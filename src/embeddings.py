from openai import OpenAI

from .config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL
)


client = OpenAI(
    api_key=OPENAI_API_KEY
)


def create_embeddings(texts):

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts
    )

    embeddings = [
        item.embedding
        for item in response.data
    ]

    return embeddings


def create_embedding(text):

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response.data[0].embedding