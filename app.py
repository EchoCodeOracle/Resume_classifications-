import streamlit as st
import pandas as pd
import docx2txt
import PyPDF2
import re

# Function to extract text from uploaded resume file
def extract_text(file):
    text = ""
    if file.type == "application/pdf":
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            for page in range(pdf_reader.numPages):
                text += pdf_reader.getPage(page).extract_text()
        except Exception as e:
            st.error(f"Error extracting PDF text: {e}")
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            text = docx2txt.process(file)
        except Exception as e:
            st.error(f"Error extracting DOCX text: {e}")
    elif file.type == "text/csv" or file.type == "application/vnd.ms-excel" or file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        try:
            if file.type == "text/csv":
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            text = df.to_string(index=False)
        except Exception as e:
            st.error(f"Error reading file: {e}")
    else:
        st.warning("Unsupported file format. Please upload a PDF, DOCX, CSV, or Excel file.")
    return text

# Function to highlight skills in the resume
def extract_skills(text):
    skills = ["Python", "Machine Learning", "Data Analysis", "Deep Learning", "NLP", "SQL", "Java", "C++"]
    extracted_skills = []
    for skill in skills:
        if re.search(f"(?i)\\b{skill}\\b", text):
            extracted_skills.append(skill)
    return extracted_skills

# Function to extract years of experience from the resume
def extract_experience_years(text):
    experience_years = re.findall(r"\b\d{4}\b", text)
    if experience_years:
        min_year = min(map(int, experience_years))
        max_year = max(map(int, experience_years))
        experience = max_year - min_year
        return experience
    return "Experience years not found"

# Define the Streamlit app
def main():
    st.title('Resume Analyzer App')
    st.write('Upload a resume file to analyze its contents.')

    uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx", "csv", "xlsx"])

    if uploaded_file is not None:
        text = extract_text(uploaded_file)
        if text:
            # Extract skills from the resume
            extracted_skills = extract_skills(text)

            # Extract years of experience from the resume
            experience_years = extract_experience_years(text)

            # Create a table of resume holder
            data = {'Name': [uploaded_file.name], 'Experience (Years)': [experience_years], 'Skills': [', '.join(extracted_skills)]}
            df = pd.DataFrame(data)

            st.header('Extracted Resume Information')
            st.write(df)
        else:
            st.error("Could not extract text from the uploaded file.")

# Run the app
if __name__ == '__main__':
    main()
