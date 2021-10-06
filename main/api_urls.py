from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.apps.users import views as user_views
from main.apps.categories import views as category_views
from main.apps.institutions import views as institution_views
from main.apps.products import views as product_views
from main.apps.portfolio import views as portfolio_views
from main.apps.portfolio_values.views import ListPortfolioValuesByPortfolioView, ListPortfolioValuesByDaysView
from main.libraries.socialview import FacebookLogin, GoogleLogin, AppleLogin

router = DefaultRouter()
router.register('users', user_views.UserViewSets)
router.register('categories', category_views.CategoryViewSet)
router.register('institutions', institution_views.InstitutionViewSet)
router.register('products', product_views.ProductViewSet)
router.register('portfolio/group', portfolio_views.PortfolioGroupByViewSet, basename='portfolio-group')
router.register('portfolio/categories', portfolio_views.PortfolioCategoriesViewSet, basename='portfolio-category')
router.register('portfolio', portfolio_views.PortfolioViewSet)
router.register('bank-accounts', portfolio_views.BankAccountsViewSet, basename='bank-account')
router.register('bonds', portfolio_views.BondsViewSet, basename='bond')
router.register('saving-accounts', portfolio_views.SavingAccountsViewSet, basename='saving-account')
router.register('term-accounts', portfolio_views.TermAccountsViewSet, basename='term-account')
router.register('building-savings', portfolio_views.BuildingSavingsViewSet, basename='building-saving')
router.register('pension-savings', portfolio_views.PensionSavingsViewSet, basename='pension-saving')
router.register('stock', portfolio_views.StocksViewSet, basename='stock')
router.register('cryptos', portfolio_views.CryptosViewSet, basename='crypto')
router.register('commodities', portfolio_views.CommoditiesViewSet, basename='commodity')
router.register('share-etf', portfolio_views.ShareEtfViewSet, basename='share-etf')

urlpatterns = [
    path('', include(router.urls)),
    path('portfolio-values/chart/pie/', ListPortfolioValuesByPortfolioView.as_view(), name='portfolio-chart-pie'),
    path('portfolio-values/chart/line/', ListPortfolioValuesByDaysView.as_view(), name='portfolio-chart-line'),

    path('social/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('social/google/', GoogleLogin.as_view(), name='google_login'),
    path('social/apple/', AppleLogin.as_view(), name='apple_login'),

    path('apple/hook/', AppleLogin.as_view(), name='apple_notification_hook'),  # todo
]
