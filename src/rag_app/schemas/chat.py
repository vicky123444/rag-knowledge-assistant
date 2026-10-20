from pydantic import BaseModel, Field

from src.rag_app.schemas.document import SourceReference


class AskQuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=4000)
    top_k: int = Field(default=4, ge=1, le=10)


class AskQuestionResponse(BaseModel):
    answer: str
    sources: list[SourceReference]
