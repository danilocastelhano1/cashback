import logging
import requests

from decimal import Decimal

from django.conf import settings

from celery import shared_task, states
from celery.exceptions import Ignore

from wallet.cashback.models.cashback import Cashback
from wallet.cashback.utils.send_cashback_api import SendCashbackApi

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def send_cashback_info(self):
    response: str = ""
    logger.info("Starting task to send_cashback_info to external API")
    try:
        cashbacks_to_process = Cashback.objects.filter(sent_to_api=False).all()
        processed_with_success: int = 0
        processed_with_error: int = 0

        for cashback_to_process in cashbacks_to_process:
            logger.info("Trying to send cashback %d", cashback_to_process.id)
            data = {
                "document": cashback_to_process.customer.document,
                "cashback": round(cashback_to_process.total * Decimal((settings.CASHBACK_PERCENT / 100)), 2),
            }
            cashback_to_process.total_cashback = data["cashback"]

            response: requests.Response = SendCashbackApi().send_cashback_to_api(data=data)
            if response.status_code == 201:
                cashback_to_process.sent_to_api = True
                cashback_to_process.result_api = response.json()
                processed_with_success += 1
                logger.info("Cashback %d, sent successfully", cashback_to_process.id)
            else:
                cashback_to_process.sent_to_api = False
                cashback_to_process.result_api = response.json()
                processed_with_error += 1
                logger.error(
                    "Cashback %d, sent with errors %s",
                    cashback_to_process.id,
                    response.content,
                )

            cashback_to_process.save()

            logger.info(f"Task concluded with SUCCESS, with {str(processed_with_success)} processed successfully "
                        f"and {processed_with_error} processed with error")
    except Exception as ex:
        logger.error("Exception Executing the task, " + str(ex))
        self.update_state(state=states.FAILURE, meta=response)
        raise Ignore()
