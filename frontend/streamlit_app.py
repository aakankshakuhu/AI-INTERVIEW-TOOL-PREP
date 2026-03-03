import streamlit as st
import sys
from pathlib import Path
import plotly.graph_objects as go

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
defaults = {
    "started": False,
    "question_index": 0,
    "session": None,
    "finished": False,
    "last_result": None,
    "report": None,
    "feedback": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -------------------------
# Restart Button (Always Visible After Start)
# -------------------------
def reset_interview():
    for key in defaults:
        st.session_state[key] = defaults[key]

if st.session_state.started:
    st.sidebar.button("🔄 Restart Interview", on_click=reset_interview)


# -------------------------
# Role Selection
# -------------------------
if not st.session_state.started:
    role = st.selectbox("Select Role", ["Data Scientist"])

    if st.button("Start Interview"):
        st.session_state.session = InterviewSession(role=role)
        st.session_state.started = True


# -------------------------
# Interview Flow
# -------------------------
if st.session_state.started and not st.session_state.finished:

    session = st.session_state.session
    idx = st.session_state.question_index
    total_questions = len(session.questions)

    current = idx + 1
    st.progress(min(current / total_questions, 1.0))
    st.caption(f"Question {current} of {total_questions}")

    question = session.get_question(idx)

    if question:
        st.subheader(f"Question {current}")
        st.write(question["question_text"])

        user_answer = st.text_area("Your Answer", height=150)

        submit_disabled = len(user_answer.strip()) < 15

        if st.button("Submit Answer", disabled=submit_disabled):

            result = session.submit_answer(
                question_id=question["question_id"],
                topic=question["topic"],
                user_answer=user_answer
            )

            st.session_state.last_result = result

        # Show result if available
        if st.session_state.last_result:

            result = st.session_state.last_result
            col1, col2 = st.columns([1, 2])

            with col1:
                st.metric("Similarity Score", round(result["similarity_score"], 3))

            with col2:
                score = result["similarity_score"]

                if score >= 0.65:
                    st.success(result["feedback"])
                elif score >= 0.40:
                    st.warning(result["feedback"])
                else:
                    st.error(result["feedback"])

            if st.button("Next Question"):
                st.session_state.question_index += 1
                st.session_state.last_result = None
                st.rerun()

    else:
        st.session_state.finished = True


# -------------------------
# Final Dashboard
# -------------------------
if st.session_state.started and st.session_state.finished:

    st.header("📊 Interview Summary")

    responses = st.session_state.session.get_all_responses()

    analyzer = PerformanceAnalyzer(responses, role="Data Scientist")
    report = analyzer.generate_report()

    feedback_generator = FeedbackGenerator(report)
    feedback = feedback_generator.generate_feedback()

    st.session_state.report = report
    st.session_state.feedback = feedback

    # -------- Score Gauge --------
    st.subheader("Overall Performance")

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=report["overall_score"],
        title={'text': "Overall Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'thickness': 0.4},
        }
    ))

    st.plotly_chart(gauge, use_container_width=True)

    # -------- Radar Chart --------
    st.subheader("Topic-wise Radar Analysis")

    topics = list(report["topic_scores"].keys())
    scores = list(report["topic_scores"].values())

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(
        r=scores,
        theta=topics,
        fill='toself'
    ))

    radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=False
    )

    st.plotly_chart(radar, use_container_width=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Confidence Score", report["confidence_score"])

    with col2:
        st.metric("Readiness Level", feedback["readiness"]["level"])

    st.divider()

    st.subheader("🛠 Improvement Plan")
    st.write(feedback["improvement_plan"])

    st.divider()

    # PDF Download
    if st.button("Generate PDF Report"):
        pdf_path = export_report_pdf(report, feedback)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Download Report",
                data=f,
                file_name="interview_report.pdf",
                mime="application/pdf"
            )