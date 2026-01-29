import re

def clean_text(text: str) -> str:
    """
    Cleans input text for NLP processing.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)  # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()  # normalize spaces

    return text
