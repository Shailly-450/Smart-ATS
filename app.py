# import streamlit as st
# import google.generativeai as genai
# import os
# from PyPDF2 import PdfReader
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Check and configure the API key
# api_key = os.getenv("GOOGLE_API_KEY")
# if not api_key:
#     raise ValueError("GOOGLE_API_KEY not found in environment variables")

# genai.configure(api_key=api_key)

# # Define function to get response from the Gemini Pro model
# def get_gemini_response(input_text):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content(input_text)
#     return response.text

# # Define function to extract text from PDF
# def input_pdf_text(uploaded_file):
#     reader = PdfReader(uploaded_file)
#     text = ""
#     for page_num in range(len(reader.pages)):
#         page = reader.pages[page_num]
#         text += page.extract_text()
#     return text

# Define the input prompt template
# input_prompt_template = """
# Hey Act Like a skilled or very experienced ATS(Application Tracking System)
# with a deep understanding of tech field, software engineering, data science, data analyst
# and big data engineer. Your task is to evaluate the resume based on the given job description.
# You must consider the job market is very competitive and you should provide
# best assistance for improving the resumes. Assign the percentage Matching based
# on the job description and the missing keywords with high accuracy.

# resume:{text}
# description:{jd}

# I want the response in one single string having the structure
# {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
# """


# # Streamlit App
# st.title("Smart ATS")
# st.text("Improve Your Resume with ATS")

# # Input fields for job description and resume upload
# jd = st.text_area("Paste the Job Description")
# uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

# # Submit button
# submit = st.button("Submit")

# if submit:
#     if uploaded_file is not None and jd:
#         text = input_pdf_text(uploaded_file)
#         input_prompt = input_prompt_template.format(text=text, jd=jd)
#         response = get_gemini_response(input_prompt)
#         st.subheader("Evaluation Result")
#         st.text(response)
#     else:
#         st.error("Please provide both a job description and upload your resume.")

import streamlit as st
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Check and configure the API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

# Define function to get response from the Gemini Pro model
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# Define function to extract text from PDF
def input_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

# Define the input prompt template
input_prompt_template = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, data analyst, 
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider that the job market is very competitive and provide the best assistance for improving resumes. 
Assign the percentage Matching based on the job description and the missing keywords with high accuracy.

Additionally, provide the following in your response:
1. A list of missing keywords.
2. A matching score that can be visualized.
3. Any other metrics that could be useful for visualizations.

Resume:
{text}

Description:
{jd}

I want the response in a structured format that includes:
{{
  "JD Match": "%",
  "MissingKeywords": [],
  "Metrics": {{
    "keyword_counts": {{"keyword1": count, "keyword2": count, ...}},
    "additional_metrics": {{}}
  }},
  "Profile Summary": ""
}}
"""

# Streamlit App
st.title("Smart ATS")
st.text("Improve Your Resume with ATS")

# Input fields for job description and resume upload
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

# Submit button
submit = st.button("Submit")

if submit:
    if uploaded_file is not None and jd:
        text = input_pdf_text(uploaded_file)
        # Format the input prompt with the actual values
        input_prompt = input_prompt_template.format(text=text, jd=jd)
        try:
            response = get_gemini_response(input_prompt)
            response_data = json.loads(response)
            
            st.subheader("Evaluation Result")
            st.json(response_data)  # Display response data in JSON format

            # Example of how you might handle visualization based on response_data
            # You would need to add your visualization logic here

        except json.JSONDecodeError:
            st.error("Failed to parse response data.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please provide both a job description and upload your resume.")

