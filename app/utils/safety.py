# app/utils/safety.py

def is_safe(question: str) -> bool:
    """
    Basic safety filter for user queries.
    Blocks obviously harmful or irrelevant queries.
    """

    if not question or not question.strip():
        return False

    blocked_keywords = [
        "hack",
        "attack",
        "illegal",
        "malware",
        "exploit",
        "virus"
    ]

    q = question.lower()

    for word in blocked_keywords:
        if word in q:
            return False

    return True