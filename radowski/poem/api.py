from ninja import NinjaAPI
from django.shortcuts import get_object_or_404

from poem.models import Poem, Book, Content
from poem.schema import PoemBase, BookBase, ContentBase
from typing import List, Optional

# Para hacer agregaciones y aliases
from django.db.models import F, Max, Q, Count
from django.contrib.postgres.aggregates import ArrayAgg

api = NinjaAPI()


@api.get("poem/", response=List[PoemBase], tags=["Poem"])
def get_poems(request, title: Optional[str] = None):
    result = (
        Poem.objects.exclude(is_active=False)
        .annotate(
            language_name=F("poem_book_language__language__name"),
            book_title=F("poem_book_language__book__title"),
            book_id=F("poem_book_language__book__id"),
        )
        .values("id", "title", "name", "cover_url")
        .annotate(
            # title=Max("title"),
            languages=ArrayAgg("language_name", distinct=True),
            books=ArrayAgg("book_title", distinct=True),
            books_ids=ArrayAgg("book_id", distinct=True),
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
            language_name=F("poem_book_language__language__name"),
            book_title=F("poem_book_language__book__title"),
            book_id=F("poem_book_language__book__id"),
        )
        .values("id", "title", "name", "cover_url")
        .annotate(
            languages=ArrayAgg("language_name", distinct=True),
            books=ArrayAgg("book_title", distinct=True),
            books_ids=ArrayAgg("book_id", distinct=True),
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
            content_language=F("poem_content_language__language__id"),
            book_language=F(
                "poem_content_language__poem__poem_book_language__language__id"
            ),
            poem_id=F("poem_content_language__poem__id"),
            book_id=F("poem_content_language__poem__poem_book_language__book__id"),
            book=F("poem_content_language__poem__poem_book_language__book"),
            language_id=F("poem_content_language__language__id"),
            is_active=F("poem_content_language__poem__is_active"),
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
            poem=F("poem_book_language__poem__id"),
            language=F("poem_book_language__language__name"),
        )
        .values("id", "title", "name", "pdf_url", "cover_url", "language")
        .annotate(num_poems=Count("poem"))
    )
    if title:
        result = result.filter(
            Q(language__icontains=title)
            | Q(poem_book_language__poem__name__icontains=title)
        )
    return result


@api.get("book/{book_id}", response=BookBase, tags=["Book"])
def get_book(request, book_id: int):
    result = (
        Book.objects.annotate(
            poem=F("poem_book_language__poem__id"),
            language=F("poem_book_language__language__name"),
        )
        .values("id", "title", "name", "pdf_url", "cover_url", "language")
        .annotate(num_poems=Count("poem"))
    )
    book = get_object_or_404(result, id=book_id)

    return book


@api.get("poem/{poem_id}", response=ContentBase, tags=["Poem"])
def get_poem(request, poem_id: int):
    content = Content.objects.values(
        "id",
        "title",
        "name",
        "body",
        "img_url",
        "ig_url",
        "pages",
        content_language=F("poem_content_language__language__id"),
        book_language=F(
            "poem_content_language__poem__poem_book_language__language__id"
        ),
        poem_id=F("poem_content_language__poem__id"),
        book_id=F("poem_content_language__poem__poem_book_language__book__id"),
        book=F("poem_content_language__poem__poem_book_language__book"),
        language_id=F("poem_content_language__language__id"),
    ).filter(Q(content_language=F("book_language")))

    result = get_object_or_404(content, id=poem_id)

    num_pages = result["pages"]
    if num_pages > 1:
        result["img_url"] = [
            result["img_url"].replace(".jpg", f"_p{url+1}.jpg")
            for url in range(num_pages)
        ]
    else:
        result["img_url"] = [result["img_url"]]

    return result
