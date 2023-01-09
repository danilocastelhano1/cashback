from django.urls import include, path
from rest_framework import routers

from .views.cashback_view import CashbackViewset

router = routers.DefaultRouter()
router.register(r"cashback", CashbackViewset)

urlpatterns = [
    path(r"api/", include(router.urls)),
]
