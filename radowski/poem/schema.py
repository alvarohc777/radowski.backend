from ninja import Schema
from typing import List


class BookRelated(Schema):
    id: int
    title: str


class ContentRelated(Schema):
    id: int
    title: str
    language: str


class PoemBase(Schema):
    id: int
    title: str
    name: str
    cover_url: str
    content_list: List[ContentRelated] = None
    book_list: List[BookRelated] = None
    languages: List[str] = None


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
    poem_id: int
    title: str
    name: str
    body: str
    ig_url: str
    language_id: int
    language_name: str
    is_active: bool
    pages: int
    img_urls: List[str]
    books: List[BookRelated]
