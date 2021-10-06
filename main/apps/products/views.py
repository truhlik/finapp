from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter

from main.apps.core.swagger import path_id_param_int

from .models import Product
from .serializers import ProductSerializer


@method_decorator(name='retrieve', decorator=path_id_param_int)
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.active().prefetch_currency()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'institutions']
    search_fields = ['name']
