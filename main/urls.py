from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.contrib import admin
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view_ya = get_schema_view(
   openapi.Info(
      title="FINAPP API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
sitemaps_dict = {

}

urlpatterns = [
    # tyhle view handluje front a jsou zde jen dummy pro reverse url
    # path('app/#/auth/login/', TemplateView.as_view(template_name='frontend.html'), name='login'),
    # path('app/#/auth/new-password/', TemplateView.as_view(template_name='frontend.html'), name='frontend_password_reset'),
    # path('app/#/password/reset/confirm/<str:uidb64>/<str:token>/', TemplateView.as_view(template_name='frontend.html'), name='password_reset_confirm'),

    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='frontend_password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # tady už jsou backend URL
    path('api/v1/', include('main.api_urls')),
    path('api/v1/accounts/', include('main.accounts_urls')),
    url(r'api/v1/accounts/account-confirm-email/(?P<key>[-:\w]+)/$',
        TemplateView.as_view(template_name='account/email/email_confirmation_signup_message.html'),
        name='account_confirm_email'),
    path('api/v1/accounts/', include('dj_rest_auth.registration.urls')),

    # yet another swagger gen
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_ya.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view_ya.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('admin/', admin.site.urls),
]


if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
