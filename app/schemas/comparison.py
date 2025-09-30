from pydantic import BaseModel


class Comparison(BaseModel):
    comparison: str
