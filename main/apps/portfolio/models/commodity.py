import datetime

from main.apps.portfolio import managers
from .portfolio import Portfolio
from ...categories.models import Category


class Commodity(Portfolio):
    objects = managers.CommodityManager.from_queryset(managers.PortfolioQuerySet)()

    class Meta:
        proxy = True

    @property
    def income(self) -> int:
        return self.data.get('income')

    @income.setter
    def income(self, value: int):
        self.set_data('income', value)

    @property
    def buy_price(self) -> float:
        return self.data.get('buy_price')

    @buy_price.setter
    def buy_price(self, value: float):
        self.set_data('buy_price', value)

    @property
    def start_date(self) -> datetime.date:
        return self.data.get('start_date')

    @start_date.setter
    def start_date(self, value: datetime.date):
        self.set_data('start_date', value)

    def save(self, *args, **kwargs):
        self.category = Category.get_commodity()
        return super(Commodity, self).save(*args, **kwargs)
