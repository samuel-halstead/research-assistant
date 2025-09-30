from pydantic import BaseModel


class Translation(BaseModel):
    translated_title: str
    translated_abstract: str
