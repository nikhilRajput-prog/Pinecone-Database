from openai import OpenAI

from .config import (
    OPENAI_API_KEY,
    LLM_MODEL,
    TOP_K
)

from .embeddings import create_embedding
from .pinecone_db import get_index


client = OpenAI(
    api_key=OPENAI_API_KEY
)


def retrieve_documents(question):

    index = get_index()

    query_embedding = create_embedding(
        question
    )

    results = index.query(
        vector=query_embedding,
        top_k=TOP_K,
        include_metadata=True
    )

    documents = []

    for match in results["matches"]:

        metadata = match["metadata"]

        documents.append({
            "text": metadata["text"],
            "page": metadata["page"],
            "score": match["score"]
        })

    return documents


def generate_answer(question, documents):

    context_parts = []

    for doc in documents:

        context_parts.append(
            f"""
Page: {doc['page']}

{doc['text']}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    prompt = f"""
You are a helpful assistant answering questions
from a PDF document.

Use ONLY the provided context to answer the question.

If the answer cannot be found in the context,
say:

"I could not find the answer in the document."

Do not make up information.

Always mention the relevant page number when possible.

CONTEXT:

{context}

QUESTION:

{question}
"""

    response = client.chat.completions.create(

        model=LLM_MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "You answer questions using "
                    "retrieved document context."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )

    return response.choices[0].message.content


def ask_question(question):

    documents = retrieve_documents(
        question
    )

    answer = generate_answer(
        question,
        documents
    )

    return answer, documents