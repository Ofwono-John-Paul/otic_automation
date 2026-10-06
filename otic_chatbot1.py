import os

import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate

from qdrant_client import QdrantClient


# 1. LOAD ENVIRONMENT VARIABLES

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# Check required environment variables
if not QDRANT_URL:
    st.error("QDRANT_URL is missing from your .env file.")
    st.stop()

if not QDRANT_API_KEY:
    st.error("QDRANT_API_KEY is missing from your .env file.")
    st.stop()

if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY is missing from your .env file.")
    st.stop()


# 2. STREAMLIT PAGE CONFIGURATION

st.set_page_config(
    page_title="OTIC Foundation AI Assistant",
    page_icon="🤖",
    layout="wide",
)

# 3. GEMINI LLM

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)


# 4. HUGGING FACE EMBEDDINGS

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# 5. QDRANT CLIENT

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)


# 6. CONNECT TO EXISTING QDRANT COLLECTION

qdrant = QdrantVectorStore(
    client=client,
    collection_name="otic-knowledge-base",
    embedding=embeddings,
)


# 7. CREATE RETRIEVER

retriever = qdrant.as_retriever(
    search_kwargs={
        "k": 6
    }
)


# 8. RAG PROMPT

prompt = ChatPromptTemplate.from_template(
    """
You are the OTIC Foundation AI Assistant.

Your task is to answer questions about the OTIC Foundation
using the information retrieved from the OTIC knowledge base.

Follow these rules:

1. Use the provided context as your primary source of information.
2. Do not invent information.
3. Do not make unsupported assumptions.
4. If the answer cannot be found in the provided context,
   clearly state that the information is not available in
   the OTIC knowledge base.
5. Give clear, professional and concise answers.
6. When useful, organize the answer using bullet points.
7. Do not mention "the retrieved documents" unless necessary.

CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""
)


# 9. STREAMLIT USER INTERFACE

st.title("🤖 OTIC Foundation AI Assistant")

st.write(
    "Ask questions about the OTIC Foundation using information "
    "from the organization's knowledge base."
)


# 10. USER INPUT

query = st.text_input(
    "Type your question here:",
    placeholder="e.g. What does OTIC Foundation do?"
)


# 11. PROCESS USER QUESTION

if query:

    with st.spinner("Searching the OTIC knowledge base..."):

        try:

            # Retrieve relevant documents from Qdrant

            documents = retriever.invoke(query)


            # Check whether documents were found

            if not documents:

                st.warning(
                    "I couldn't find relevant information "
                    "in the OTIC knowledge base."
                )

            else:

                # Combine retrieved document content

                context = "\n\n".join(
                    document.page_content
                    for document in documents
                )


                # Build the prompt

                messages = prompt.invoke(
                    {
                        "context": context,
                        "question": query,
                    }
                )


                # Send request to Gemini
                response = llm.invoke(messages)

                answer = response.content

                # Display response

                st.success("Done!")

                st.markdown("### Your Question")

                st.write(query)

                st.markdown("### 🤖 OTIC Bot")

                st.markdown(answer)


                # Display source chunks

                with st.expander(
                    "📚 Show Source Chunks Used"
                ):

                    for i, document in enumerate(documents):

                        st.markdown(
                            f"**Chunk {i + 1}**"
                        )

                        st.code(
                            document.page_content
                        )

                        # Display metadata if available
                        if document.metadata:

                            st.caption(
                                f"Metadata: {document.metadata}"
                            )


        except Exception as e:

            st.error(
                f"An error occurred while processing your question: {e}"
            )