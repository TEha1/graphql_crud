import graphene
from graphene_django import DjangoObjectType

from products.models import Product, Category, Order
from utilities.graphene.exceptions import Unauthorized
from utilities.graphene.filters import (
    CustomPageInfo,
    DjangoFilterInput,
    filter_order_paginate,
    build_q,
)


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        exclude = ("products",)


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        exclude = ("orders",)


class OrderType(DjangoObjectType):
    class Meta:
        model = Order


class Query(graphene.ObjectType):
    products = graphene.List(
        ProductType,
        pk=graphene.Int(),
        page_info=CustomPageInfo(),
        filters=graphene.List(DjangoFilterInput),
    )
    categories = graphene.List(
        CategoryType,
        pk=graphene.Int(),
        page_info=CustomPageInfo(),
        filters=graphene.List(DjangoFilterInput),
    )
    orders = graphene.List(
        OrderType,
        pk=graphene.Int(),
        page_info=CustomPageInfo(),
        filters=graphene.List(DjangoFilterInput),
    )

    @staticmethod
    def resolve_products(root, info, pk: int = None, page_info=None, filters=None):
        user = info.context.user
        if not user.is_authenticated:
            raise Unauthorized()

        return filter_order_paginate(
            Product.objects.all(), build_q(pk, filters), page_info
        )

    @staticmethod
    def resolve_categories(root, info, pk: int = None, page_info=None, filters=None):
        user = info.context.user
        if not user.is_authenticated:
            raise Unauthorized()

        return filter_order_paginate(
            Category.objects.all(), build_q(pk, filters), page_info
        )

    @staticmethod
    def resolve_orders(root, info, pk: int = None, page_info=None, filters=None):
        user = info.context.user
        if not user.is_authenticated:
            raise Unauthorized()

        return filter_order_paginate(
            Order.objects.filter(customer=user), build_q(pk, filters), page_info
        )


__all__ = ["Query"]
