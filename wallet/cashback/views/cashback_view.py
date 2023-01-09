from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Cashback
from ..serializers.cashback_serializer import CashbackSerializer


class CashbackViewset(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Cashback.objects.all()
    serializer_class = CashbackSerializer
    permission_classes = [IsAuthenticated]
