class FeedbackGenerator:
    def __init__(self, report: dict):
        self.report = report

    def overall_feedback(self):
        score = self.report["overall_score"]

        if score >= 75:
            return "Excellent overall performance. You demonstrate strong conceptual understanding across most topics."
        elif score >= 50:
            return "Decent performance, but there are noticeable gaps in certain topics that need improvement."
        else:
            return "Your performance indicates significant conceptual gaps. Focused revision and practice are required."

    def topic_feedback(self):
        feedback = {}

        for topic, score in self.report["topic_scores"].items():
            if score >= 75:
                feedback[topic] = (
                    "Strong understanding. You are comfortable with core concepts and practical usage."
                )
            elif score >= 50:
                feedback[topic] = (
                    "Average understanding. Revise fundamentals and practice applying concepts."
                )
            else:
                feedback[topic] = (
                    "Weak understanding. Focus on core concepts, examples, and common interview questions."
                )

        return feedback

    def improvement_plan(self):
        weak_topics = self.report["classification"]["weak"]

        if not weak_topics:
            return "Maintain consistency and continue practicing advanced problems."

        plan = "Recommended improvement plan:\n"
        for topic in weak_topics:
            plan += f"- Strengthen fundamentals in {topic}\n"

        return plan

    def generate_feedback(self):
        return {
            "overall_feedback": self.overall_feedback(),
            "topic_feedback": self.topic_feedback(),
            "improvement_plan": self.improvement_plan()
        }
