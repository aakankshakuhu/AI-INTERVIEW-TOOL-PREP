from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.text_preprocessing import clean_text
import math


# ------------------ SIMILARITY ------------------ #
def compute_similarity(user_answer: str, ideal_answer: str) -> float:
    user_clean = clean_text(user_answer)
    ideal_clean = clean_text(ideal_answer)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([user_clean, ideal_clean])

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return float(similarity[0][0])  # 0–1


# ------------------ KEYWORD LOGIC (IMPROVED) ------------------ #

def normalize(text):
    return (
        text.lower()
        .replace(" ", "")
        .replace("s", "")
        .replace("ing", "")
    )


def keyword_match_score(user_answer, keywords):
    if not keywords:
        return 0

    user_norm = normalize(user_answer)

    matched = sum(
        1 for word in keywords if normalize(word) in user_norm or user_norm in normalize(word)
    )

    return (matched / len(keywords)) * 100


def keyword_match_details(user_answer, keywords):
    user_norm = normalize(user_answer)

    matched = []
    missed = []

    for word in keywords:
        if normalize(word) in user_norm:
            matched.append(word)
        else:
            missed.append(word)

    return matched, missed

def normalize(text):
    return text.lower().replace(" ", "").replace("s", "")


# ------------------ MAIN EVALUATION ------------------ #
def evaluate_answer(user_answer, ideal_answer, keywords):

    # TF-IDF similarity (0–1 → convert to %)
    if ideal_answer and ideal_answer != "TO_BE_ADDED":
        similarity = compute_similarity(user_answer, ideal_answer) * 100
    else:
        similarity = 0

    # Keyword score (already %)
    keyword_score = keyword_match_score(user_answer, keywords)

    # Final weighted score
    final_score = max((0.4 * similarity) + (0.6 * keyword_score), keyword_score)

    # Keyword details
    matched, missed = keyword_match_details(user_answer, keywords)

    # Confidence (based on consistency of scoring signals)
    confidence = 100 - abs(similarity - keyword_score)
    confidence = max(50, min(confidence, 100))  # clamp


    if keyword_score >= 60:
        final_score = max(final_score, 60)


    # Balanced scoring
    base_score = (0.5 * similarity) + (0.5 * keyword_score)

    # Prevent collapse
    final_score = max(base_score, keyword_score)

    # Strong concept boost
    if keyword_score >= 60:
        final_score = max(final_score, 70)

    # Cap
    final_score = min(final_score, 100)

    # Feedback generation
    if final_score >= 70:
        feedback = "Good answer. Core concept is correct."
    elif final_score >= 50:
        feedback = "Partial understanding. Add more detail."
    else:
        feedback = "Weak answer. Missing key concepts."

    print("SIM:", similarity)
    print("KEY:", keyword_score)
    print("FINAL:", final_score)

    return {
        "score": round(final_score, 2),
        "confidence": round(confidence, 2),
        "keyword_match": round(keyword_score, 2),
        "matched_keywords": matched,
        "missing_keywords": missed,
        "feedback": feedback
    }
    