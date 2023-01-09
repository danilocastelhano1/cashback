from django.db import models

from .base_model import BaseModel
from .cashback import Cashback


class Products(BaseModel):
    TYPES_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
    ]

    cashback = models.ForeignKey(
        to=Cashback,
        related_name="products",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    type = models.CharField(
        max_length=11, null=False, blank=False, choices=TYPES_CHOICES
    )
    value = models.DecimalField(
        max_digits=12, decimal_places=2, blank=False, null=False
    )
    qty = models.PositiveIntegerField(blank=False, null=False)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return f"Cashback ID: {self.cashback.id}, Product Type {self.type}"
