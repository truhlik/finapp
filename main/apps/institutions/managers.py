from django.db import models


class InstitutionQuerySet(models.QuerySet):

    def active(self):
        return self.filter(active=True)
