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