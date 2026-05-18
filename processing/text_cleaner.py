import re


def clean_text(text):
    """
    Clean raw financial text for NLP processing.
    """

    if not text:
        return ""

    text = str(text).lower()

    # Remove URLs
    text = re.sub(
        r"http\S+",
        "",
        text
    )

    # Remove punctuation / symbols
    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        "",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text