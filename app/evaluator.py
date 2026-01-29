from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.text_preprocessing import clean_text
import pandas as pd
from pathlib import Path

def compute_similarity(user_answer: str, ideal_answer: str) -> float:
    """
    Computes TF-IDF cosine similarity between user answer and ideal answer.
    """
    # Clean texts
    user_clean = clean_text(user_answer)
    ideal_clean = clean_text(ideal_answer)

    # Vectorize
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([user_clean, ideal_clean])

    # Compute cosine similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return float(similarity[0][0])

def evaluate_answer(similarity_score: float) -> dict:
    """
    Maps similarity score to qualitative feedback.
    """
    if similarity_score >= 0.65:
        return {
            "label": "Good",
            "feedback": "Your answer covers most of the important concepts clearly."
        }
    elif similarity_score >= 0.40:
        return {
            "label": "Average",
            "feedback": "Your answer shows partial understanding but misses some key points."
        }
    else:
        return {
            "label": "Needs Improvement",
            "feedback": "Your answer lacks key concepts and needs further improvement."
        }


# Load dataset once
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "questions.csv"

df_questions = pd.read_csv(DATA_PATH)


def evaluate_response(question_id: str, user_answer: str) -> dict:
    """
    Evaluates a user's answer for a given question ID.
    """
    # Fetch ideal answer
    row = df_questions[df_questions["question_id"] == question_id]

    if row.empty:
        return {"error": "Invalid question ID"}

    ideal_answer = row.iloc[0]["ideal_answer"]

    # Compute similarity
    similarity = compute_similarity(user_answer, ideal_answer)

    # Generate feedback
    evaluation = evaluate_answer(similarity)

    return {
        "question_id": question_id,
        "similarity_score": round(similarity, 3),
        "label": evaluation["label"],
        "feedback": evaluation["feedback"]
    }

def run_evaluation(question_id: str, user_answer: str) -> dict:
    """
    Entry-point function for session manager / UI.
    """
    return evaluate_response(question_id, user_answer)
