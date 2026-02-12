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

    
    RESOURCE_LIBRARY = {
        "SQL": {
            "focus": "Aggregation, window functions, indexing, query optimization",
            "practice": "Solve advanced GROUP BY and ranking problems",
            "tools": "Practice on LeetCode SQL section or Mode Analytics"
        },
        "Machine Learning": {
            "focus": "Bias-variance tradeoff, overfitting, regularization, cross-validation",
            "practice": "Explain models conceptually before implementation",
            "tools": "Revise sklearn implementations and experiment with hyperparameters"
        },
        "Python / Data Handling": {
            "focus": "Pandas optimization, vectorization, memory management",
            "practice": "Work with large datasets and profile execution time",
            "tools": "Practice NumPy broadcasting and Pandas groupby operations"
        },
        "System Design Basics": {
            "focus": "High-level architecture, scalability, data pipelines",
            "practice": "Draw system diagrams for simple problems",
            "tools": "Study basic components like load balancers, queues, storage systems"
        },
        "Operating Systems": {
            "focus": "Process management, memory, scheduling",
            "practice": "Explain concepts like deadlock and paging",
            "tools": "Revise OS fundamentals and system-level trade-offs"
        }
    }

    def resource_recommendations(self):
        recommendations = {}
        weak_topics = self.report["classification"]["weak"]

        for topic in weak_topics:
            if topic in self.RESOURCE_LIBRARY:
                recommendations[topic] = self.RESOURCE_LIBRARY[topic]

        return recommendations
    
    
    def readiness_level(self):
        score = self.report["overall_score"]

        if score >= 75:
            return {
                "level": "Interview Ready",
                "description": "You are well-prepared for technical interviews and demonstrate strong topic mastery."
            }
        elif score >= 55:
            return {
                "level": "Moderately Prepared",
                "description": "You have decent understanding but should refine weak areas before appearing for interviews."
            }
        elif score >= 35:
            return {
                "level": "Beginner",
                "description": "Your fundamentals need strengthening before attempting competitive interviews."
            }
        else:
            return {
                "level": "Needs Foundation Work",
                "description": "Significant conceptual gaps detected. Focus on core fundamentals before progressing."
            }
    
    
    def confidence_feedback(self):
        confidence = self.report["confidence_score"]

        if confidence >= 75:
            return "Your performance is consistent across topics, indicating stable understanding."
        elif confidence >= 50:
            return "Your performance shows moderate variation across topics."
        else:
            return "Your performance is inconsistent across topics. Strengthen weak areas for stability."
        
    def generate_feedback(self):
        return {
            "overall_feedback": self.overall_feedback(),
            "topic_feedback": self.topic_feedback(),
            "improvement_plan": self.improvement_plan(),
            "resources": self.resource_recommendations(),
            "readiness": self.readiness_level(),
            "confidence_score": self.report["confidence_score"],
            "confidence_feedback": self.confidence_feedback()
        }







