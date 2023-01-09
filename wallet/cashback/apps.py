from django.apps import AppConfig


class CashbackConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wallet.cashback"

    def ready(self):
        import wallet.cashback.signals
