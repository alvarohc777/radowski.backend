from ninja import Schema
from typing import List


class PoemBase(Schema):
    id: int
    title: str
    name: str
    cover_url: str
    languages: List[str] = None
    books: List[str] = None
    books_ids: List[int] = None


class BookBase(Schema):
    id: int
    title: str
    name: str
    pdf_url: str
    cover_url: str
    num_poems: int
    language: str
