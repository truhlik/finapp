from typing import Optional

from django.utils import timezone
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from main.apps.core.swagger import portfolio_and_category_param, portfolio_and_category_and_day_param
from . import methods
from .serializers import PieSerializer, LineChartSerializer


class ListPortfolioValuesByDaysView(APIView):
    """
    Vrací hodnoty pro vykreslení liniových grafů.

    Přijímá query parametry:
        - portfolio_id: int -> vrací hodnoty jen pro dané portfolio
        - category_slug: str -> vrací hodnoty jen pro danou kategorii portfolia (bankovní účty)
        - days: int -> kolik dní zpět vrátit hodnoty (pokud je prázdné tak vrať za celou historii)
    """
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(name='list', decorator=portfolio_and_category_and_day_param)
    def get(self, request, *args, **kwargs):

        portfolio_id = self._get_portfolio_id_from_request()
        category_slug = self._get_category_slug_from_request()
        days = self._get_days_from_request() or 365  # nastavuju maximálně rok zpátky

        data = methods.get_portfolio_values_by_days(self.request.user, portfolio_id, category_slug, days)

        # manuálně vložím jednu hodnotu navíc do grafu, aby se to lépe vykreslovalo
        data = list(data)
        if len(data) == 1:
            data.insert(0, {"date": data[0]['date'] - timezone.timedelta(days=1), "sum": 0})

        # spočítám meta data pro graf
        response_data = methods.get_meta_data_for_graph(data)
        response_data["data"] = data
        serializer = LineChartSerializer(response_data)
        return Response(serializer.data)

    def _get_portfolio_id_from_request(self) -> Optional[int]:
        try:
            return int(self.request.query_params.get('portfolio_id'))
        except (ValueError, TypeError):
            return None

    def _get_category_slug_from_request(self) -> Optional[str]:
        return self.request.query_params.get('category_slug')

    def _get_days_from_request(self) -> Optional[int]:
        try:
            return int(self.request.query_params.get('days'))
        except (ValueError, TypeError):
            return None


class ListPortfolioValuesByPortfolioView(APIView):
    """
    Vrací hodnoty pro vykreslení koláčových grafů.

    Přijímá query parametry:
        - portfolio_id: int -> vrací hodnoty jen pro dané portfolio
        - category_slug: str -> vrací hodnoty jen pro danou kategorii portfolia (bankovní účty)
    """
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(name='list', decorator=portfolio_and_category_param)
    def get(self, request, *args, **kwargs):

        portfolio_id = self._get_portfolio_id_from_request()
        category_slug = self._get_category_slug_from_request()

        lst = methods.get_portfolio_values_by_portfolio(self.request.user, portfolio_id, category_slug)
        serializer = PieSerializer({'data': lst})

        return Response(serializer.data)

    def _get_portfolio_id_from_request(self) -> Optional[int]:
        try:
            return int(self.request.query_params.get('portfolio_id'))
        except (ValueError, TypeError):
            return None

    def _get_category_slug_from_request(self) -> Optional[str]:
        try:
            return self.request.query_params.get('category_slug')
        except (ValueError, TypeError):
            return None
