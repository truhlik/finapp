from django.utils.decorators import method_decorator
from rest_framework import viewsets

from main.apps.core.swagger import path_slug_param_str

from .models import Category
from .serializers import CategorySerializer


@method_decorator(name='retrieve', decorator=path_slug_param_str)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by('order')
    serializer_class = CategorySerializer
