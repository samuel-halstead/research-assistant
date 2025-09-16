from pydantic import BaseModel


class DocListResponse(BaseModel):
    index: int
    title: str
    abstract: str
    source_id: str
    similarity: float
