from ninja import NinjaAPI

from poem.models import Poem, Book
from poem.schema import PoemBase, BookBase
from typing import List, Optional

# Para hacer agregaciones y aliases
from django.db.models import F, Max, Q, Count
from django.contrib.postgres.aggregates import ArrayAgg

api = NinjaAPI()


@api.get("poem/", response=List[PoemBase], tags=["Test"])
def poem(request, title: Optional[str] = None):
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


@api.get("book/", response=List[BookBase], tags=["Poem"])
def poem(request, title: Optional[str] = None):
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
