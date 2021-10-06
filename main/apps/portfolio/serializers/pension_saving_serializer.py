from rest_framework import serializers
from main.apps.categories.models import Category

from .base_serializers import BaseWithInsitutionPortfolioSerializer
from .. import models, constants


class PensionSavingSerializer(BaseWithInsitutionPortfolioSerializer):
    evaluation = serializers.FloatField(required=True)
    start_date = serializers.DateField(required=False, allow_null=True)
    initial_sum = serializers.IntegerField(required=False, min_value=0, allow_null=True)
    saving_form = serializers.ChoiceField(required=False, choices=constants.PENSION_SAVING_FORM_CHOICES, allow_blank=True)
    saving_strategy = serializers.ChoiceField(required=False, choices=constants.PENSION_SAVING_STRATEGY_CHOICES, allow_blank=True)
    income = serializers.IntegerField(required=True, min_value=0)
    income_employer = serializers.IntegerField(required=True, min_value=0)

    class Meta:
        model = models.PensionSaving
        fields = BaseWithInsitutionPortfolioSerializer.Meta.fields + [
            'evaluation',
            'start_date',
            'initial_sum',
            'saving_form',
            'saving_strategy',
            'income',
            'income_employer',
        ]
        read_only_fields = BaseWithInsitutionPortfolioSerializer.Meta.read_only_fields

    def get_category(self):
        return Category.get_pension_saving()

