from typing import List, Dict, Any

from rest_framework import serializers

from main.apps.currencies.models import Currency
from main.apps.currencies.serializer import CurrencySerializer


class PieDataSerializer(serializers.Serializer):
    """
    [
                {
                    'title': portfolio1.name,
                    'value': 10,  # procenta
                    'data': 10000  # hodnota
                },
                {
                    'title': portfolio2.name,
                    'value': 90,
                    'data': 90000  # hodnota
                },

            ]
    """
    title = serializers.CharField(read_only=True)
    value = serializers.SerializerMethodField()
    data = serializers.IntegerField(source='value')

    def __init__(self, *args, **kwargs):
        super(PieDataSerializer, self).__init__(*args, **kwargs)
        self._sum_value = 0
        self.objects = args[0]
        self.calc_values(self.objects)

    def calc_values(self, objects: List[Dict[str, Any]]):
        # chci sečíst hodnoty všech objektů do value
        # musím udělat váhový průměr evaluation
        for i in objects:
            self._sum_value += i.get('value')

    def get_value(self, obj):
        """ Vrací hodnotu v procentech. """
        if self._sum_value == 0:
            return 0.00

        return round(obj['value'] * 100 / self._sum_value, 2)


class PieSerializer(serializers.Serializer):
    currency = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    def get_currency(self, obj):
        return CurrencySerializer(Currency.get_czk()).data  # todo default Currency

    def get_data(self, obj):
        return PieDataSerializer(obj['data'], many=True).data


class DataLineChartSerializer(serializers.Serializer):
    date = serializers.DateField()
    sum = serializers.IntegerField()


class LineChartSerializer(serializers.Serializer):
    min_y = serializers.IntegerField()
    max_y = serializers.IntegerField()
    min_x = serializers.IntegerField()
    max_x = serializers.IntegerField()
    title_y = serializers.JSONField()
    title_x = serializers.JSONField()
    currency = CurrencySerializer()
    data = DataLineChartSerializer(many=True)
