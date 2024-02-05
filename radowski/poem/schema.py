from ninja import Schema
from typing import List


class BookRelated(Schema):
    id: int
    title: str
    language: str


class ContentRelated(Schema):
    id: int
    title: str
    language: str


class PoemBase(Schema):
    id: int
    title: str
    name: str
    cover_url: str
    content: List[ContentRelated] = None
    books: List[BookRelated] = None


class BookBase(Schema):
    id: int
    title: str
    name: str
    pdf_url: str
    cover_url: str
    num_poems: int
    content: List[ContentRelated] = None
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
