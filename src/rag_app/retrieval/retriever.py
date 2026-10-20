from __future__ import annotations

from src.rag_app.vectorstore.base import VectorStore


class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 4) -> list[dict]:
        return self.vector_store.similarity_search(query=query, k=top_k)
