from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Chunk:
    chunk_id: str
    text: str
    document_id: str
    filename: str
    page_number: int | None = None
    source_index: int = 0


class Chunker:
    """Split source text into overlapping character windows."""

    def __init__(self, chunk_size: int, chunk_overlap: int):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero")
        if chunk_overlap < 0:
            raise ValueError("chunk_overlap must be non-negative")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str, document_id: str, filename: str, pages: list[dict] | None = None) -> list[Chunk]:
        if not text or not text.strip():
            return []
        segments = []
        if pages:
            for index, page in enumerate(pages):
                page_text = str(page.get("text", "")).strip()
                if page_text:
                    segments.append((page_text, page.get("page_number"), index))
        if not segments:
            segments = [(text.strip(), None, 0)]

        result = []
        step = self.chunk_size - self.chunk_overlap
        for segment, page_number, source_index in segments:
            if len(segment) <= self.chunk_size:
                parts = [segment]
            else:
                parts = []
                start = 0
                while start < len(segment):
                    end = min(start + self.chunk_size, len(segment))
                    part = segment[start:end].strip()
                    if part:
                        parts.append(part)
                    if end == len(segment):
                        break
                    start += step
            for index, part in enumerate(parts):
                result.append(Chunk(
                    chunk_id=f"{document_id}:{source_index}:{index}",
                    text=part,
                    document_id=document_id,
                    filename=filename,
                    page_number=page_number,
                    source_index=source_index,
                ))
        return result
