import uuid
from typing import Optional

from pydantic import BaseModel, Field


class Document(BaseModel):
    uuid: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    abstract: str
    authors: list[str]


class DocumentsResponse(BaseModel):
    documents: list[Document]
