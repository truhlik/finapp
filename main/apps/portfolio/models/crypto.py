from main.apps.portfolio import managers
from .portfolio import Portfolio
from ...categories.models import Category


class Crypto(Portfolio):
    objects = managers.CryptoManager.from_queryset(managers.PortfolioQuerySet)()

    class Meta:
        proxy = True

    @property
    def income(self):
        return self.data.get('income')

    @income.setter
    def income(self, value):
        self.set_data('income', value)

    @property
    def past_evaluation(self) -> float:
        return self.data.get('past_evaluation')

    @past_evaluation.setter
    def past_evaluation(self, value: float):
        self.set_data('past_evaluation', value)

    def save(self, *args, **kwargs):
        self.category = Category.get_crypto()
        return super(Crypto, self).save(*args, **kwargs)
