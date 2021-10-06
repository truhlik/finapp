from django.db import models


class ProductQuerySet(models.QuerySet):

    def prefetch_currency(self):
        return self.prefetch_related('currencies')

    def active(self):
        return self.filter(active=True)
