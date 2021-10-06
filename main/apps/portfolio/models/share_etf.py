import datetime

from .. import managers
from .portfolio import Portfolio
from ...categories.models import Category


class ShareEtf(Portfolio):
    objects = managers.ShareEtfManager.from_queryset(managers.PortfolioQuerySet)()

    class Meta:
        proxy = True

    @property
    def start_date(self) -> datetime.date:
        return self.data.get('start_date')

    @start_date.setter
    def start_date(self, value: datetime.date):
        self.set_data('start_date', value)

    @property
    def initial_sum(self) -> int:
        return self.data.get('initial_sum')

    @initial_sum.setter
    def initial_sum(self, value: int):
        self.set_data('initial_sum', value)

    @property
    def actual_sum(self) -> int:
        return self.data.get('actual_sum')

    @initial_sum.setter
    def actual_sum(self, value: int):
        self.set_data('actual_sum', value)

    @property
    def saving_strategy(self) -> str:
        return self.data.get('saving_strategy')

    @saving_strategy.setter
    def saving_strategy(self, value: str):
        self.set_data('saving_strategy', value)

    @property
    def income(self) -> int:
        return self.data.get('income')

    @income.setter
    def income(self, value: int):
        self.set_data('income', value)

    def save(self, *args, **kwargs):
        self.category = Category.get_share_etf()
        return super(ShareEtf, self).save(*args, **kwargs)
