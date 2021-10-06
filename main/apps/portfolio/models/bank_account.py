from main.apps.categories.models import Category

from .. import managers
from .portfolio import Portfolio


class BankAccount(Portfolio):
    objects = managers.BankAccountsManager.from_queryset(managers.PortfolioQuerySet)()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if self.category is None or self.category != Category.get_bank_account():
            self.category = Category.get_bank_account()
        super(BankAccount, self).save(*args, **kwargs)

    @property
    def account_number(self):
        return self.data.get('account_number')

    @account_number.setter
    def account_number(self, value):
        self.set_data('account_number', value)

    @property
    def income(self):
        return self.data.get('income')

    @income.setter
    def income(self, value):
        self.set_data('income', value)

    @property
    def outcome(self):
        return self.data.get('outcome')

    @outcome.setter
    def outcome(self, value):
        self.set_data('outcome', value)
