from pathlib import Path

from src.rag_app.ingestion.loader import SUPPORTED_SUFFIXES
from src.rag_app.services.rag_service import RAGService


def ingest_directory(directory: str | Path) -> None:
    base = Path(directory)
    if not base.is_dir():
        raise NotADirectoryError(f"Directory not found: {base}")
    service = RAGService()
    for path in sorted(base.iterdir()):
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            document_id, chunk_count = service.ingest_file(path)
            print(f"Indexed {path.name} as {document_id} ({chunk_count} chunks)")


if __name__ == "__main__":
    ingest_directory("data/sample_documents")
