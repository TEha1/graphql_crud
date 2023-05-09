import graphene

import users.schema
import products.schema


# IOC gql
class Query(
    users.schema.Query,
    products.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    users.schema.AuthMutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
