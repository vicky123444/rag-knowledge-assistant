from fastapi import APIRouter, HTTPException

from src.rag_app.schemas.chat import AskQuestionRequest, AskQuestionResponse
from src.rag_app.services.rag_service import get_rag_service

router = APIRouter()


@router.post("/chat/ask", response_model=AskQuestionResponse, tags=["chat"])
async def ask_question(payload: AskQuestionRequest) -> AskQuestionResponse:
    try:
        answer, context = get_rag_service().ask_question(payload.question, top_k=payload.top_k)
        sources = [
            {
                "document": item.get("filename") or "unknown",
                "page": item.get("page_number"),
                "excerpt": (item.get("text") or "")[:300],
            }
            for item in context
        ]
        return AskQuestionResponse(answer=answer, sources=sources)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Question answering failed; check server logs") from exc
