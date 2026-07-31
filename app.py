import streamlit as st
import pandas as pd
import json

from services.pdf_reader import (save_uploaded_file, extract_text_from_pdf, clean_text)
from services.database import (save_resume, get_all_resumes)

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

        resume = save_resume(
                resume_path,
                jd_path,
                resume_text,
                jd_text
                )

        from services.llm import ask_llm

        prompt = f"""
                You are an expert AI Resume Screening Assistant.

                Compare the following resume against the job description.

                Resume:
                {resume_text}

                Job Description:
                {jd_text}

                Return ONLY valid JSON.

                Format:

                {{
                    "match_percentage": 0,
                    "strengths": [],
                    "missing_skills": [],
                    "recommendations": []
                }}

                Do not include markdown.
                Do not include explanations.
                Return JSON only.
                """

        analysis = ask_llm(prompt)

        analysis = json.loads(analysis)

        st.success(f"Files uploaded and saved successfully! Resume ID: {resume.id}")

        all_resumes = get_all_resumes()

        st.subheader("Stored Resumes")

        resume_data = []

        for resume in all_resumes:
            resume_data.append(
                {
                    "ID": resume.id,
                    "Resume Path": resume.resume_path,
                    "Uploaded At": resume.created_at
                }
            )

        df = pd.DataFrame(resume_data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
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

        st.subheader("🤖 AI Analysis")

        st.metric(
            "Match Percentage",
            f"{analysis['match_percentage']}%"
        )

        st.subheader("✅ Strengths")

        for item in analysis["strengths"]:
            st.write(f"• {item}")

        st.subheader("❌ Missing Skills")

        for item in analysis["missing_skills"]:
            st.write(f"• {item}")

        st.subheader("💡 Recommendations")

        for item in analysis["recommendations"]:
            st.write(f"• {item}")