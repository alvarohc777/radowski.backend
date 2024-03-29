from ninja import NinjaAPI
from django.shortcuts import get_object_or_404

from poem.models import Poem, Book, Content
from poem.schema import PoemBase, BookBase, ContentBase
from typing import List, Optional

# Para hacer agregaciones y aliases
from django.db.models import F, Q, Value, Count
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import JSONObject, Coalesce

api = NinjaAPI()


@api.get("poem/", response=List[PoemBase], tags=["Poem"])
def get_poems(request, title: Optional[str] = None, book: Optional[str] = None):
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
        .order_by("title")
    )
    if title:
        result = result.filter(Q(title__icontains=title))

    if book:
        result = result.filter(Q(book_title__exact=book))

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
            "dedication",
            "body",
            "ig_url",
            "language_id",
            "cover_url",
            language_name=F("language__name"),
            is_active=F("poem__is_active"),
        )
        .annotate(
            books=ArrayAgg("book", distinct=True),
            img_urls=ArrayAgg(Coalesce("img_url", Value("")), distinct=True),
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
            poem=F("book_content__content__poem"),
            language=F("book_content__content__language__name"),
            language_id=F("book_content__content__language__id"),
            language_list=JSONObject(id="language_id", name="language"),
        )
        .values("id", "title", "name", "pdf_url", "cover_url")
        .annotate(
            num_poems=Count("poem", filter=Q(language_id__exact=1)),
            language_list=ArrayAgg("language_list", distinct=True),
        )
    )
    if title:
        result = result.filter(Q(title__icontains=title))

    return result


@api.get("book/{book_id}", response=BookBase, tags=["Book"])
def get_book(request, book_id: int):
    result = (
        Book.objects.annotate(
            poem=F("book_content__content__poem"),
            language=F("book_content__content__language__name"),
            language_id=F("book_content__content__language__id"),
            content_id=F("book_content__content__id"),
            content_title=F("book_content__content__title"),
            content_language=F("book_content__content__language__name"),
        )
        .values(
            "id",
            "title",
            "name",
            "pdf_url",
            "cover_url",
        )
        .annotate(
            num_poems=Count("poem"),
            language_list=ArrayAgg(
                JSONObject(id="language_id", name="language"), distinct=True
            ),
            content=ArrayAgg(
                JSONObject(
                    language="content_language",
                    content=JSONObject(
                        id="content_id",
                        title="content_title",
                    ),
                ),
                distinct=True,
            ),
        )
    )
    book = get_object_or_404(result, id=book_id)

    # Process the result to group poems by language
    grouped_content = []
    for language_info in book["language_list"]:
        language_content = [
            content["content"]
            for content in book["content"]
            if content["language"] == language_info["name"]
        ]
        grouped_content.append(
            {"language": language_info["name"], "content": language_content}
        )

    book["content"] = grouped_content
    return book
