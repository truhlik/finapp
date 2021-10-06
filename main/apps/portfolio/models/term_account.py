import datetime

from .. import managers
from .portfolio import Portfolio
from ...categories.models import Category


class TermAccount(Portfolio):
    objects = managers.TermAccountManager.from_queryset(managers.PortfolioQuerySet)()

    class Meta:
        proxy = True

    @property
    def end_date(self) -> datetime.date:
        return self.data.get('end_date')

    @end_date.setter
    def end_date(self, value: datetime.date):
        self.set_data('end_date', value)

    @property
    def duration(self) -> int:
        return self.data.get('duration')

    @duration.setter
    def duration(self, value: int):
        self.set_data('duration', value)

    def save(self, *args, **kwargs):
        self.category = Category.get_term_account()
        return super(TermAccount, self).save(*args, **kwargs)
