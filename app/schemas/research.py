from typing import List, Optional

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    query: str


class ResearchResponseDocument(BaseModel):
    index: int
    abstract: str


class ResearchResponse(BaseModel):
    are_relevant_documents: bool
    documents: Optional[List[ResearchResponseDocument]] = Field(default=None)
    summary: Optional[str] = Field(default=None)
