from rest_framework import serializers

from .models import Product
from main.apps.currencies.serializer import CurrencySerializer


class ProductSerializer(serializers.ModelSerializer):
    currencies = CurrencySerializer(many=True, allow_null=True)
    evaluation = serializers.DecimalField(decimal_places=2, max_digits=10, coerce_to_string=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'currencies', 'evaluation']
        read_only_fields = fields
