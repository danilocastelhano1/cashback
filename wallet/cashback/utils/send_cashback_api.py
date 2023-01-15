import requests

from typing import Dict

from django.conf import settings


class SendCashbackApi(object):
    def __init__(self):
        self.CASHBACK_URL = settings.CASHBACK_URL

    def send_cashback_to_api(self, data=Dict):
        return requests.post(self.CASHBACK_URL, data=data)
