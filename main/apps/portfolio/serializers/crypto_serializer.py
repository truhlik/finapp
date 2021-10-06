from rest_framework import serializers
from main.apps.categories.models import Category

from .base_serializers import BasePortfolioSerializer
from .. import models


class CryptosSerializer(BasePortfolioSerializer):
    evaluation = serializers.FloatField(required=False, allow_null=True)
    past_evaluation = serializers.FloatField(required=False, allow_null=True)
    income = serializers.IntegerField(required=False, min_value=0, allow_null=True)

    class Meta:
        model = models.Crypto
        fields = BasePortfolioSerializer.Meta.fields + [
            'evaluation',
            'past_evaluation',
            'income',
        ]
        read_only_fields = BasePortfolioSerializer.Meta.read_only_fields

    def get_category(self):
        return Category.get_crypto()


