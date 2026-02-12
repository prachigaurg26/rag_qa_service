from fastapi import APIRouter
from pydantic import BaseModel
import string

from app.services.retrieval import retrieve_context
from app.services.llm import generate_answer
from app.utils.safety import is_safe

router = APIRouter(prefix="/query", tags=["Query"])


class QueryRequest(BaseModel):
    question: str


# Stop words for relevance filtering
STOP_WORDS = {
    "is", "a", "an", "the", "what", "who", "when",
    "where", "why", "how", "of", "to", "for", "in"
}


@router.post("/")
def query_data(req: QueryRequest):

    # 🔒 SAFETY CHECK
    if not is_safe(req.question):
        return {
            "answer": "Query not allowed due to safety restrictions",
            "sources": [],
            "confidence": "blocked"
        }

    # 🔍 RETRIEVE CONTEXT
    results = retrieve_context(req.question)

    if not results:
        return {
            "answer": "I don't know",
            "sources": [],
            "confidence": "low"
        }

    # 🔑 Normalize question words
    question_words = {
        w for w in req.question.lower()
        .translate(str.maketrans("", "", string.punctuation))
        .split()
        if w not in STOP_WORDS
    }

    # 🔑 Check relevance across ALL retrieved chunks
    relevant = False

    for r in results:
        context_words = {
            w for w in r["text"].lower()
            .translate(str.maketrans("", "", string.punctuation))
            .split()
            if w not in STOP_WORDS
        }

        if len(question_words & context_words) > 0:
            relevant = True
            break

    if not relevant:
        return {
            "answer": "I don't know",
            "sources": [],
            "confidence": "low"
        }

    # 🤖 GENERATE ANSWER (grounded)
    answer = generate_answer(req.question, results)

    return {
        "answer": answer,
        "sources": [
            {
                "source": r.get("source", "unknown"),
                "preview": r.get("text", "")
            }
            for r in results
        ],
        "confidence": "grounded"
    }