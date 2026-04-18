import pandas as pd
import random

# Import evaluator functions
from app.evaluator import evaluate_answer


def parse_keywords(keywords):
    if not keywords:
        return []

    if isinstance(keywords, float):
        return []

    if isinstance(keywords, str):
        return [k.strip().lower() for k in keywords.split(",")]

    return keywords


class InterviewSession:

    def __init__(self, role):

        # load dataset
        df = pd.read_csv("data/questions.csv")

        # normalize column names
        df.columns = df.columns.str.strip().str.lower()

        # filter questions by role
        self.questions = df[df["role"] == role]

        # convert to list of dictionaries
        self.questions = self.questions.to_dict("records")

        # shuffle questions
        random.shuffle(self.questions)

        # tracking
        self.current_index = 0
        self.responses = []   # 🔥 store all responses

    def get_next_question(self):

        if self.current_index < len(self.questions):

            question_data = self.questions[self.current_index]
            self.current_index += 1

            return {
                "question": question_data["question_text"],
                "topic": question_data["topic"],
                "ideal_answer": question_data["ideal_answer"],
                "input_type": question_data.get("input_type", "text"),
                "keywords": question_data.get("keywords", "")
            }

        return None

    def evaluate_answer(self, user_answer, question_data):

        ideal_answer = question_data.get("ideal_answer")
        topic = question_data.get("topic")
        keywords = parse_keywords(question_data.get("keywords", ""))


        result = evaluate_answer(user_answer, ideal_answer, keywords)

        # ✅ extract correct fields
        score = result["score"]
        matched = result["matched_keywords"]
        missed = result["missing_keywords"]
        confidence = result["confidence"]

    
        self.responses.append({
            "question": question_data.get("question"),
            "topic": topic,
            "score": score,
            "confidence": confidence,
            "matched_keywords": matched,
            "missing_keywords": missed
        })

        print("KEYWORDS RAW:", question_data.get("keywords"))

        return result

    # 🔥 (PREP FOR TASK 19)
    def get_all_responses(self):
        return self.responses
    
    def get_topic_wise_scores(self):

        topic_scores = {}

        for response in self.responses:
            topic = response["topic"]
            score = response["score"]

            if topic not in topic_scores:
                topic_scores[topic] = []

            topic_scores[topic].append(score)

        # compute averages
        topic_avg = {}
        for topic, scores in topic_scores.items():
            topic_avg[topic] = round(sum(scores) / len(scores), 2)

        return topic_avg

    # ✅ FIXED: inside class
    def get_strengths_and_weaknesses(self):

        topic_scores = self.get_topic_wise_scores()

        strengths = []
        weaknesses = []

        for topic, score in topic_scores.items():
            if score >= 75:
                strengths.append(topic)
            elif score <= 60:
                weaknesses.append(topic)

        return strengths, weaknesses
    
    
    
