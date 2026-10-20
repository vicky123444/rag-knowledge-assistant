from __future__ import annotations

import hashlib
from pathlib import Path

from src.rag_app.config import settings
from src.rag_app.generation.llm_service import LLMService
from src.rag_app.generation.prompt_builder import PromptBuilder
from src.rag_app.ingestion.chunker import Chunker
from src.rag_app.ingestion.loader import DocumentLoader
from src.rag_app.retrieval.retriever import Retriever
from src.rag_app.vectorstore.chroma_store import ChromaVectorStore


class RAGService:
    def __init__(self, vector_store=None, llm_service: LLMService | None = None):
        self.vector_store = vector_store if vector_store is not None else ChromaVectorStore()
        self.llm_service = llm_service if llm_service is not None else LLMService()
        self.chunker = Chunker(settings.chunk_size, settings.chunk_overlap)
        self.retriever = Retriever(self.vector_store)

    def ingest_file(self, file_path: str | Path) -> tuple[str, int]:
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Document not found: {path}")
        text, pages = DocumentLoader.extract_text(path)
        if not text.strip():
            raise ValueError("No extractable text found. Scanned PDFs may require OCR.")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()[:12]
        document_id = f"{path.stem[:60]}-{digest}"
        chunks = self.chunker.chunk(text, document_id, path.name, pages)
        documents = [{
            "id": chunk.chunk_id,
            "text": chunk.text,
            "document_id": chunk.document_id,
            "filename": chunk.filename,
            "page_number": chunk.page_number,
            "chunk_id": chunk.chunk_id,
            "source_index": chunk.source_index,
        } for chunk in chunks]
        self.vector_store.add_documents(documents)
        return document_id, len(chunks)

    def ask_question(self, question: str, top_k: int = 4) -> tuple[str, list[dict]]:
        context = self.retriever.retrieve(question, top_k=top_k)
        if not context:
            return (
                "I could not find relevant information in the indexed documents to answer this question. "
                "Try uploading a document covering the topic or rephrasing the question.",
                [],
            )
        prompt = PromptBuilder.build_prompt(question, context)
        return self.llm_service.generate(prompt), context
