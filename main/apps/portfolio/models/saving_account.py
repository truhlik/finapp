from main.apps.portfolio import managers, constants
from .portfolio import Portfolio
from ...categories.models import Category


class SavingAccount(Portfolio):
    objects = managers.SavingAccountManager.from_queryset(managers.PortfolioQuerySet)()

    class Meta:
        proxy = True

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
        if self.payment_frequency is None:
            self.payment_frequency = constants.PAYMENT_FREQUENCY_YEARLY
        self.category = Category.get_saving_account()
        return super(SavingAccount, self).save(*args, **kwargs)
