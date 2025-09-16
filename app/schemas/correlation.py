from pydantic import BaseModel


class Correlation(BaseModel):
    indexes: list[int]
