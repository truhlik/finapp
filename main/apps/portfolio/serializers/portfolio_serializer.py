from typing import Any, Dict, List

from rest_framework import serializers

from main.apps.categories.serializers import CategorySerializer
from main.apps.currencies.serializer import CurrencySerializer
from main.apps.institutions.serializers import InstitutionSerializer
from main.apps.products.serializers import ProductSerializer

from .. import models
from ...currencies.models import Currency


class PortfolioSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    institution = InstitutionSerializer(allow_null=True)
    product = ProductSerializer(allow_null=True)
    currency = CurrencySerializer()
    value = serializers.IntegerField()
    current_eval = serializers.DecimalField(decimal_places=2, max_digits=10, coerce_to_string=False)

    class Meta:
        model = models.Portfolio
        fields = [
            'id',
            'name',
            'category',
            'institution',
            'product',
            'currency',
            'value',
            'current_eval',
            'ytd_eval',
            'avg_eval',
            'total_eval',
            'weight_eval',
        ]
        read_only_fields = fields

    def save(self):
        # not implemented yet, use specific serializers for create, update
        raise NotImplementedError()


class PortfolioGroupBySerializer(serializers.Serializer):
    portfolio_id = serializers.IntegerField(allow_null=True)
    category = serializers.CharField()
    name = serializers.CharField()
    current_eval = serializers.DecimalField(decimal_places=2, max_digits=10, coerce_to_string=False)
    ytd_eval = serializers.FloatField()
    avg_eval = serializers.FloatField()
    total_eval = serializers.FloatField()
    weight_eval = serializers.FloatField()
    value = serializers.IntegerField()
    currency = serializers.SerializerMethodField()

    def get_currency(self, obj):
        return CurrencySerializer(data={'code': obj['currency_code'], 'name': obj['currency_name']}).initial_data


class AggregateValuesSerializer(serializers.Serializer):
    sum_value = serializers.SerializerMethodField()
    sum_evaluation = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(AggregateValuesSerializer, self).__init__(*args, **kwargs)
        self._sum_value = 0
        self._sum_evaluation = 0
        self.objects = args[0]
        self.calc_values(self.objects)

    def calc_values(self, objects: List[Dict[str, Any]]):
        # chci sečíst hodnoty všech objektů do value
        # musím udělat váhový průměr evaluation
        for i in objects:
            self._sum_value += i.get('value')
            self._sum_evaluation += i.get('current_eval') * i.get('value')

        if self._sum_value == 0:
            return
        else:
            self._sum_evaluation = self._sum_evaluation / self._sum_value

    def get_sum_value(self, obj) -> int:
        return round(self._sum_value)

    def get_sum_evaluation(self, obj) -> float:
        # nasobim 100, zaokrouhluju a delim 100 a delam float, abych dostal 2 desetinna mista
        return round(self._sum_evaluation, 2)

    def get_results(self, obj) -> Dict:
        return PortfolioGroupBySerializer(self.objects, many=True).data

    def get_currency(self, obj):
        return CurrencySerializer(Currency.get_czk()).data
