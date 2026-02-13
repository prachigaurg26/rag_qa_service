from fastapi import APIRouter
from pydantic import BaseModel
import string

from app.services.retrieval import retrieve_context
from app.services.llm import generate_answer
from app.utils.safety import is_safe

router = APIRouter(prefix="/query", tags=["Query"])


class QueryRequest(BaseModel):
    question: str


STOP_WORDS = {
    "is", "a", "an", "the", "what", "who", "when",
    "where", "why", "how", "of", "to", "for", "in"
}


@router.post("/")
def query_data(req: QueryRequest):

    if not is_safe(req.question):
        return {
            "answer": "Query not allowed due to safety restrictions",
            "sources": [],
            "confidence": "blocked"
        }

    results = retrieve_context(req.question)

    if not results:
        return {
            "answer": "I don't know",
            "sources": [],
            "confidence": "low"
        }

    question_words = {
        w for w in req.question.lower()
        .translate(str.maketrans("", "", string.punctuation))
        .split()
        if w not in STOP_WORDS
    }

    relevant_results = []

    for r in results:
        context_words = {
            w for w in r["text"].lower()
            .translate(str.maketrans("", "", string.punctuation))
            .split()
            if w not in STOP_WORDS
        }

        if question_words & context_words:
            relevant_results.append(r)

    if not relevant_results:
        return {
            "answer": "I don't know",
            "sources": [],
            "confidence": "low"
        }

   
    relevant_results = relevant_results[:1]

    answer = generate_answer(req.question, relevant_results)

    return {
        "answer": answer,
        "sources": [
            {
                "source": r.get("source", "unknown"),
                "preview": r.get("text", "")
            }
            for r in relevant_results
        ],
        "confidence": "grounded"
    }