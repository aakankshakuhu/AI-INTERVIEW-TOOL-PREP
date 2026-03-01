from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.text_preprocessing import clean_text
import pandas as pd
from pathlib import Path
import math

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

    topic = row.iloc[0]["topic"]
    ideal_answer = row.iloc[0]["ideal_answer"]

    # Compute similarity
    similarity = compute_similarity(user_answer, ideal_answer)

    # Generate feedback
    evaluation = evaluate_answer(similarity)

    return {
        "question_id": question_id,
        "topic": topic,
        "similarity_score": round(similarity, 3),
        "label": evaluation["label"],
        "feedback": evaluation["feedback"]
    }

def run_evaluation(question_id: str, user_answer: str) -> dict:
    return evaluate_response(question_id, user_answer)

class PerformanceAnalyzer:
    def __init__(self, evaluation_results, role="Data Scientist"):
        self.evaluation_results = evaluation_results
        self.role = role

    def topic_wise_scores(self):
        topic_scores = {}

        for result in self.evaluation_results:
            topic = result["topic"]
            score = result["similarity_score"]

            if topic not in topic_scores:
                topic_scores[topic] = []

            topic_scores[topic].append(score)

        for topic in topic_scores:
            avg_score = sum(topic_scores[topic]) / len(topic_scores[topic])
            topic_scores[topic] = round(avg_score * 100, 2)

        return topic_scores

    def classify_topics(self, topic_scores):
        strengths = []
        weaknesses = []
        average = []

        for topic, score in topic_scores.items():
            if score >= 75:
                strengths.append(topic)
            elif score >= 50:
                average.append(topic)
            else:
                weaknesses.append(topic)

        return {
            "strong": strengths,
            "average": average,
            "weak": weaknesses
        }

    def overall_score(self, topic_scores):
        if not topic_scores:
            return 0

        weights = self.TOPIC_WEIGHTS.get(self.role, {})

        total_weighted_score = 0
        total_weights = 0

        for topic, score in topic_scores.items():
            weight = weights.get(topic, 1)  # default weight = 1
            total_weighted_score += score * weight
            total_weights += weight

        if total_weights == 0:
            return 0

        return round(total_weighted_score / total_weights, 2)


    def confidence_score(self, topic_scores):
        scores = list(topic_scores.values())

        if len(scores) <= 1:
            return 100.0  # single topic → fully stable

        mean = sum(scores) / len(scores)

        variance = sum((x - mean) ** 2 for x in scores) / len(scores)
        std_dev = math.sqrt(variance)

        # Normalize confidence (cap effect)
        confidence = max(0, 100 - std_dev)

        return round(confidence, 2)
    
    def generate_report(self):
        topic_scores = self.topic_wise_scores()
        classification = self.classify_topics(topic_scores)
        overall = self.overall_score(topic_scores)
        confidence = self.confidence_score(topic_scores)
        adjusted_confidence = round(confidence * (overall / 100), 2)

        return {
            "overall_score": overall,
            "topic_scores": topic_scores,
            "classification": classification,
            "confidence_score": adjusted_confidence
        }
    
    TOPIC_WEIGHTS = {
    "Data Scientist": {
        "Machine Learning": 3,
        "Python / Data Handling": 2,
        "SQL": 2,
        "System Design Basics": 1,
        "Operating Systems": 1
    }
}


