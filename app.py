import streamlit as st
from services.pdf_reader import (save_uploaded_file, 
                                 extract_text_from_pdf, 
                                 clean_text)

st.set_page_config(
    page_title="AI Resume Screening Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Resume Screening Agent")
st.write("Upload a Resume and a Job Description to begin AI-powered analysis.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Resume")
    resume_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        key="resume"
    )

with col2:
    st.subheader("💼 Job Description")
    jd_file = st.file_uploader(
        "Upload Job Description (PDF)",
        type=["pdf"],
        key="jd"
    )

st.divider()

analyze_button = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)

if analyze_button:

    if resume_file is None or jd_file is None:
        st.error("Please upload both Resume and Job Description PDFs.")

    else:
        resume_path = save_uploaded_file(resume_file)
        jd_path = save_uploaded_file(jd_file)

        try:
            resume_text = clean_text(extract_text_from_pdf(resume_path))

            jd_text = clean_text(extract_text_from_pdf(jd_path))

        except Exception as e:
            st.error(str(e))
            st.stop()

        st.success("Files uploaded successfully!")

        st.subheader("Resume Text")

        st.text_area(
            "Extracted Resume",
            resume_text,
            height=300
        )

        st.subheader("Job Description Text")

        st.text_area(
            "Extracted JD",
            jd_text,
            height=300
        )