from __future__ import annotations

from pathlib import Path

from src.rag_app.config import settings
from src.rag_app.embeddings.embedding_service import EmbeddingService
from src.rag_app.vectorstore.base import VectorStore


class ChromaVectorStore(VectorStore):
    def __init__(
        self,
        persist_directory: str | None = None,
        embedding_service: EmbeddingService | None = None,
    ):
        try:
            import chromadb
        except ImportError as exc:  # pragma: no cover - runtime dependency guard
            raise RuntimeError("chromadb is required; install requirements.txt") from exc

        self.persist_directory = persist_directory or settings.chroma_persist_directory
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(name="document_chunks")
        self.embedding_service = embedding_service or EmbeddingService()

    def add_documents(self, documents: list[dict]) -> None:
        if not documents:
            return
        texts = [item["text"] for item in documents]
        embeddings = self.embedding_service.embed_documents(texts)
        ids = [item["id"] for item in documents]
        metadatas = []
        for item in documents:
            metadata = {
                "document_id": item.get("document_id"),
                "filename": item.get("filename"),
                "page_number": item.get("page_number"),
                "chunk_id": item.get("chunk_id"),
                "source_index": item.get("source_index"),
            }
            # Chroma metadata values must be scalar and non-null.
            metadatas.append({k: v for k, v in metadata.items() if v is not None})
        self.collection.upsert(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=texts)

    def similarity_search(self, query: str, k: int = 4) -> list[dict]:
        if k < 1:
            return []
        count = self.collection.count()
        if count == 0:
            return []
        query_embedding = self.embedding_service.embed_text(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(k, count),
            include=["documents", "metadatas", "distances"],
        )
        matches: list[dict] = []
        for index, result_id in enumerate(results.get("ids", [[]])[0]):
            metadata = (results.get("metadatas") or [[]])[0][index] or {}
            matches.append(
                {
                    "id": result_id,
                    "text": (results.get("documents") or [[]])[0][index],
                    "score": (results.get("distances") or [[]])[0][index],
                    "document_id": metadata.get("document_id"),
                    "filename": metadata.get("filename"),
                    "page_number": metadata.get("page_number"),
                    "chunk_id": metadata.get("chunk_id"),
                    "source_index": metadata.get("source_index"),
                }
            )
        return matches
