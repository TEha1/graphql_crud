import typing

from django.utils.translation import gettext_lazy as _
from graphql import GraphQLError
from graphene.utils.str_converters import to_camel_case
from rest_framework import status


class HTTPGraphQLError(GraphQLError):
    def __init__(
        self,
        http_status: int,
        http_status_text: str,
        reason: typing.Dict = None,
        *args,
        **kwargs,
    ):
        if reason:
            reason = {to_camel_case(key): value for key, value in reason.items()}
        extensions = {
            "http": {
                "status": http_status,
                "status_text": http_status_text,
                "reason": reason,
            },
        }
        super().__init__(extensions=extensions, *args, **kwargs)


class Unauthorized(HTTPGraphQLError):
    def __init__(self, *args, **kwargs):
        super().__init__(
            message=_("Unauthorized"),
            http_status=status.HTTP_401_UNAUTHORIZED,
            http_status_text="Unauthorized",
            *args,
            **kwargs,
        )


class Forbidden(HTTPGraphQLError):
    def __init__(self, *args, **kwargs):
        super().__init__(
            message=_("Forbidden"),
            http_status=status.HTTP_403_FORBIDDEN,
            http_status_text="Forbidden",
            *args,
            **kwargs,
        )


class NotFound(HTTPGraphQLError):
    def __init__(self, *args, **kwargs):
        super().__init__(
            message=_("Not Found"),
            http_status=status.HTTP_404_NOT_FOUND,
            http_status_text="Not Found",
            *args,
            **kwargs,
        )


class BadRequest(HTTPGraphQLError):
    def __init__(self, reason: typing.Dict, *args, **kwargs):
        super().__init__(
            message=_("Bad Request"),
            http_status=status.HTTP_400_BAD_REQUEST,
            http_status_text="Bad Request",
            reason=reason,
            *args,
            **kwargs,
        )
