import streamlit as st
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load .env variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# LLM Setup
llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-latest", google_api_key=google_api_key, temperature=0.7)

# Prompt template
prompt = PromptTemplate(
    input_variables=["resume"],
    template="""
You are an expert career coach and resume writer. Please rewrite the following resume in a much more professional tone. Improve clarity, fix grammar, and present the content in a way that appeals to employers.

Resume:
{resume}

Professional Resume:
"""
)

# Create the chain
chain = LLMChain(llm=llm, prompt=prompt)

# Streamlit UI
st.title("📄 Resume Rewriter with Gemini + LangChain")
st.write("Paste your raw resume below, and we'll rewrite it in a professional tone using AI.")

# Text input
user_resume = st.text_area("Paste your resume here:", height=150)

# Button to trigger rewriting
if st.button("Rewrite Resume"):
    if user_resume.strip():
        with st.spinner("Rewriting..."):
            result = chain.run(resume=user_resume)
            st.success("Here’s your improved resume:")
            st.text_area("Professional Resume", result, height=300)
    else:
        st.warning("Please paste a resume before clicking the button.")
