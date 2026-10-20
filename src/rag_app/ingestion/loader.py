from __future__ import annotations

from pathlib import Path

from .text_cleaner import clean_text


SUPPORTED_SUFFIXES = {".pdf", ".txt", ".md", ".markdown"}


class DocumentLoader:
    @staticmethod
    def extract_text(file_path: str | Path) -> tuple[str, list[dict]]:
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return DocumentLoader._extract_pdf(path)
        if suffix in {".txt", ".md", ".markdown"}:
            return DocumentLoader._extract_text_file(path)
        raise ValueError(f"Unsupported file type: {suffix}. Supported file types: PDF, TXT, MD, MARKDOWN")

    @staticmethod
    def _extract_pdf(path: Path) -> tuple[str, list[dict]]:
        try:
            import fitz
        except ImportError as exc:  # pragma: no cover - optional runtime dependency guard
            raise RuntimeError("PyMuPDF is required to read PDF files") from exc

        pages: list[dict] = []
        texts: list[str] = []
        with fitz.open(path) as doc:
            for page_number, page in enumerate(doc, start=1):
                cleaned = clean_text(page.get_text("text"))
                texts.append(cleaned)
                pages.append({"page_number": page_number, "text": cleaned})
        return "\n\n".join(text for text in texts if text), pages

    @staticmethod
    def _extract_text_file(path: Path) -> tuple[str, list[dict]]:
        text = clean_text(path.read_text(encoding="utf-8", errors="replace"))
        return text, [{"page_number": None, "text": text}]
