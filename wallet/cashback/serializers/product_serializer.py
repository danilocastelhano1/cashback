from rest_framework import serializers

from ..models import Products


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = (
           "type", "value", "qty"
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
