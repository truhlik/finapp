from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response

from main.apps.core.swagger import path_id_param_int, portfolio_and_category_and_group_by_param, category_param

from . import serializers, models
from ..categories.models import Category
from ..categories.serializers import CategorySerializer


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='list', decorator=category_param)
class PortfolioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Portfolio.objects.active().prefetch()
    serializer_class = serializers.PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_queryset(self):
        return super(PortfolioViewSet, self).get_queryset().for_user(self.request.user)


@method_decorator(name='list', decorator=portfolio_and_category_and_group_by_param)
class PortfolioGroupByViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Portfolio.objects.active().prefetch()
    serializer_class = serializers.AggregateValuesSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category_id', 'id']
    pagination_class = None

    def get_queryset(self):
        qs = super(PortfolioGroupByViewSet, self).get_queryset().for_user(self.request.user)
        if self.group_by_category():
            return qs.group_by_category()
        return qs.group_by_portfolio()

    def group_by_category(self):
        return self.request.query_params.get('group_by', '') == 'category'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class PortfolioCategoriesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return super(PortfolioCategoriesViewSet, self)\
            .get_queryset()\
            .filter(portfolio__owner=self.request.user, portfolio__active=True)\
            .distinct()


class BasePortfolioViewSetMixin(object):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super(BasePortfolioViewSetMixin, self).get_queryset().for_user(self.request.user)


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
@method_decorator(name='destroy', decorator=path_id_param_int)
class BankAccountsViewSet(BasePortfolioViewSetMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = models.BankAccount.objects.active().prefetch()
    serializer_class = serializers.BankAccountsSerializer


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
@method_decorator(name='destroy', decorator=path_id_param_int)
class BondsViewSet(BasePortfolioViewSetMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = models.Bond.objects.active().prefetch()
    serializer_class = serializers.BondsSerializer


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
@method_decorator(name='destroy', decorator=path_id_param_int)
class SavingAccountsViewSet(BasePortfolioViewSetMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    queryset = models.SavingAccount.objects.active().prefetch()
    serializer_class = serializers.SavingAccountSerializer
    permission_classes = [permissions.IsAuthenticated]


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
@method_decorator(name='destroy', decorator=path_id_param_int)
class TermAccountsViewSet(BasePortfolioViewSetMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    queryset = models.TermAccount.objects.active().prefetch()
    serializer_class = serializers.TermAccountSerializer
    permission_classes = [permissions.IsAuthenticated]


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
@method_decorator(name='destroy', decorator=path_id_param_int)
class BuildingSavingsViewSet(BasePortfolioViewSetMixin,
                             mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    queryset = models.BuildingSaving.objects.active().prefetch()
    serializer_class = serializers.BuildingSavingSerializer
    permission_classes = [permissions.IsAuthenticated]


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
@method_decorator(name='destroy', decorator=path_id_param_int)
class PensionSavingsViewSet(BasePortfolioViewSetMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    queryset = models.PensionSaving.objects.active().prefetch()
    serializer_class = serializers.PensionSavingSerializer
    permission_classes = [permissions.IsAuthenticated]


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
@method_decorator(name='destroy', decorator=path_id_param_int)
class StocksViewSet(BasePortfolioViewSetMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = models.Stock.objects.active().prefetch()
    serializer_class = serializers.StocksSerializer
    permission_classes = [permissions.IsAuthenticated]


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
@method_decorator(name='destroy', decorator=path_id_param_int)
class CryptosViewSet(BasePortfolioViewSetMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = models.Crypto.objects.active().prefetch()
    serializer_class = serializers.CryptosSerializer
    permission_classes = [permissions.IsAuthenticated]


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
@method_decorator(name='destroy', decorator=path_id_param_int)
class CommoditiesViewSet(BasePortfolioViewSetMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = models.Commodity.objects.active().prefetch()
    serializer_class = serializers.CommoditySerializer
    permission_classes = [permissions.IsAuthenticated]


@method_decorator(name='retrieve', decorator=path_id_param_int)
@method_decorator(name='update', decorator=path_id_param_int)
@method_decorator(name='partial_update', decorator=path_id_param_int)
@method_decorator(name='destroy', decorator=path_id_param_int)
class ShareEtfViewSet(BasePortfolioViewSetMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = models.ShareEtf.objects.active().prefetch()
    serializer_class = serializers.ShareEtfSerializer
    permission_classes = [permissions.IsAuthenticated]
