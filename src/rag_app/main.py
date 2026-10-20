from fastapi import FastAPI

from src.rag_app.api.chat import router as chat_router
from src.rag_app.api.documents import router as documents_router
from src.rag_app.api.health import router as health_router
from src.rag_app.config import settings

app = FastAPI(title="RAG Knowledge Assistant API", version=settings.app_version)
app.include_router(health_router)
app.include_router(documents_router)
app.include_router(chat_router)


@app.get("/", tags=["health"])
async def root() -> dict:
    return {"message": "RAG Knowledge Assistant API is running"}
