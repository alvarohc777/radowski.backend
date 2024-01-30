from django.contrib import admin
from .models import Poem, Book, Content, PoemBookLanguage
from django.utils.translation import gettext as _


# Register your models here.


class BooksListFilter(admin.SimpleListFilter):
    title = _("Books List")
    parameter_name = "books_list"

    def lookups(self, request, model_admin):
        # Get distinct book titles for all poems
        books = PoemBookLanguage.objects.values_list(
            "book__title", flat=True
        ).distinct()
        return [(book, book) for book in books]

    def queryset(self, request, queryset):
        # Filter poems based on selected book title
        if self.value():
            return queryset.filter(poembooklanguage__book__title=self.value())


@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "title",
        "get_books_list",
    )
    search_fields = ("title",)
    ordering = ("id",)
    list_filter = (BooksListFilter,)

    def get_books_list(self, obj):
        # Assuming there is a reverse relationship from Poem to PoemBookLanguage
        books = obj.poembooklanguage_set.values_list("book__title", flat=True)
        return ", ".join(books)

    get_books_list.short_description = "Books List"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "title",
        "poem_count",
    )
    ordering = ("id",)

    def poem_count(self, obj):
        return obj.poembooklanguage_set.count()

    poem_count.short_description = "Number of Poems"


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "title",
    )
