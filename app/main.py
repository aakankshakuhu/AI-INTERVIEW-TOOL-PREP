import pandas as pd

df = pd.read_csv("data/questions.csv")

print(df)

from app.evaluator import evaluate_response

result = evaluate_response(
    question_id="Q5",
    user_answer="Overfitting happens when a model memorizes training data and fails on new data"
)

print(result)

from app.session import InterviewSession

session = InterviewSession(role="Data Scientist")

for i in range(3):
    q = session.get_question(i)
    print("\nQuestion:", q["question_text"])

    result = session.submit_answer(
        question_id=q["question_id"],
        topic=q["topic"],
        user_answer="This is a sample answer for testing"
    )

    print("Evaluation:", result)

print("\nAll responses stored:")
print(session.get_all_responses())

from app.evaluator import PerformanceAnalyzer

evaluation_results = session.get_all_responses()

analyzer = PerformanceAnalyzer(evaluation_results)
report = analyzer.generate_report()

print("\nInterview Performance Summary")
print("-----------------------------")
print("Overall Score:", report["overall_score"])
print("Topic-wise Scores:", report["topic_scores"])
print("Strengths:", report["classification"]["strong"])
print("Weak Topics:", report["classification"]["weak"])




