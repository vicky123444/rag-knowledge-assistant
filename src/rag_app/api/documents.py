from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from src.rag_app.config import settings
from src.rag_app.ingestion.loader import SUPPORTED_SUFFIXES
from src.rag_app.schemas.document import DocumentIngestResponse
from src.rag_app.services.rag_service import get_rag_service

router = APIRouter()


@router.post("/documents/ingest", response_model=DocumentIngestResponse, tags=["documents"])
async def ingest_document(file: UploadFile = File(...)) -> DocumentIngestResponse:
    submitted_name = (file.filename or "upload").replace(chr(92), "/")
    filename = Path(submitted_name).name
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise HTTPException(status_code=400, detail="Supported file types: PDF, TXT, MD, MARKDOWN")

    content = await file.read(settings.max_upload_bytes + 1)
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")
    if len(content) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="File exceeds configured upload limit")

    temp_dir = Path("data/uploads")
    temp_dir.mkdir(parents=True, exist_ok=True)
    destination = temp_dir / f"{uuid4().hex}{suffix}"
    try:
        destination.write_bytes(content)
        document_id, chunk_count = get_rag_service().ingest_file(destination, display_filename=filename)
        return DocumentIngestResponse(
            status="success",
            message="Document ingested successfully",
            filename=filename,
            document_id=document_id,
            chunk_count=chunk_count,
        )
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Document ingestion failed; check server logs") from exc
    finally:
        destination.unlink(missing_ok=True)
        await file.close()
