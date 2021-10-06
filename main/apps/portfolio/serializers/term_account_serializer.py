from django.utils import timezone
from rest_framework import serializers
from main.apps.categories.models import Category

from .base_serializers import BaseWithInsitutionPortfolioSerializer
from .. import models


class TermAccountSerializer(BaseWithInsitutionPortfolioSerializer):
    evaluation = serializers.FloatField(required=True)
    end_date = serializers.DateField(required=False, allow_null=True)
    duration = serializers.IntegerField(required=False, min_value=1, allow_null=True)

    class Meta:
        model = models.TermAccount
        fields = BaseWithInsitutionPortfolioSerializer.Meta.fields + [
            'evaluation',
            'end_date',
            'duration',
        ]
        read_only_fields = BaseWithInsitutionPortfolioSerializer.Meta.read_only_fields

    def get_category(self):
        return Category.get_term_account()

    def validate_end_date(self, value):
        if value and value <= timezone.now().date():
            raise serializers.ValidationError('nemůžete zadat datum v minulosti')
        return value
