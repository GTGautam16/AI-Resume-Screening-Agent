import streamlit as st

from services.pdf_reader import (
    save_uploaded_file,
    extract_text_from_pdf,
    clean_text
)

from services.database import (
    save_resume,
    resume_exists
)

from services.vector_store import (
    store_resume_embedding
)

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

# -----------------------------
# Upload Section
# -----------------------------

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

# -----------------------------
# Semantic Search
# -----------------------------

st.subheader("🔍 Semantic Resume Search")

search_query = st.text_input(
    "Search resumes using natural language"
)

search_button = st.button("Search")

if search_button and search_query:

    with st.spinner("Searching resumes..."):
        answer = answer_with_rag(search_query)

    st.subheader("🤖 AI Answer")
    st.write(answer)

# -----------------------------
# Resume Analysis
# -----------------------------

if analyze_button:

    if resume_file is None or jd_file is None:

        st.error("Please upload both Resume and Job Description PDFs.")
        st.stop()

    resume_path = save_uploaded_file(resume_file)
    jd_path = save_uploaded_file(jd_file)

    try:

        resume_text = clean_text(
            extract_text_from_pdf(resume_path)
        )

        jd_text = clean_text(
            extract_text_from_pdf(jd_path)
        )

    except Exception as e:

        st.error(str(e))
        st.stop()

    existing_resume = resume_exists(
        resume_path,
        jd_path
    )

    if existing_resume:

        st.info(
            "ℹ️ This Resume and Job Description have already been analyzed."
        )
        st.stop()

    with st.spinner("🤖 AI is analyzing the resume..."):

        result = run_resume_pipeline(
            resume_text,
            jd_text
        )

        analysis = result["analysis"]
        interview_questions = result["interview_questions"]
        learning_roadmap = result["learning_roadmap"]

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

    st.success("✅ Resume analyzed successfully!")

    # -----------------------------
    # Result Tabs
    # -----------------------------

    tab1, tab2, tab3 = st.tabs(
        [
            "📊 Analysis",
            "🎤 Interview",
            "🛣️ Roadmap"
        ]
    )

    # -----------------------------
    # Analysis Tab
    # -----------------------------

    with tab1:

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

    # -----------------------------
    # Interview Tab
    # -----------------------------

    with tab2:

        st.subheader("🎤 AI Interview Questions")

        st.write(interview_questions)

    # -----------------------------
    # Roadmap Tab
    # -----------------------------

    with tab3:

        st.subheader("🛣️ Personalized Learning Roadmap")

        st.write(learning_roadmap)