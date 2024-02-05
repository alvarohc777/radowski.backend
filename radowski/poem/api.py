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
            book_title=F("pbl__book__title"),
            book_id=F("pbl__book__id"),
            book_language=F("pbl__language__name"),
            book=JSONObject(id="book_id", title="book_title", language="book_language"),
        )
        .values("id", "title", "name", "cover_url")
        .annotate(
            books=ArrayAgg("book", distinct=True),
        )
    )
    if title:
        result = result.filter(Q(title__icontains=title) | Q(books__icontains=title))

    print(f"Total responses: {len(result)}")
    return result


@api.get("poem/{poem_id}", response=PoemBase, tags=["Poem"])
def get_poem(request, poem_id: int):
    result = (
        Poem.objects.exclude(is_active=False)
        .annotate(
            book_id=F("pbl__book__id"),
            book_title=F("pbl__book__title"),
            book_language=F("pbl__language__name"),
            content_id=F("pcl__content__id"),
            content_title=F("pcl__content__title"),
            content_language=F("pcl__language__name"),
            book=JSONObject(id="book_id", title="book_title", language="book_language"),
            content=JSONObject(
                id="content_id", title="content_title", language="content_language"
            ),
        )
        .values("id", "title", "name", "cover_url")
        .annotate(
            books=ArrayAgg("book", distinct=True),
            content=ArrayAgg("content", distinct=True),
        )
    )
    result = get_object_or_404(result, id=poem_id)
    return result


@api.get("poem/content/{content_id}", response=ContentBase, tags=["Poem"])
def get_content(request, content_id: int):
    content = (
        Content.objects.values(
            "id",
            "title",
            "name",
            "body",
            "img_url",
            "ig_url",
            "pages",
            content_language=F("pcl__language__id"),
            book_language=F("pcl__poem__pbl__language__id"),
            poem_id=F("pcl__poem__id"),
            book_id=F("pcl__poem__pbl__book__id"),
            book=F("pcl__poem__pbl__book"),
            language_id=F("pcl__language__id"),
            is_active=F("pcl__poem__is_active"),
        )
        .filter(Q(content_language=F("book_language")))
        .exclude(is_active=False)
    )

    result = get_object_or_404(content, id=content_id)

    num_pages = result["pages"]
    if num_pages > 1:
        result["img_url"] = [
            result["img_url"].replace(".jpg", f"_p{url+1}.jpg")
            for url in range(num_pages)
        ]
    else:
        result["img_url"] = [result["img_url"]]

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
