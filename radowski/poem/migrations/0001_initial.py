# Generated by Django 4.2.9 on 2024-01-28 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=35)),
                ("title", models.CharField(max_length=35)),
                ("pdf_url", models.CharField(max_length=100)),
                ("cover_url", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "book",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Content",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=35)),
                ("title", models.CharField(max_length=35)),
                ("body", models.CharField(max_length=2500)),
                ("pages", models.IntegerField()),
                ("cover_url", models.CharField(max_length=100)),
                ("img_url", models.CharField(blank=True, max_length=100, null=True)),
                ("ig_url", models.CharField(blank=True, max_length=100, null=True)),
                ("created_at", models.DateTimeField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "content",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Language",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=35)),
            ],
            options={
                "db_table": "language",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Poem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=35)),
                ("title", models.CharField(max_length=35)),
                ("cover_url", models.CharField(blank=True, max_length=100, null=True)),
                ("is_active", models.BooleanField()),
                ("created_at", models.DateTimeField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "poem",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PoemBookLanguage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "db_table": "poem_book_language",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PoemContentLanguage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "db_table": "poem_content_language",
                "managed": False,
            },
        ),
    ]
