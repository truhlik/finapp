from django.db import models

from main.apps.portfolio_values.managers import PortfolioValuesManager


class PortfolioValue(models.Model):
    objects = PortfolioValuesManager.as_manager()

    portfolio = models.ForeignKey('portfolio.Portfolio', on_delete=models.CASCADE, related_name='portfolio_values')
    date = models.DateField()
    value = models.DecimalField(decimal_places=12, max_digits=27)

    class Meta:
        verbose_name = 'hodnota portfolia'
        verbose_name_plural = 'hodnoty portfolia'
        unique_together = ('portfolio', 'date')

    def __str__(self):
        return "{0} - {1}".format(self.portfolio.name, self.date)
