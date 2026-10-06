# import streamlit as st
# from dotenv import load_dotenv
# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# # Load .env variables
# load_dotenv()
# google_api_key = os.getenv("GOOGLE_API_KEY")

# # LLM Setup
# llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-latest", google_api_key=google_api_key, temperature=0.7)

# # Prompt template
# prompt = PromptTemplate(
#     input_variables=["resume"],
#     template="""
# You are an expert career coach and resume writer. Please rewrite the following resume in a much more professional tone. Improve clarity, fix grammar, and present the content in a way that appeals to employers.

# Resume:
# {resume}

# Professional Resume:
# """
# )

# # Create the chain
# chain = LLMChain(llm=llm, prompt=prompt)

# # Streamlit UI
# st.title("📄 Resume Rewriter with Gemini + LangChain")
# st.write("Paste your raw resume below, and we'll rewrite it in a professional tone using AI.")

# # Text input
# user_resume = st.text_area("Paste your resume here:", height=150)

# # Button to trigger rewriting
# if st.button("Rewrite Resume"):
#     if user_resume.strip():
#         with st.spinner("Rewriting..."):
#             result = chain.run(resume=user_resume)
#             st.success("Here’s your improved resume:")
#             st.text_area("Professional Resume", result, height=300)
#     else:
#         st.warning("Please paste a resume before clicking the button.")


import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY is missing from your .env file.")
    st.stop()

# Gemini client
client = genai.Client(api_key=api_key)

# Streamlit configuration
st.set_page_config(
    page_title="Resume Rewriter",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Resume Rewriter with Gemini")

st.write(
    "Paste your resume below and Gemini will rewrite it "
    "in a professional, employer-friendly format."
)

user_resume = st.text_area(
    "Paste your resume here:",
    height=350,
    placeholder="Paste your resume here..."
)

if st.button("Rewrite Resume", type="primary"):

    if not user_resume.strip():
        st.warning("Please paste a resume before clicking the button.")

    else:
        prompt = f"""
You are an expert career coach and professional resume writer.

Rewrite the following resume in a professional, clear and compelling way.

Requirements:
- Correct grammar and spelling.
- Improve clarity and professional tone.
- Preserve the candidate's actual experience and qualifications.
- Do not invent jobs, qualifications, achievements, responsibilities,
  technologies, or experience.
- Use strong but truthful professional language.
- Make the resume appealing to employers.
- Keep important technical skills and achievements.
- Organize the content into appropriate professional resume sections.

Resume:
{user_resume}

Return only the improved professional resume.
"""

        with st.spinner("Rewriting your resume..."):

            try:
                response = client.interactions.create(
                    model="gemini-3.8-flash",
                    input=prompt,
                )

                result = response.output_text

                st.success("Resume rewritten successfully!")

                st.text_area(
                    "Professional Resume",
                    result,
                    height=600,
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
