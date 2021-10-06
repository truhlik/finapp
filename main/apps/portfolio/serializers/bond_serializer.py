from rest_framework import serializers
from main.apps.categories.models import Category

from .base_serializers import BasePortfolioSerializer
from .. import models
from ..constants import BOND_PAYMENT_FREQUENCY_CHOICES
from ...products.models import Product


class BondsSerializer(BasePortfolioSerializer):
    evaluation = serializers.FloatField(required=False, allow_null=True)
    payment_frequency = serializers.ChoiceField(choices=BOND_PAYMENT_FREQUENCY_CHOICES)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.active(),
                                                    required=False,
                                                    source='product', allow_null=True)  # todo active jen při create
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = models.Bond
        fields = BasePortfolioSerializer.Meta.fields + [
            'evaluation',
            'payment_frequency',
            'start_date',
            'end_date',
        ]
        read_only_fields = BasePortfolioSerializer.Meta.read_only_fields

    def get_category(self):
        return Category.get_bond()


