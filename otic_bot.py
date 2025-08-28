import streamlit as st
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

# Load environment variables (Google API Key)
load_dotenv()

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Title
st.title("OTIC Interaction Bot")
st.markdown("Ask me anything about the OTIC Foundation. Type your question below:")

# Load vector store and retriever
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("otic_vectorstore", embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever()

# Load Google Gemini model
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash-latest",  # or use a Gemini model name you have access to
    temperature=0.1
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"
)

# Input field
user_input = st.text_input("Your question", key="user_question")

# Handle user query
if user_input:
    # Save to history
    st.session_state.chat_history.append({"question": user_input})
    # Run the QA chain
    try:
        answer = qa_chain.run(user_input)
        st.session_state.chat_history[-1]["answer"] = answer
    except Exception as e:
        st.session_state.chat_history[-1]["answer"] = f"⚠️ Error: {e}"

# Display conversation
for chat in st.session_state.chat_history:
    st.markdown(f"**🧍 You:** {chat['question']}")
    st.markdown(f"**🤖 OTIC Bot:** {chat['answer']}\n")

# Option to clear chat
if st.button("Clear Chat"):
    st.session_state.chat_history = []
