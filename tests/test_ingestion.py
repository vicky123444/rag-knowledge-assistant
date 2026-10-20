from pathlib import Path

import pytest

from src.rag_app.ingestion.loader import DocumentLoader


def test_txt_loader_extracts_text(tmp_path: Path):
    sample = tmp_path / "sample.txt"
    sample.write_text("Alpha beta gamma\n\nThis is a test.", encoding="utf-8")
    text, pages = DocumentLoader.extract_text(sample)
    assert "Alpha beta gamma" in text
    assert pages[0]["page_number"] is None


def test_loader_rejects_unsupported_extensions(tmp_path: Path):
    sample = tmp_path / "sample.exe"
    sample.write_text("not a document", encoding="utf-8")
    with pytest.raises(ValueError, match="Supported file types"):
        DocumentLoader.extract_text(sample)
