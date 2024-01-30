
``` python
# 1. start project
django-admin startproject <project-name>

# 2. run server
python manage.py runserver

# 3. start api app
python manage.py startapp api

# 4. Include api app and 'ninja' to installed apps in project settings.py
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    ...
    "ninja",

    # my apps
    "poem.apps.PoemConfig",
]

# 5. create api.py inside app folder
from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return "hello world"

# 6. Import app.api inside project.urls
urlpatterns = [path("admin/", admin.site.urls), path("api/", include("poem.urls"))]

# 7. Install psycopg
pip install psycopg
pip install --upgrade pip
pip install "psycopg[binary,pool]"

# 7. Update DATABASES dictionary with connection string
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "radowski_dev",
        "USER": "alvarohc777",
        "PASSWORD": "rada-app#1",
        "HOST": "radowski.postgres.database.azure.com",
        "PORT": "5432",
    }
}

# Scaffold postgres DB
python manage.py inspectdb > models_test.py
python manage.py makemigrations
python manage.py migrate --fake-initial

# create super user
python manage.py createsuperuser


# Register models in admin page
from .models import Poem, Book, Content

@admin.register(Poem)
class PoemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "title",
    )
    search_fields = ("title",)
    list_filter = ("title",)

# Create Schemas
from poem.models import Poem
from ninja import Schema
from ninja.orm import create_schema

PoemBase = create_schema(Poem, fields=["id", "name", "title"])


# Create Endpoint

from ninja import NinjaAPI

from poem.models import Poem
from poem.schema import PoemBase
from typing import List, Optional

api = NinjaAPI()

@api.get("", response=List[PoemBase], tags=["Poem"])
def poem(request, nombre: Optional[str] = None):
    if nombre:
        return Poem.objects.filter(nombre__icontains=nombre)
    return Poem.objects.all()


# CORS HEADER
pip install django-cors-headers 


INSTALLED_APPS = [
    # ...
    'corsheaders',
    # ...
]

MIDDLEWARE = [
    # ...
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:9000",
    # Add other allowed origins as needed
]

CORS_ORIGIN_ALLOW_ALL = True

```


