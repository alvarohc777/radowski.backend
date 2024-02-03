from ninja import Schema
from typing import List


class PoemBase(Schema):
    id: int
    title: str
    name: str
    cover_url: str
    content: List[str] = None
    content_id: List[int] = None
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
    content_list: List[str] = None
    content_id: List[int] = None
    language: str


class ContentBase(Schema):
    id: int

    title: str
    name: str
    pages: int
    img_url: List[str]
    body: str = None
    poem_id: int
    book: int = None
    language_id: int
