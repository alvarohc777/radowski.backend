from ninja import Schema
from typing import List

class PoemBase(Schema):
    id: int
    title: str
    name: str
    cover_url: str
    languages: List[str] = None
    books: List[str] = None
