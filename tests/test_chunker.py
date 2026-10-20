import pytest

from src.rag_app.ingestion.chunker import Chunker


def test_chunker_creates_overlapping_chunks():
    text = "This is a sample document with multiple sentences that should be chunked into smaller text blocks. " * 4
    chunks = Chunker(chunk_size=80, chunk_overlap=20).chunk(
        text=text,
        document_id="doc-1",
        filename="sample.txt",
        pages=[{"page_number": 1, "text": text}],
    )
    assert len(chunks) > 1
    assert all(chunk.text for chunk in chunks)
    assert chunks[0].document_id == "doc-1"
    assert chunks[0].filename == "sample.txt"
    assert chunks[0].page_number == 1


def test_chunker_rejects_invalid_overlap():
    with pytest.raises(ValueError, match="smaller than chunk_size"):
        Chunker(chunk_size=50, chunk_overlap=50)


def test_chunker_returns_no_chunks_for_blank_text():
    assert Chunker(chunk_size=100, chunk_overlap=10).chunk("  ", "doc", "a.txt") == []
