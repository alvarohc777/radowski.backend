from ninja import Schema
from typing import List


class BookRelated(Schema):
    id: int
    title: str


class ContentRelated(Schema):
    id: int
    title: str
    language: str = None


class LanguageContent(Schema):
    language: str
    content: List[BookRelated]


class PoemBase(Schema):
    id: int
    title: str
    name: str
    cover_url: str
    content_list: List[ContentRelated] = None
    book_list: List[BookRelated] = None
    languages: List[str] = None


class Language(Schema):
    id: int
    name: str


class BookBase(Schema):
    id: int
    title: str
    name: str
    pdf_url: str
    cover_url: str
    num_poems: int
    language_list: List[Language] = None
    content: List[LanguageContent] = None


class ContentBase(Schema):
    id: int
    poem_id: int
    title: str
    name: str
    body: str
    language_id: int
    language_name: str
    is_active: bool
    pages: int
    ig_url: str
    cover_url: str
    img_urls: List[str]
    books: List[BookRelated]
