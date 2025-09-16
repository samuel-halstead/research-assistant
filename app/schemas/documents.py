from pydantic import BaseModel


class Document(BaseModel):
    id: int
    title: str
    abstract: str
    authors: list[str]


class DocumentsResponse(BaseModel):
    documents: list[Document]
