import streamlit as st
import sys
from pathlib import Path

# Allow importing from project root
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.session import InterviewSession
from app.evaluator import PerformanceAnalyzer
from app.feedback import FeedbackGenerator
from utils.report_exporter import export_report_pdf

st.set_page_config(page_title="AI Interview Simulator", layout="wide")

st.title("🤖 AI Interview Simulation Platform")

# -------------------------
# Initialize Session State
# -------------------------
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.question_index = 0
    st.session_state.session = None
    st.session_state.finished = False
    st.session_state.report = None
    st.session_state.feedback = None

# -------------------------
# Role Selection
# -------------------------
if not st.session_state.started:
    role = st.selectbox("Select Role", ["Data Scientist"])

    if st.button("Start Interview"):
        st.session_state.session = InterviewSession(role=role)
        st.session_state.started = True
        st.session_state.question_index = 0
        st.session_state.finished = False

# -------------------------
# Interview Flow
# -------------------------
if st.session_state.started and not st.session_state.finished:

    session = st.session_state.session
    idx = st.session_state.question_index

    question = session.get_question(idx)

    if question:
        st.subheader(f"Question {idx + 1}")
        st.write(question["question_text"])

        user_answer = st.text_area("Your Answer", height=150)

        if st.button("Submit Answer"):
            result = session.submit_answer(
                question_id=question["question_id"],
                topic=question["topic"],
                user_answer=user_answer
            )

            st.success(f"Score: {result['similarity_score']}")
            st.info(result["feedback"])

            st.session_state.question_index += 1

    else:
        st.session_state.finished = True

# -------------------------
# Final Report
# -------------------------
if st.session_state.finished:

    st.header("📊 Interview Summary")

    responses = st.session_state.session.get_all_responses()

    analyzer = PerformanceAnalyzer(responses, role="Data Scientist")
    report = analyzer.generate_report()

    feedback_generator = FeedbackGenerator(report)
    feedback = feedback_generator.generate_feedback()

    st.metric("Overall Score", report["overall_score"])
    st.metric("Confidence Score", report["confidence_score"])
    st.metric("Readiness Level", feedback["readiness"]["level"])

    st.subheader("Topic-wise Scores")
    st.bar_chart(report["topic_scores"])

    st.subheader("Improvement Plan")
    st.write(feedback["improvement_plan"])

    # Export PDF
    if st.button("Generate PDF Report"):
        path = export_report_pdf(report, feedback)
        st.success(f"Report saved at: {path}")