import datetime

from .. import managers
from .portfolio import Portfolio
from ...categories.models import Category


class BuildingSaving(Portfolio):
    objects = managers.BuildingSavingManager.from_queryset(managers.PortfolioQuerySet)()

    class Meta:
        proxy = True

    @property
    def start_date(self) -> datetime.date:
        return self.data.get('start_date')

    @start_date.setter
    def start_date(self, value: datetime.date):
        self.set_data('start_date', value)

    @property
    def final_sum(self) -> int:
        return self.data.get('final_sum')

    @final_sum.setter
    def final_sum(self, value: int):
        self.set_data('final_sum', value)

    @property
    def initial_sum(self) -> int:
        return self.data.get('initial_sum')

    @initial_sum.setter
    def initial_sum(self, value: int):
        self.set_data('initial_sum', value)

    @property
    def payment_frequency(self):
        return self.data.get('payment_frequency')

    @payment_frequency.setter
    def payment_frequency(self, value):
        self.set_data('payment_frequency', value)

    @property
    def income(self):
        return self.data.get('income')

    @income.setter
    def income(self, value):
        self.set_data('income', value)

    def save(self, *args, **kwargs):
        self.category = Category.get_building_saving()
        return super(BuildingSaving, self).save(*args, **kwargs)
