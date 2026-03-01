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

analyzer = PerformanceAnalyzer(evaluation_results, role="Data Scientist")
report = analyzer.generate_report()

print("\nInterview Performance Summary")
print("-----------------------------")
print("Overall Score:", report["overall_score"])
print("Topic-wise Scores:", report["topic_scores"])
print("Strengths:", report["classification"]["strong"])
print("Weak Topics:", report["classification"]["weak"])


from app.feedback import FeedbackGenerator

feedback_gen = FeedbackGenerator(report)
feedback = feedback_gen.generate_feedback()

print("\nInterview Feedback")
print("------------------")
print("Overall:", feedback["overall_feedback"])

print("\nTopic-wise Feedback:")
for topic, fb in feedback["topic_feedback"].items():
    print(f"- {topic}: {fb}")

print("\nImprovement Plan:")
print(feedback["improvement_plan"])

print("\nRecommended Resources:")
for topic, details in feedback["resources"].items():
    print(f"\n{topic}:")
    print("  Focus Areas:", details["focus"])
    print("  Practice Strategy:", details["practice"])
    print("  Suggested Tools:", details["tools"])

print("\nReadiness Assessment")
print("--------------------")
print("Level:", feedback["readiness"]["level"])
print("Description:", feedback["readiness"]["description"])

print("\nConfidence Analysis")
print("-------------------")
print("Confidence Score:", feedback["confidence_score"])
print("Confidence Insight:", feedback["confidence_feedback"])







