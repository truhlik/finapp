from django.db import models


class CustomObjectQueryset(models.QuerySet):

    def active(self):
        return self.filter(trash=False)
