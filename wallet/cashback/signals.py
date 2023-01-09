import requests
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Cashback


@receiver(post_save, sender=Cashback)
def cashback_post_save(sender, instance, **kwargs):
    data = {
        "document": instance.customer.document,
        "cashback": round(instance.total * Decimal((settings.CASHBACK_PERCENT / 100)),2)
    }

    response = requests.post(settings.CASHBACK_URL, data=data)
    if response.status_code == 201:
        pass
    else:
        pass
