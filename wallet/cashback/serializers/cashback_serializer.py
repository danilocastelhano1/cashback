import logging
from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from ..models import Cashback, Customer, Products
from ..serializers.customer_serializer import CustomerSerializer
from ..serializers.product_serializer import ProductSerializer

logger = logging.getLogger(__name__)


class CashbackSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(many=False, required=True)
    products = ProductSerializer(many=True, required=True)

    class Meta:
        model = Cashback
        fields = ("sold_at", "customer", "total", "products")
        read_only_fields = ("id", "created_at", "updated_at")

    @transaction.atomic
    def create(self, validated_data):
        logger.info("Creating new cashback in database")
        products = validated_data.pop("products")
        customer = self.create_or_get_customer(validated_data.pop("customer"))
        validated_data["customer"] = customer

        cashback = Cashback.objects.create(**validated_data)
        for product in products:
            Products.objects.create(cashback=cashback, **product)

        return cashback

    def create_or_get_customer(self, customer) -> Customer:
        """
        Get or create new customer
        """
        customer, _ = Customer.objects.get_or_create(
            document=customer["document"], defaults={"name": customer["name"]}
        )
        return customer

    def validate_products(self, value):
        """
        Validate total product vs total items
        """
        logger.info("Validating products")
        total_calculated: Decimal = Decimal(0)
        for product in value:
            total_calculated += Decimal(product["qty"]) * Decimal(product["value"])

        if Decimal(self.initial_data["total"]) != total_calculated:
            logger.error("Total does not match with the sum of products %.2f, %.2f",
                         Decimal(self.initial_data["total"]), total_calculated)
            raise serializers.ValidationError(
                detail="Total does not match with the sum of products"
            )
        return value
