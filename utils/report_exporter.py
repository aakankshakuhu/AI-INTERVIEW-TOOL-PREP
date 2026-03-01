import json
from pathlib import Path
import matplotlib.pyplot as plt

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch


# ---------- CHART GENERATION ----------

def generate_topic_bar_chart(topic_scores, output_path):
    plt.figure()
    topics = list(topic_scores.keys())
    scores = list(topic_scores.values())

    plt.bar(topics, scores)
    plt.title("Topic-wise Performance")
    plt.xlabel("Topics")
    plt.ylabel("Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def generate_score_pie_chart(topic_scores, output_path):
    plt.figure()
    plt.pie(
        topic_scores.values(),
        labels=topic_scores.keys(),
        autopct="%1.1f%%"
    )
    plt.title("Score Distribution")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


# ---------- JSON EXPORT ----------

def export_report_json(report, feedback, output_dir="outputs"):
    Path(output_dir).mkdir(exist_ok=True)

    path = Path(output_dir) / "interview_report.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            {"report": report, "feedback": feedback},
            f,
            indent=4
        )
    return path


# ---------- PROFESSIONAL PDF EXPORT ----------

def export_report_pdf(report, feedback, output_dir="outputs"):
    Path(output_dir).mkdir(exist_ok=True)

    bar_chart = Path(output_dir) / "topic_scores.png"
    pie_chart = Path(output_dir) / "score_distribution.png"

    generate_topic_bar_chart(report["topic_scores"], bar_chart)
    generate_score_pie_chart(report["topic_scores"], pie_chart)

    pdf_path = Path(output_dir) / "interview_report.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    elements = []

    # ---------- TITLE ----------
    elements.append(Paragraph("AI Interview Performance Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    # ---------- SUMMARY ----------
    elements.append(Paragraph(
        f"<b>Overall Score:</b> {report['overall_score']}", styles["Normal"]
    ))
    elements.append(Paragraph(
        f"<b>Confidence Score:</b> {report['confidence_score']}", styles["Normal"]
    ))
    elements.append(Paragraph(
        f"<b>Readiness Level:</b> {feedback['readiness']['level']}", styles["Normal"]
    ))
    elements.append(Spacer(1, 0.3 * inch))

    # ---------- TABLE ----------
    table_data = [["Topic", "Score"]]
    for topic, score in report["topic_scores"].items():
        table_data.append([topic, str(score)])

    table = Table(table_data, colWidths=[4 * inch, 1.5 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))

    elements.append(Paragraph("Topic-wise Scores", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(table)
    elements.append(Spacer(1, 0.4 * inch))

    # ---------- CHARTS ----------
    elements.append(Paragraph("Performance Visualization", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Image(str(bar_chart), width=4.5 * inch, height=3 * inch))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Image(str(pie_chart), width=4.5 * inch, height=3 * inch))
    elements.append(Spacer(1, 0.4 * inch))

    # ---------- FEEDBACK ----------
    elements.append(Paragraph("Overall Feedback", styles["Heading2"]))
    elements.append(Paragraph(feedback["overall_feedback"], styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("Improvement Plan", styles["Heading2"]))
    for line in feedback["improvement_plan"].split("\n"):
        elements.append(Paragraph(line, styles["Normal"]))

    doc.build(elements)

    return pdf_path