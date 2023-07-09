from typing import Optional

from pydantic import BaseModel


class Link(BaseModel):
    url: str


class LinkUpdate(BaseModel):
    id: int
    result_url: str


class LinkInDB(Link):
    id: int
    result_url: Optional[str]

    class Config:
        orm_mode = True