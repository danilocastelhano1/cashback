from django.db import models

from .base_model import BaseModel
from .customer import Customer


class Cashback(BaseModel):
    sold_at = models.DateTimeField(blank=False, null=False)
    customer = models.ForeignKey(
        to=Customer,
        related_name="cashback_customer",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    total = models.DecimalField(
        max_digits=12, decimal_places=2, blank=False, null=False
    )
    sent_to_api = models.BooleanField(default=False)
    result_api = models.JSONField(blank=True, null=True, default=dict)

    class Meta:
        verbose_name_plural = "Cashback's"

    def __str__(self):
        return str(self.id)
