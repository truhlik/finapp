from django.db import models
from django.db.models import When
from django.db.models.functions import Cast


class PortfolioQuerySet(models.QuerySet):

    def active(self):
        return self.filter(active=True)

    def bank_accounts(self):
        return self.filter(category__slug='bank-accounts')

    def bonds(self):
        return self.filter(category__slug='bonds')

    def building_savings(self):
        return self.filter(category__slug='building-savings')

    def commodities(self):
        return self.filter(category__slug='commodities')

    def cryptos(self):
        return self.filter(category__slug='cryptos')

    def pension_savings(self):
        return self.filter(category__slug='pension-savings')

    def saving_accounts(self):
        return self.filter(category__slug='saving-accounts')

    def share_etfs(self):
        return self.filter(category__slug='share-etf')

    def stocks(self):
        return self.filter(category__slug='stocks')

    def term_accounts(self):
        return self.filter(category__slug='term-accounts')

    def properties(self):
        return self.filter(category__slug='properties')

    def prefetch(self):
        return self.select_related('category', 'institution', 'product', 'currency')

    def for_user(self, user):
        # if changed, update PortfolioValuesManager.for_user()
        return self.filter(owner=user)

    def group_by_category(self):
        return self.values('category') \
            .annotate(
            val=models.Sum('value'),
            name=models.F('category__name'),
            current_eval=Cast(
                models.Case(
                    When(val=0, then=models.Avg(models.F('current_eval'))),
                    default=models.Sum(models.F('value') * models.F('current_eval')) / models.F('val')),
                output_field=models.DecimalField(decimal_places=2, max_digits=10)
            ),
            ytd_eval=Cast(
                models.Case(
                    When(val=0, then=models.Avg(models.F('ytd_eval'))),
                    default=models.Sum(models.F('value') * models.F('ytd_eval')) / models.F('val')),
                output_field=models.DecimalField(decimal_places=2, max_digits=10)
            ),
            avg_eval=Cast(
                models.Case(
                    When(val=0, then=models.Avg(models.F('avg_eval'))),
                    default=models.Sum(models.F('value') * models.F('avg_eval')) / models.F('val')),
                output_field=models.DecimalField(decimal_places=2, max_digits=10)
            ),
            total_eval=Cast(
                models.Case(
                    When(val=0, then=models.Avg(models.F('total_eval'))),
                    default=models.Sum(models.F('value') * models.F('total_eval')) / models.F('val')),
                output_field=models.DecimalField(decimal_places=2, max_digits=10)
            ),
            weight_eval=Cast(
                models.Case(
                    When(val=0, then=models.Avg(models.F('weight_eval'))),
                    default=models.Sum(models.F('value') * models.F('weight_eval')) / models.F('val')),
                output_field=models.DecimalField(decimal_places=2, max_digits=10)
            ),

            currency_code=models.F('currency__code'),
            currency_name=models.F('currency__name'),
        ) \
            .values('category',
                    'name',
                    'current_eval',
                    'ytd_eval',
                    'avg_eval',
                    'total_eval',
                    'weight_eval',
                    'currency_code',
                    'currency_name',
                    value=models.F('val'),
                    ) \
            .order_by()

    def group_by_portfolio(self):
        return self.values('id') \
            .annotate(
            portfolio_id=models.F('id'),
            category=models.F('category__slug'),
            val=models.Sum('value'),
            name=models.F('name'),
            current_eval=Cast(
                models.Case(
                    When(val=0, then=models.Avg(models.F('current_eval'))),
                    default=models.Sum(models.F('value') * models.F('current_eval')) / models.F('val')),
                output_field=models.DecimalField(decimal_places=2, max_digits=10)
            ),
            ytd_eval=Cast(
                models.Case(
                    When(val=0, then=models.Avg(models.F('ytd_eval'))),
                    default=models.Sum(models.F('value') * models.F('ytd_eval')) / models.F('val')),
                output_field=models.DecimalField(decimal_places=2, max_digits=10)
            ),
            avg_eval=Cast(
                models.Case(
                    When(val=0, then=models.Avg(models.F('avg_eval'))),
                    default=models.Sum(models.F('value') * models.F('avg_eval')) / models.F('val')),
                output_field=models.DecimalField(decimal_places=2, max_digits=10)
            ),
            total_eval=Cast(
                models.Case(
                    When(val=0, then=models.Avg(models.F('total_eval'))),
                    default=models.Sum(models.F('value') * models.F('total_eval')) / models.F('val')),
                output_field=models.DecimalField(decimal_places=2, max_digits=10)
            ),
            weight_eval=Cast(
                models.Case(
                    When(val=0, then=models.Avg(models.F('weight_eval'))),
                    default=models.Sum(models.F('value') * models.F('weight_eval')) / models.F('val')),
                output_field=models.DecimalField(decimal_places=2, max_digits=10)
            ),
            currency_code=models.F('currency__code'),
            currency_name=models.F('currency__name'),
        ).values(
            'portfolio_id',
            'category',
            'name',
            'current_eval',
            'ytd_eval',
            'avg_eval',
            'total_eval',
            'weight_eval',
            'currency_code',
            'currency_name',
            value=models.F('val'),
        ).order_by('category__order')


class BankAccountsManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(category__slug='bank-accounts')


class BondsManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(category__slug='bonds')


class SavingAccountManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(category__slug='saving-accounts')


class TermAccountManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(category__slug='term-accounts')


class BuildingSavingManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(category__slug='building-savings')


class PensionSavingManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(category__slug='pension-savings')


class StockManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(category__slug='stocks')


class CryptoManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(category__slug='cryptos')


class CommodityManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(category__slug='commodities')


class ShareEtfManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(category__slug='share-etf')
