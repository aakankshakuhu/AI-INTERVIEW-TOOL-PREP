from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.session import InterviewSession

app = FastAPI()

# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve static files (JS, CSS)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# ✅ Serve frontend (index.html)
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")


# ---------------- SESSION LOGIC ---------------- #

sessions = {}

@app.post("/start-session")
def start_session(role: str):
    session = InterviewSession(role)
    session_id = str(id(session))
    sessions[session_id] = session
    return {"session_id": session_id}


@app.get("/next-question")
def next_question(session_id: str):
    session = sessions.get(session_id)
    if not session:
        return {"error": "Invalid session_id"}
    return session.get_next_question()


@app.post("/submit-answer")
def submit_answer(data: dict):
    session = sessions.get(data["session_id"])
    if not session:
        return {"error": "Invalid session_id"}

    return session.evaluate_answer(
        data["user_answer"],
        data["question_data"]
    )


@app.get("/get-results")
def get_results(session_id: str):
    session = sessions.get(session_id)
    if not session:
        return {"error": "Invalid session_id"}

    strengths, weaknesses = session.get_strengths_and_weaknesses()

    return {
        "topic_scores": session.get_topic_wise_scores(),
        "strengths": strengths,
        "weaknesses": weaknesses
    }