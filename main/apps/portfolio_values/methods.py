import datetime
from typing import Dict, List, Any

from django.db import models
from django.utils import timezone

from main.apps.portfolio.models import Portfolio
from main.apps.portfolio_values.models import PortfolioValue


def get_portfolio_values_by_days(user=None,
                                 portfolio_id: int = None,
                                 category_slug: str = None,
                                 days: int = None) -> List[Dict[str, Any]]:

    """
    :param user: uživatel pro kterého filtrujeme data
    :param portfolio_id: portfolio ze kterého bereme data
    :param category_slug: kategorie ze které bereme data
    :param days: počet dní zpět, které filtrujeme
    :return: [
          {"date": Date(D.M.Y), "sum": 150},
          {"date": Date(D.M.Y), "sum": 250},
          {"date": Date(D.M.Y), "sum": 300}
    ]
    """

    # todo přepočítávat currency

    qs = PortfolioValue.objects.all()

    if user is not None:
        qs = qs.for_user(user)

    if days is not None:
        qs = qs.filter(date__gte=timezone.now() - timezone.timedelta(days=days))

    if portfolio_id is not None:
        qs = qs.filter(portfolio_id=portfolio_id)
    elif category_slug is not None:
        qs = qs.filter(portfolio__category_id=category_slug)

    qs = qs.values('date') \
        .annotate(sum=models.Sum('value')) \
        .values('date', 'sum') \
        .order_by('date')

    return qs


def get_meta_data_for_graph(data) -> Dict[str, Any]:
    # pokud mám prázdný data, tak vrať jen prázdný meta data
    if len(data) == 0:
        today = timezone.now().date()

        return {
            "min_y": 0,
            "max_y": 100000,
            "min_x": 1,
            "max_x": 6,
            "currency": {
                "code": "CZK",
                "name": "Kč",
            },
            "title_y": [
                {"20000": "20 000 Kč"},
                {"40000": "40 000 Kč"},
                {"60000": "60 000 Kč"},
                {"80000": "80 000 Kč"},
                {"100000": "100 000 Kč"},
            ],
            "title_x": [
                {"1": "{}".format((today - datetime.timedelta(days=305)).strftime("%d %b"))},
                {"2": "{}".format((today - datetime.timedelta(days=244)).strftime("%d %b"))},
                {"3": "{}".format((today - datetime.timedelta(days=183)).strftime("%d %b"))},
                {"4": "{}".format((today - datetime.timedelta(days=122)).strftime("%d %b"))},
                {"5": "{}".format((today - datetime.timedelta(days=61)).strftime("%d %b"))},
                {"6": "{}".format(today.strftime("%d %b"))},
            ],
        }

    # pokud nemám prázdný data, tak generuju hodnoty pro graf
    min_y = data[0]["sum"]
    max_y = data[0]["sum"]
    min_x = data[0]["date"]
    max_x = data[len(data) - 1]["date"]

    # zjistím max a min hodnoty na ose Y
    for item in data:
        if item["sum"] > max_y:
            max_y = item["sum"]
        if item["sum"] < min_y:
            min_y = item["sum"]

    # generuju labels pro osu X
    iter = min(11, len(data))
    td = (max_x - min_x) / (iter - 1) if iter > 1 else datetime.timedelta(days=0)
    title_x = [{str(i): "{}".format((min_x + (td * i)).strftime("%d %b"))} for i in range(0, iter)]

    # generuju labels pro osu Y
    title_y = []
    val = 0
    diff = max_y - min_y if max_y != min_y else max_y
    for i in range(0, 6):
        val = int(min_y + (diff / 5) * i)
        title_y.append({str(val): "{} Kč".format(val)})
    max_y = val  # nastav pro jistotu max na ose y

    meta_data = {
        "min_y": min_y - ((max_y - min_y) / 10),
        "max_y": max_y + ((max_y - min_y) / 10),
        "min_x": 0,
        "max_x": iter,
        "title_y": title_y,
        "title_x": title_x,
        "currency": {
            "code": "CZK",
            "name": "Kč",
        },
    }
    return meta_data


def get_portfolio_values_by_portfolio(user=None,
                                      portfolio_id: int = None,
                                      category_slug: str = None,
                                      date: datetime.date = None) -> List[Dict[str, Any]]:

    qs = Portfolio.objects.all()

    # todo přepočítávat currency

    if user is not None:
        qs = qs.for_user(user)

    if portfolio_id is not None:
        # filtruju jenom jedno portfolio, a nedělám defacto group by podle ničeho
        qs = qs.filter(id=portfolio_id)\
            .values('id')\
            .annotate(
            value=models.Sum('value'),
            title=models.F('name')
        )\
            .values('title', 'value') \
            .order_by('category__order')

    elif category_slug is not None:
        # filtruju na jednu kategorii a dělám group by na portofolia
        qs = qs.filter(category_id=category_slug)\
            .values('id') \
            .annotate(
            value=models.Sum('value'),
            title=models.F('name')
        ) \
            .values('title', 'value') \
            .order_by('category__order')
    else:
        # nedělám filter, ale dělám group by category
        qs = qs.values('category_id') \
            .annotate(
            value=models.Sum('value'),
            title=models.F('category__name')
        ) \
            .values('title', 'value') \
            .order_by('category__order')

    return qs
