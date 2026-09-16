import streamlit as st

from src.rag import ask_question


st.set_page_config(
    page_title="PDF RAG",
    page_icon="📚"
)


st.title("📚 PDF RAG Chatbot")

st.write(
    "Ask questions about your 900-page PDF."
)


if "messages" not in st.session_state:

    st.session_state.messages = []


# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# Chat input

question = st.chat_input(
    "Ask a question..."
)


if question:

    # User message

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):

        st.markdown(question)


    # Assistant response

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching the document..."
        ):

            answer, documents = ask_question(
                question
            )

        st.markdown(answer)


        # Sources

        with st.expander(
            "📖 Sources"
        ):

            for i, doc in enumerate(
                documents
            ):

                st.write(
                    f"**Source {i + 1}**"
                )

                st.write(
                    f"Page: {doc['page']}"
                )

                st.write(
                    f"Similarity: "
                    f"{doc['score']:.4f}"
                )

                st.write(
                    doc["text"]
                )

                st.divider()


    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })