from rest_framework import serializers
from main.apps.categories.models import Category

from .base_serializers import BaseWithInsitutionPortfolioSerializer
from .. import models, constants


class BuildingSavingSerializer(BaseWithInsitutionPortfolioSerializer):
    evaluation = serializers.FloatField(required=True)
    start_date = serializers.DateField(required=False, allow_null=True)
    final_sum = serializers.IntegerField(required=False, min_value=10000, allow_null=True)
    initial_sum = serializers.IntegerField(required=False, min_value=0, allow_null=True)
    payment_frequency = serializers.ChoiceField(required=True, choices=constants.BUILDING_SAVING_PAYMENT_FREQUENCY_CHOICES)
    income = serializers.IntegerField(required=True, min_value=0, allow_null=True)

    class Meta:
        model = models.BuildingSaving
        fields = BaseWithInsitutionPortfolioSerializer.Meta.fields + [
            'payment_frequency',
            'income',
            'evaluation',
            'start_date',
            'final_sum',
            'initial_sum',
        ]
        read_only_fields = BaseWithInsitutionPortfolioSerializer.Meta.read_only_fields

    def get_category(self):
        return Category.get_building_saving()

    def validate(self, attrs):
        super(BuildingSavingSerializer, self).validate(attrs)
        initial_sum = attrs.get('initial_sum')
        final_sum = attrs.get('final_sum')
        if initial_sum and final_sum and initial_sum > final_sum:
            raise serializers.ValidationError({
                'initial_sum': 'Počáteční vklad nemůže být větší než cílová částka.',
                'final_sum': 'Počáteční vklad nemůže být větší než cílová částka.',
            })
        return attrs
