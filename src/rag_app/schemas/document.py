from pydantic import BaseModel


class DocumentIngestResponse(BaseModel):
    status: str
    message: str
    filename: str
    document_id: str
    chunk_count: int


class SourceReference(BaseModel):
    document: str
    page: int | None = None
    excerpt: str
