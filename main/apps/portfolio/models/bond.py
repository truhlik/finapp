import datetime

from main.apps.portfolio import managers, constants
from .portfolio import Portfolio


class Bond(Portfolio):
    objects = managers.BondsManager.from_queryset(managers.PortfolioQuerySet)()

    class Meta:
        proxy = True

    @property
    def payment_frequency(self):
        return self.data.get('payment_frequency')

    @payment_frequency.setter
    def payment_frequency(self, value):
        self.set_data('payment_frequency', value)

    @property
    def start_date(self) -> datetime.date:
        return self.data.get('start_date')

    @start_date.setter
    def start_date(self, value: datetime.date):
        self.set_data('start_date', value)

    @property
    def end_date(self) -> datetime.date:
        return self.data.get('end_date')

    @end_date.setter
    def end_date(self, value: datetime.date):
        self.set_data('end_date', value)

    def save(self, *args, **kwargs):
        if self.payment_frequency is None:
            self.payment_frequency = constants.PAYMENT_FREQUENCY_YEARLY
        return super(Bond, self).save(*args, **kwargs)
