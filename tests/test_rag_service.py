from unittest.mock import MagicMock

from src.rag_app.services.rag_service import RAGService


def test_rag_service_ingest_file_uses_vector_store(tmp_path):
    path = tmp_path / "notes.txt"
    path.write_text("System design is important for the app.", encoding="utf-8")
    store = MagicMock()
    service = RAGService(vector_store=store)
    doc_id, chunk_count = service.ingest_file(path)
    assert doc_id.startswith("notes-")
    assert len(doc_id.split("-", 1)[1]) == 12
    assert chunk_count >= 1
    store.add_documents.assert_called_once()


def test_rag_service_returns_fallback_without_calling_llm():
    store = MagicMock()
    store.similarity_search.return_value = []
    llm = MagicMock()
    service = RAGService(vector_store=store, llm_service=llm)
    answer, sources = service.ask_question("Question not covered by documents")
    assert "could not find relevant information" in answer.lower()
    assert sources == []
    llm.generate.assert_not_called()
