from rest_framework import serializers
from main.apps.categories.models import Category

from .base_serializers import BasePortfolioSerializer
from .. import models


class StocksSerializer(BasePortfolioSerializer):
    evaluation = serializers.FloatField(required=False, allow_null=True)
    past_evaluation = serializers.FloatField(required=False, allow_null=True)

    class Meta:
        model = models.Stock
        fields = BasePortfolioSerializer.Meta.fields + [
            'evaluation',
            'past_evaluation',
        ]
        read_only_fields = BasePortfolioSerializer.Meta.read_only_fields

    def get_category(self):
        return Category.get_stock()

