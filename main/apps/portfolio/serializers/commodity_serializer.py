from django.utils import timezone
from rest_framework import serializers
from main.apps.categories.models import Category

from .base_serializers import BasePortfolioSerializer
from .. import models


class CommoditySerializer(BasePortfolioSerializer):
    evaluation = serializers.FloatField(required=True)
    buy_price = serializers.FloatField(required=False, min_value=0, allow_null=True)
    income = serializers.IntegerField(required=False, min_value=0, allow_null=True)
    start_date = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = models.Commodity
        fields = BasePortfolioSerializer.Meta.fields + [
            'evaluation',
            'buy_price',
            'start_date',
            'income',
        ]
        read_only_fields = BasePortfolioSerializer.Meta.read_only_fields

    def get_category(self):
        return Category.get_commodity()

    def validate_start_date(self, value):
        if value and value >= timezone.now().date():
            raise serializers.ValidationError('nemůžete zadat datum v budoucnosti')
        return value
