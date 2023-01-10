import requests
from decimal import Decimal
from django.conf import settings


class SendCashbackApi(object):

    def __init__(self):
        self.CASHBACK_URL = settings.CASHBACK_URL
        self.CASHBACK_PERCENT = settings.CASHBACK_PERCENT

    def send_cashback_to_api(self, document: str, total: Decimal):
        data = {
            "document": document,
            "cashback": round(
                total * Decimal((self.CASHBACK_PERCENT / 100)), 2
            ),
        }

        return requests.post(self.CASHBACK_URL, data=data)
