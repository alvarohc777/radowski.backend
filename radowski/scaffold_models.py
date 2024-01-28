# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=35)
    title = models.CharField(max_length=35)
    pdf_url = models.CharField(max_length=100)
    cover_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "book"


class Content(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=35)
    title = models.CharField(max_length=35)
    body = models.CharField(max_length=2500)
    pages = models.IntegerField()
    cover_url = models.CharField(max_length=100)
    img_url = models.CharField(max_length=100, blank=True, null=True)
    ig_url = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "content"


class Language(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=35)

    class Meta:
        managed = False
        db_table = "language"


class Poem(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=35)
    title = models.CharField(max_length=35)
    cover_url = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "poem"


class PoemBookLanguage(models.Model):
    id = models.IntegerField(primary_key=True)
    poem = models.ForeignKey(Poem, models.DO_NOTHING)
    book = models.ForeignKey(Book, models.DO_NOTHING)
    language = models.ForeignKey(Language, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "poem_book_language"
        unique_together = (("book", "poem", "language"),)


class PoemContentLanguage(models.Model):
    id = models.IntegerField(primary_key=True)
    poem = models.ForeignKey(Poem, models.DO_NOTHING)
    content = models.ForeignKey(Content, models.DO_NOTHING)
    language = models.ForeignKey(Language, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "poem_content_language"
