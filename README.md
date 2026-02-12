RAG QA Service

This repository contains a simple Retrieval Augmented Generation (RAG) based Question Answering service built using FastAPI.
The goal of this project is to demonstrate how stored knowledge can be ingested, retrieved, and used to answer user questions in a grounded and safe manner.

The system strictly avoids hallucination and returns a safe fallback when relevant data is not available.

Problem Statement

The objective of this task is to design and build a backend service that can accept knowledge input, store it in a searchable memory system, and answer user questions using only the stored knowledge. The system must also indicate which sources were used to generate the answer and must not guess when data is missing.

Architecture Decisions

The system is designed using a modular architecture to keep responsibilities clearly separated.

The FastAPI framework is used to expose REST APIs for ingestion and querying. FastAPI was chosen for its simplicity, performance, and built-in support for request validation and API documentation.

Knowledge ingestion is handled by a dedicated API that accepts text input. The text is split into manageable chunks and converted into vector embeddings. These embeddings are stored in an in-memory vector store along with metadata such as the source of the content.

For retrieval, the query is embedded using the same embedding mechanism and compared against stored embeddings using vector similarity search. FAISS is used as the vector store due to its efficiency and simplicity.

Answer generation is intentionally kept simple. Instead of generating new text, the system returns content directly from retrieved knowledge. This ensures answers are always grounded in stored data.

A safety layer is included to block unsafe queries and prevent misuse.

Knowledge Ingestion Flow

The ingestion API accepts raw text along with a source identifier.
The text is split into chunks, embedded, and stored in the vector store along with metadata.
This allows the system to retrieve relevant information later while maintaining traceability to the original source.

Question Answering Flow

When a user submits a question, the system first performs a safety check.
If the query is allowed, the question is embedded and compared against stored embeddings.

Multiple relevant chunks are retrieved.
A relevance check ensures that the retrieved content shares meaningful terms with the user query.
If no relevant content is found, the system safely responds with "I don't know".

If relevant content exists, the system returns an answer derived strictly from the stored knowledge along with source references.

Example API Calls
Ingest Knowledge

Endpoint
POST /ingest/ingest/

Request body
{
"text": "Python is a programming language. It is widely used for data science and web development.",
"source": "python_docs"
}

Query Knowledge

Endpoint
POST /query/query/

Request body
{
"question": "What is Python?"
}

Expected behavior
The system returns a grounded answer based on the ingested Python knowledge along with the source reference.

Safety and Hallucination Prevention

The system never generates information that does not exist in the stored knowledge base.
If relevant information cannot be found, it explicitly returns "I don't know".

Unsafe queries related to hacking, malware, or illegal activities are blocked before retrieval is performed.

This design ensures that the system is safe, predictable, and aligned with responsible AI practices.

Tradeoffs

The vector store is kept in memory to keep the system simple and easy to evaluate. This means the data is not persistent across restarts.

Dummy deterministic embeddings are used instead of real language model embeddings. This simplifies setup and avoids external dependencies but results in approximate similarity ranking.

The answer generation logic is intentionally minimal to prioritize correctness and grounding over fluency.

Scaling Considerations

In a production environment, the in-memory vector store can be replaced with a persistent vector database such as Pinecone or Weaviate.

Real embedding models can be introduced to improve retrieval quality without changing the overall architecture.

The ingestion pipeline can be extended to support file uploads and URL-based ingestion.

For multi-user scenarios, user-level isolation can be implemented by tagging stored data with user identifiers.

Asynchronous processing, caching, and horizontal scaling of the API layer can be added to handle higher load.

How to Run the Project

Install dependencies using the requirements file and start the FastAPI server using Uvicorn.
The API documentation is available through the built-in Swagger UI.

Summary

This project demonstrates a clear and practical implementation of a RAG-based question answering system.
It satisfies all functional requirements of the assessment, including knowledge ingestion, grounded answering, source attribution, and safety handling.

The design prioritizes correctness, simplicity, and explainability while remaining extensible for future improvements.
