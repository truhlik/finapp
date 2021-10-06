from main.apps.portfolio import managers
from .portfolio import Portfolio
from ...categories.models import Category


class Stock(Portfolio):
    objects = managers.StockManager.from_queryset(managers.PortfolioQuerySet)()

    class Meta:
        proxy = True

    @property
    def past_evaluation(self) -> float:
        return self.data.get('past_evaluation')

    @past_evaluation.setter
    def past_evaluation(self, value: float):
        self.set_data('past_evaluation', value)

    def save(self, *args, **kwargs):
        self.category = Category.get_stock()
        return super(Stock, self).save(*args, **kwargs)
