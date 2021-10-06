from rest_framework import serializers
from main.apps.categories.models import Category

from .base_serializers import BaseWithInsitutionPortfolioSerializer
from .. import models
from ..constants import SAVING_ACCOUNT_PAYMENT_FREQUENCY_CHOICES


class SavingAccountSerializer(BaseWithInsitutionPortfolioSerializer):
    evaluation = serializers.FloatField(required=True)
    payment_frequency = serializers.ChoiceField(required=True, choices=SAVING_ACCOUNT_PAYMENT_FREQUENCY_CHOICES)
    income = serializers.IntegerField(required=False, min_value=0, allow_null=True)

    class Meta:
        model = models.SavingAccount
        fields = BaseWithInsitutionPortfolioSerializer.Meta.fields + [
            'evaluation',
            'payment_frequency',
            'income',
        ]
        read_only_fields = BaseWithInsitutionPortfolioSerializer.Meta.read_only_fields

    def get_category(self):
        return Category.get_saving_account()
