from django.core.exceptions import ValidationError
from django.db import models

from ..utils.validate_cpf import validate_cpf
from .base_model import BaseModel


class Customer(BaseModel):
    document = models.CharField(max_length=11, null=False, blank=False)
    name = models.CharField(max_length=60, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name

    def clean(self):
        """In case insert via admin page"""
        if not validate_cpf(str(self.document)):
            raise ValidationError({"document": "Invalid document"})
