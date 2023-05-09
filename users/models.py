from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    CUSTOMER = 1
    MERCHANT = 2
    ADMIN = 3

    ROLE_CHOICES = (
        (CUSTOMER, _("customer")),
        (MERCHANT, _("merchant")),
        (ADMIN, _("admin")),
    )

    username = models.CharField(
        verbose_name=_("username"),
        max_length=50,
        unique=True,
    )
    email = models.EmailField(blank=False, max_length=255, verbose_name="email")
    full_name = models.CharField(verbose_name=_("full name"), max_length=200)
    profile_info = models.TextField(verbose_name=_("profile information"), blank=True)
    role = models.PositiveSmallIntegerField(
        verbose_name=_("role"), choices=ROLE_CHOICES, default=CUSTOMER
    )
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.username}"
