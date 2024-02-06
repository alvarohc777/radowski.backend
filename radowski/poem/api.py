from ninja import NinjaAPI
from django.shortcuts import get_object_or_404

from poem.models import Poem, Book, Content
from poem.schema import PoemBase, BookBase, ContentBase
from typing import List, Optional

# Para hacer agregaciones y aliases
from django.db.models import F, Max, Q, Count
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import JSONObject

api = NinjaAPI()


@api.get("poem/", response=List[PoemBase], tags=["Poem"])
def get_poems(request, title: Optional[str] = None):
    result = (
        Poem.objects.exclude(is_active=False)
        .annotate(
            content_id=F("content__id"),
            content_title=F("content__title"),
            content_language=F("content__language__name"),
            content_list=JSONObject(
                id="content_id", title="content_title", language="content_language"
            ),
            book_id=F("content__book_content__book__id"),
            book_title=F("content__book_content__book__title"),
            book_list=JSONObject(id="book_id", title="book_title"),
        )
        .values("id", "title", "name", "cover_url")
        .annotate(
            content_list=ArrayAgg("content_list", distinct=True),
            book_list=ArrayAgg("book_list", distinct=True),
            languages=ArrayAgg("content_language", distinct=True),
        )
    )
    if title:
        result = result.filter(Q(title__icontains=title))

    return result


@api.get("poem/{poem_id}", response=PoemBase, tags=["Poem"])
def get_poem(request, poem_id: int):
    result = (
        Poem.objects.exclude(is_active=False)
        .annotate(
            content_id=F("content__id"),
            content_title=F("content__title"),
            content_language=F("content__language__name"),
            content_list=JSONObject(
                id="content_id", title="content_title", language="content_language"
            ),
            book_id=F("content__book_content__book__id"),
            book_title=F("content__book_content__book__title"),
            book_list=JSONObject(id="book_id", title="book_title"),
        )
        .values("id", "title", "name", "cover_url")
        .annotate(
            content_list=ArrayAgg("content_list", distinct=True),
            book_list=ArrayAgg("book_list", distinct=True),
            languages=ArrayAgg("content_language", distinct=True),
        )
    )
    result = get_object_or_404(result, id=poem_id)
    return result


@api.get("poem/content/{content_id}", response=ContentBase, tags=["Poem"])
def get_content(request, content_id: int):
    result = (
        Content.objects.annotate(
            img_url=F("content_image__img_url"),
            book_id=F("book_content__book__id"),
            book_title=F("book_content__book__title"),
            book=JSONObject(id="book_id", title="book_title"),
        )
        .values(
            "id",
            "poem_id",
            "title",
            "name",
            "body",
            "ig_url",
            "language_id",
            language_name=F("language__name"),
            is_active=F("poem__is_active"),
        )
        .annotate(
            books=ArrayAgg("book", distinct=True),
            img_urls=ArrayAgg("img_url", distinct=True),
            pages=Count("img_url", distinct=True),
        )
        .exclude(is_active=False)
    )

    result = get_object_or_404(result, id=content_id)

    return result


@api.get("book/", response=List[BookBase], tags=["Book"])
def get_books(request, title: Optional[str] = None):
    result = (
        Book.objects.annotate(
            poem=F("pbl__poem__id"),
            language=F("pbl__language__name"),
        )
        .values("id", "title", "name", "pdf_url", "cover_url", "language")
        .annotate(num_poems=Count("poem"))
    )
    if title:
        result = result.filter(
            Q(language__icontains=title) | Q(pbl__poem__name__icontains=title)
        )
    return result


@api.get("book/{book_id}", response=BookBase, tags=["Book"])
def get_book(request, book_id: int):
    result = (
        Book.objects.annotate(
            poem=F("pbl__poem__id"),
            language=F("pbl__language__name"),
            content_language=F("pbl__poem__pcl__language__name"),
            content_title=F("pbl__poem__pcl__content__title"),
            content_id=F("pbl__poem__pcl__content__id"),
            content=JSONObject(
                id="content_id", title="content_title", language="content_language"
            ),
        )
        .order_by()
        .values("id", "title", "name", "pdf_url", "cover_url", "language")
        .annotate(num_poems=Count("poem"), content=ArrayAgg("content", distinct=True))
    )
    book = get_object_or_404(result, id=book_id)

    book["content"] = [
        poem for poem in book["content"] if poem["language"] == book["language"]
    ]

    if not book["content"]:
        del book["content"]

    return book
