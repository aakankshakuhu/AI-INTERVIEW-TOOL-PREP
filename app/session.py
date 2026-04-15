import pandas as pd
import random

# Import evaluator functions
from app.evaluator import evaluate_answer


def parse_keywords(keyword_str):
    if not isinstance(keyword_str, str):
        return []
    return [k.strip().lower() for k in keyword_str.split(",")]


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
                "input_type": question_data["input_type"],
                "keywords": question_data.get("keywords", "")
            }

        return None

    def evaluate_answer(self, user_answer, question_data):

        ideal_answer = question_data["ideal_answer"]
        topic = question_data["topic"]
        keywords = parse_keywords(question_data.get("keywords", ""))

        # 🔥 call evaluator (HYBRID)
        result = evaluate_answer(user_answer, ideal_answer, keywords)

        score = result["score"]
        matched = result["matched"]
        missed = result["missed"]

        # 🔥 store response
        self.responses.append({
            "question": question_data["question"],
            "topic": topic,
            "score": score,
            "matched": matched,
            "missed": missed
        })

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
    
