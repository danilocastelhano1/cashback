from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from ..models import Cashback
from ..serializers.cashback_serializer import CashbackSerializer


class CashbackViewset(viewsets.GenericViewSet,
                      mixins.CreateModelMixin):
    queryset = Cashback.objects.all()
    serializer_class = CashbackSerializer
    permission_classes = [AllowAny]
