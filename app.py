import streamlit as st

import requests

from config import API_URL


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

        response = requests.post(
            f"{API_URL}/search",
            json={
                "query": search_query
            }
        )

        answer = response.json()["answer"]

    st.subheader("🤖 AI Answer")
    st.write(answer)

# -----------------------------
# Resume Analysis
# -----------------------------

if analyze_button:

    if resume_file is None or jd_file is None:

        st.error("Please upload both Resume and Job Description PDFs.")
        st.stop()

    files = {
    "resume": (
        resume_file.name,
        resume_file.getvalue(),
        "application/pdf"
    ),
    "jd": (
        jd_file.name,
        jd_file.getvalue(),
        "application/pdf"
    )
    }

    response = requests.post(
        f"{API_URL}/analyze",
        files=files
    )

    if response.status_code != 200:
        st.error(response.text)
        st.stop()

    result = response.json()

    analysis = result["analysis"]
    interview_questions = result["interview_questions"]
    learning_roadmap = result["learning_roadmap"]

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