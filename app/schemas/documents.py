import uuid
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Document(BaseModel):
    uuid: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    abstract: str
    authors: list[str]

    @field_validator("authors", mode="before")
    def split_authors(cls, v):
        if isinstance(v, str):
            return [author.strip() for author in v.split(";")]
        return v


class DocumentsResponse(BaseModel):
    documents: list[Document]
