from rest_framework import serializers

from main.apps.categories.models import Category

from .. import models
from .base_serializers import BaseWithInsitutionPortfolioSerializer


class BankAccountsSerializer(BaseWithInsitutionPortfolioSerializer):
    account_number = serializers.CharField(required=False, allow_blank=True)
    evaluation = serializers.FloatField(required=True)
    income = serializers.IntegerField(required=False, min_value=0, allow_null=True)
    outcome = serializers.IntegerField(required=False, min_value=0, allow_null=True)

    class Meta:
        model = models.BankAccount
        fields = BaseWithInsitutionPortfolioSerializer.Meta.fields + [
            'account_number',
            'evaluation',
            'income',
            'outcome',
        ]
        read_only_fields = BaseWithInsitutionPortfolioSerializer.Meta.read_only_fields

    def get_category(self):
        return Category.get_bank_account()
