import random
import pandas as pd
from pathlib import Path

from app.evaluator import run_evaluation


class InterviewSession:
    def __init__(self, role: str):
        self.role = role
        self.responses = []

        # Load dataset
        base_dir = Path(__file__).resolve().parent.parent
        data_path = base_dir / "data" / "questions.csv"
        self.df = pd.read_csv(data_path)

        # Filter questions by role
        self.questions = self.df[self.df["role"] == role].copy()

        if self.questions.empty:
            raise ValueError(f"No questions found for role: {role}")

        # Randomize question order
        self.questions = self.questions.sample(frac=1).reset_index(drop=True)

    def get_question(self, index: int) -> dict:
        """
        Returns question at a given index.
        """
        if index >= len(self.questions):
            return {}

        row = self.questions.iloc[index]
        return {
            "question_id": row["question_id"],
            "question_text": row["question_text"],
            "topic": row["topic"],
            "input_type": row["input_type"]
        }

    def submit_answer(self, question_id: str, topic: str, user_answer: str) -> dict:
        """
        Evaluates and stores the user's answer.
        """
        result = run_evaluation(question_id, user_answer)

        record = {
            "question_id": question_id,
            "topic": topic,
            "score": result["similarity_score"],
            "label": result["label"],
            "suggestion": result["feedback"]
        }

        self.responses.append(record)
        return record

    def get_all_responses(self):
        return self.responses
