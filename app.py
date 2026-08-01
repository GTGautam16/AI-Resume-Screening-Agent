import streamlit as st
import pandas as pd
import json

from services.pdf_reader import (save_uploaded_file, extract_text_from_pdf, clean_text)
from services.database import (save_resume, get_all_resumes, resume_exists)
from services.vector_store import (store_resume_embedding, get_embedding_count, search_similar_resumes)
from services.rag import answer_with_rag

from agents.planner import run_resume_pipeline


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

analyze_button = st.button( "🚀 Analyze Resume", use_container_width=True )

st.subheader("🔍 Semantic Resume Search")
search_query = st.text_input("Search resumes using natural language")
search_button = st.button("Search")

if search_button and search_query:
    with st.spinner("Searching resumes..."):
        answer = answer_with_rag(search_query)

    st.subheader("🤖 AI Answer")
    st.write(answer)

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

        with st.spinner("🤖 AI is analyzing the resume..."):
            result = run_resume_pipeline(resume_text, jd_text)

            parsed_resume = result["parsed_resume"]
            analysis = result["analysis"]
            interview_questions = result["interview_questions"]
            learning_roadmap = result["learning_roadmap"]

        existing_resume = resume_exists(resume_path,jd_path)

        if existing_resume:
            st.warning("This Resume and Job Description have already been analyzed.")
            st.stop()

        resume = save_resume(
            resume_path,
            jd_path,
            resume_text,
            jd_text,
            analysis["match_percentage"],
            "\n".join(analysis["strengths"]),
            "\n".join(analysis["missing_skills"]),
            "\n".join(analysis["recommendations"]),
            analysis
        )

        store_resume_embedding(
            resume.id,
            resume_text
        )

        st.success(f"Total Embeddings Stored: {get_embedding_count()}")
        
        st.success(
            f"Files uploaded and saved successfully! Resume ID: {resume.id}"
        )

        # -----------------------------
        # Current Resume
        # -----------------------------

        st.subheader("📄 Resume Text")

        st.text_area(
            "Extracted Resume",
            resume_text,
            height=250,
            key="current_resume"
        )

        st.subheader("💼 Job Description Text")

        st.text_area(
            "Extracted JD",
            jd_text,
            height=250,
            key="current_jd"
        )

        # -----------------------------
        # Current AI Analysis
        # -----------------------------

        st.subheader("🤖 Current AI Analysis")

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

        # -----------------------------
        # AI Interview Questions
        # -----------------------------

        st.divider()

        st.subheader("🎤 AI Interview Questions")

        st.write(interview_questions)
        
        # -----------------------------
        # Personalized Learning Roadmap
        # -----------------------------

        st.divider()

        st.subheader("🛣️ Personalized Learning Roadmap")

        st.write(learning_roadmap)

        # -----------------------------
        # Stored Resume List
        # -----------------------------

        st.divider()

        all_resumes = get_all_resumes()

        st.subheader("📋 Stored Resumes")

        resume_data = []

        for r in all_resumes:
            resume_data.append(
                {
                    "ID": r.id,
                    "Resume Path": r.resume_path,
                    "Uploaded At": r.created_at,
                    "Match %": r.match_percentage
                }
            )

        df = pd.DataFrame(resume_data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # -----------------------------
        # Previous Analyses
        # -----------------------------

        if len(all_resumes) > 1:

            st.divider()

            st.subheader("📚 Previous AI Analyses")

            for resume in reversed(all_resumes):

                st.divider()

                st.subheader(f"Resume #{resume.id}")

                st.metric( "Match Percentage", f"{resume.analysis_json['match_percentage']}%" )

                st.subheader("✅ Strengths")

                for strength in resume.analysis_json["strengths"]:
                    st.write(f"• {strength}")

                st.subheader("❌ Missing Skills")

                for skill in resume.analysis_json["missing_skills"]:
                    st.write(f"• {skill}")

                st.subheader("💡 Recommendations")

                for recommendation in resume.analysis_json["recommendations"]:
                    st.write(f"• {recommendation}")