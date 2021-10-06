from django.db import models


class PortfolioValuesManager(models.QuerySet):

    def for_user(self, user):
        return self.filter(portfolio__owner=user)
