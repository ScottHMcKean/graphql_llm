# GraphQL LLM
A proof of concept for conecting GraphQL & Langchain

This project is a proof of concept for using Langchain with GraphQl. It ships a mock GraphQL Server using Graphene, along with three APIs that are abstracted behind the GraphQL Server. The APIs are:

1. A weather API
2. A database API
3. A served model endpoint API

It then uses a Langchain Agent to interact with the GraphQL Server. The Agent is designed to be a multi-step workflow that uses the APIs to answer a user's question. It uses the GraphQL toolkit to interact with the GraphQL Server. The LLM interacts with users and determines what the user's question is, then determines the appropriate API to use, and then uses the GraphQL API to get the answer to the user's question.

## Initial Setup

We'll use Graphene-Django for GraphQL integration. Here's how to set it up:
1. First, create a new Django project and app:
```
# Create a new directory for your project
mkdir django_graphql_demo
cd django_graphql_demo

# Create a virtual environment and activate it
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install Django and Graphene-Django
pip install django graphene-django

# Create a new Django project
django-admin startproject demo_project .

# Create a new Django app
python manage.py startapp demo_app
```


2. Add 'graphene_django' and 'demo_app' to your INSTALLED_APPS in `demo_project/settings.py`:

```python:demo_project/settings.py
INSTALLED_APPS = [
    # ... other apps ...
    'graphene_django',
    'demo_app',
]

# Add this at the end of the file
GRAPHENE = {
    'SCHEMA': 'demo_project.schema.schema'
}
```


3. Create a simple model in `demo_app/models.py`:

```python:demo_app/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title
```

4. Create a new file `demo_app/schema.py`:

```python:demo_app/schema.py
import graphene
from graphene_django import DjangoObjectType
from .models import Book

class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id", "title", "author")

class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)
    book_by_id = graphene.Field(BookType, id=graphene.Int(required=True))

    def resolve_all_books(self, info):
        return Book.objects.all()

    def resolve_book_by_id(self, info, id):
        return Book.objects.get(pk=id)

schema = graphene.Schema(query=Query)
```

5. Create a new file `demo_project/schema.py`:

```python:demo_project/schema.py
import graphene
import demo_app.schema

class Query(demo_app.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
```


6. Update `demo_project/urls.py`:

```python:demo_project/urls.py
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
```

7. Apply migrations and create a superuser:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```


8. Run the development server:

```bash
python manage.py runserver
```


Now you have a simple Django GraphQL app up and running. You can test it by following these steps:

1. Open your browser and go to http://localhost:8000/admin/
2. Log in with the superuser credentials you created
3. Add a few books through the admin interface
4. Go to http://localhost:8000/graphql/

You can now test your GraphQL queries. For example:

```
{
  allBooks {
    id
    title
    author
  }
}
```

```
query {
  bookById(id: 1) {
    title
    author
  }
}
```

This setup provides a basic GraphQL API with Django that you can test and expand upon. It includes a simple Book model and queries to fetch all books or a specific book by ID.