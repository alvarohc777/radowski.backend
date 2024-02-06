# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=35)
    title = models.CharField(max_length=35)
    pdf_url = models.CharField(max_length=100)
    cover_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "book"


class BookContent(models.Model):
    book = models.ForeignKey(Book, models.DO_NOTHING, related_name="book_content")
    content = models.ForeignKey(
        "Content", models.DO_NOTHING, related_name="book_content"
    )

    class Meta:
        managed = False
        db_table = "book_content"
        unique_together = (("book", "content"),)


class Content(models.Model):
    poem = models.ForeignKey("Poem", models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=35)
    title = models.CharField(max_length=35)
    body = models.CharField(max_length=2500)
    cover_url = models.CharField(max_length=100)
    ig_url = models.CharField(max_length=100, blank=True, null=True)
    language = models.ForeignKey("Language", models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "content"


class ContentImage(models.Model):
    content = models.ForeignKey(
        Content, models.DO_NOTHING, related_name="content_image"
    )
    pages = models.IntegerField()
    img_url = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "content_image"


class Language(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=35)
    original_name = models.CharField(max_length=35)

    class Meta:
        managed = False
        db_table = "language"


class Poem(models.Model):
    name = models.CharField(max_length=35)
    title = models.CharField(max_length=35)
    cover_url = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "poem"
