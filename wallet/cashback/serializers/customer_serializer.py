from rest_framework import serializers

from ..models import Customer
from ..utils.validate_cpf import validate_cpf


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("document", "name")
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_document(self, value):
        if not validate_cpf(value):
            raise serializers.ValidationError(detail="Invalid CPF")
        return value
