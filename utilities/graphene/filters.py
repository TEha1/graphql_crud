import datetime
import json
import typing
from enum import Enum

import graphene
from django.db.models import Q


class DjangoFilterClauses(Enum):
    # text clauses
    exact = "exact"
    iexact = "iexact"
    contains = "contains"
    icontains = "icontains"

    # values in clauses
    values_in = "in"

    # numbers
    gt = "gt"
    lt = "lt"
    gte = "gte"
    lte = "lte"

    # dates
    date__gt = "date__gt"
    date__lt = "date__lt"
    date__gte = "date__gte"
    date__lte = "date__lte"

    # times
    time__gt = "time__gt"
    time__lt = "time__lt"
    time__gte = "time__gte"
    time__lte = "time__lte"


DjangoFilterChoices = graphene.Enum.from_enum(DjangoFilterClauses)


class DjangoFilterInput(graphene.InputObjectType):
    field = graphene.String(required=True)
    value = graphene.String(required=True)
    clause = graphene.Field(DjangoFilterChoices)


class CustomPageInfo(graphene.InputObjectType):
    limit = graphene.Int()
    offset = graphene.Int()
    order_by = graphene.String()


_conversion_methods = {
    # string conversions
    "exact": lambda x: x,
    "iexact": lambda x: x,
    "contains": lambda x: x,
    "icontains": lambda x: x,
    # numbers conversions
    "gt": float,
    "lt": float,
    "gte": float,
    "lte": float,
    # date time conversions
    "date__gt": lambda x: datetime.date.fromisoformat(x).isoformat(),
    "date__lt": lambda x: datetime.date.fromisoformat(x).isoformat(),
    "date__gte": lambda x: datetime.date.fromisoformat(x).isoformat(),
    "date__lte": lambda x: datetime.date.fromisoformat(x).isoformat(),
    "time__gt": lambda x: datetime.time.fromisoformat(x).isoformat(),
    "time__lt": lambda x: datetime.time.fromisoformat(x).isoformat(),
    "time__gte": lambda x: datetime.time.fromisoformat(x).isoformat(),
    "time__lte": lambda x: datetime.time.fromisoformat(x).isoformat(),
    # ids_ in clause conversions
    "in": lambda x: json.loads(x),
}


def build_q(pk: int = None, filters: typing.List = None):
    if filters is None:
        filters = list()

    if pk is not None:
        filters.append({"field": "pk", "value": pk})

    q_filters = {}
    for f in filters:
        field = f.get("field")
        clause = f.get("clause", "exact")
        value = _conversion_methods.get(clause)(f.get("value"))
        q_filters.update({f"{field}__{clause}": value})
    return Q(**q_filters)


def filter_order_paginate(qs, q: Q, page_info: typing.Dict = None):
    page_info = page_info or dict()
    limit = page_info.get("limit", 100)
    offset = page_info.get("offset", 0)
    order_by = "__".join(page_info.get("order_by", "").strip().split("."))
    if order_by:
        return qs.filter(q).order_by(order_by)[offset : limit + offset]
    return qs.filter(q)[offset : limit + offset]


__all__ = [
    "CustomPageInfo",
    "DjangoFilterInput",
    "filter_order_paginate",
    "build_q",
]
