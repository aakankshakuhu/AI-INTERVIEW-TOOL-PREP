import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
from app.session import InterviewSession

st.set_page_config(page_title="AI Interview Platform", layout="wide")

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "session" not in st.session_state:
    st.session_state.session = None

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "score" not in st.session_state:
    st.session_state.score = None


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

body {
background-color: #0E1117;
color: white;
}

.hero {
padding: 80px 20px;
text-align: center;
background: radial-gradient(circle at center, #6a00ff, #0e1117);
border-radius: 20px;
margin-bottom: 30px;
}

.hero h1{
font-size:48px;
font-weight:700;
}

.hero p{
font-size:20px;
color:#cfcfcf;
}

.card{
background: linear-gradient(145deg,#1f1f2e,#0e1117);
padding:25px;
border-radius:15px;
box-shadow:0px 10px 30px rgba(0,0,0,0.5);
}

.feature-title{
font-size:20px;
font-weight:600;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

selected = option_menu(
    menu_title=None,
    options=["Home","Start Interview","Dashboard","Reports"],
    icons=["house","mic","bar-chart","file-earmark"],
    orientation="horizontal"
)

# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

if selected == "Home":

    st.markdown("""
    <div class="hero">
    <h1>AI Interview Simulation Platform</h1>
    <p>Practice real-world technical interviews with AI-powered evaluation and feedback.</p>
    </div>
    """, unsafe_allow_html=True)

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Mock Interviews", "520+")
    col2.metric("Job Roles", "12")
    col3.metric("Topics Covered", "30+")
    col4.metric("Avg Score", "76%")

    st.subheader("Platform Features")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <div class="feature-title">AI Answer Evaluation</div>
        NLP based scoring using TF-IDF and similarity models.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <div class="feature-title">Topic-wise Analytics</div>
        Identify strengths and weaknesses across interview topics.
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <div class="feature-title">Download Interview Reports</div>
        Automatically generate JSON and PDF reports.
        </div>
        """, unsafe_allow_html=True)


# --------------------------------------------------
# START INTERVIEW
# --------------------------------------------------

elif selected == "Start Interview":

    st.title("🎤 Start Mock Interview")

    role = st.selectbox(
        "Select Job Role",
        ["Data Scientist","Machine Learning Engineer","Backend Developer"]
    )

    experience = st.selectbox(
        "Experience Level",
        ["Beginner","Intermediate","Advanced"]
    )

    if st.button("Start Interview 🚀"):

        st.session_state.session = InterviewSession(role)

        question = st.session_state.session.get_next_question()

        st.session_state.current_question = question

        st.success(f"Starting {role} interview for {experience} level!")

    # DISPLAY QUESTION
    if st.session_state.current_question:

        question_data = st.session_state.current_question

        st.subheader("Question")
        st.write(question_data["question"])

        user_answer = st.text_area("Enter your answer")

        if st.button("Submit Answer"):

            result = st.session_state.session.evaluate_answer(user_answer, question_data)

            st.session_state.score = result["score"]

            st.write("✅ Matched Keywords:", result["matched"])
            st.write("❌ Missing Keywords:", result["missed"])

            # next question
            next_q = st.session_state.session.get_next_question()
            st.session_state.current_question = next_q

    # SHOW SCORE
    if st.session_state.score is not None:
        st.metric("Answer Score", f"{st.session_state.score}%")

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

elif selected == "Dashboard":

    st.title("📊 Performance Dashboard")

    if st.session_state.session is None:
        st.warning("Start an interview first!")
    
    else:
        topic_scores = st.session_state.session.get_topic_wise_scores()

        st.subheader("📊 Topic-wise Performance")
        st.write(topic_scores)

        strengths, weaknesses = st.session_state.session.get_strengths_and_weaknesses()

        st.subheader("💪 Strengths")
        st.write(strengths)

        st.subheader("⚠️ Weak Areas")
        st.write(weaknesses)

        # Radar Chart
        df = pd.DataFrame({
            "Topic": list(topic_scores.keys()),
            "Score": list(topic_scores.values())
        })

        fig = px.line_polar(
            df,
            r="Score",
            theta="Topic",
            line_close=True
        )

        st.plotly_chart(fig)

# --------------------------------------------------
# REPORTS
# --------------------------------------------------

elif selected == "Reports":

    st.title("📄 Interview Reports")

    report_list = [
        "Interview_DS_01.pdf",
        "Interview_ML_02.pdf",
        "Interview_Backend_03.pdf"
    ]

    for report in report_list:

        col1,col2 = st.columns([4,1])

        col1.write(report)

        col2.download_button(
            "Download",
            data="Sample Report",
            file_name=report
        )
