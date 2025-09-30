from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.documents import Document


class ResearchRequest(BaseModel):
    query: str


class ResearchResponseDocument(Document):
    similarity: float


class ResearchResponse(BaseModel):
    are_relevant_documents: bool
    documents: Optional[List[ResearchResponseDocument]] = Field(default=None)
    comparison: Optional[str] = Field(default=None)
