import graphene
import graphql_app.schema

class Query(graphql_app.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)