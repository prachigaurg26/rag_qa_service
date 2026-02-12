from typing import List, Dict


def generate_answer(question: str, contexts: List[Dict]) -> str:
    """
    Generate an answer grounded strictly in retrieved context.
    """

    if not contexts:
        return "I don't know"

    context_text = "\n".join(c.get("text", "") for c in contexts)

    if not context_text.strip():
        return "I don't know"

    # Strict grounding: answer must come from context only
    return contexts[0].get("text", "I don't know")