from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from main.apps.core.swagger import path_id_param_int

from .models import Institution
from .serializers import InstitutionSerializer


@method_decorator(name='retrieve', decorator=path_id_param_int)
class InstitutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Institution.objects.active()
    serializer_class = InstitutionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categories', 'products']

