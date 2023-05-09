from django.contrib.auth import get_user_model
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    merchant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        limit_choices_to={"role": User.MERCHANT},
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to="products/")
    quantity = models.PositiveSmallIntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    PENDING = 1
    ON_DELIVERY = 2
    DELIVERED = 3
    CANCELLED = 4

    STATUS_CHOICES = (
        (PENDING, _("pending")),
        (ON_DELIVERY, _("on delivery")),
        (DELIVERED, _("delivered")),
        (CANCELLED, _("cancelled")),
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        limit_choices_to={"role": User.CUSTOMER},
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="orders",
        limit_choices_to={"active": True},
    )
    number = models.CharField(max_length=100, blank=True, default="")
    quantity = models.PositiveSmallIntegerField(default=1)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"{self.number}"

    def save(self, *args, **kwargs):
        self.number = get_random_string(length=6)
        return super(Order, self).save(*args, **kwargs)
