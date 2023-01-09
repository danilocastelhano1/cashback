from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Cashback

from .utils.send_cashback_api import SendCashbackApi


@receiver(post_save, sender=Cashback)
def cashback_post_save(sender, instance, created, *args, **kwargs):
    if created:
        response = SendCashbackApi().send_cashback_to_api(instance.customer.document, instance.total)

        if response.status_code == 201:
            instance.sent_to_api = True
            instance.result_api = response.json()
        else:
            instance.sent_to_api = False
            instance.result_api = response.json()

        instance.save()
