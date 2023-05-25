from django.urls import include, path, re_path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from hasker.api.api_accounts.views import CustomAuthToken
from config import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from hasker.api.api_accounts.views import CustomAuthToken


schema_view = get_schema_view(
    openapi.Info(
      title="EXAMPLE API",
      default_version='v1',
      description="REST API Documentation",
      contact=openapi.Contact(email="example@example.com"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('settings/', include('hasker.accounts.urls')),
    path('auth/', include('hasker.accounts.urls')),
    path('', include('hasker.questions.urls')),
    path('answers/', include('hasker.answers.urls')),
    path('api/', include('hasker.api.polls.urls')),
    path('api/api-token-auth/', CustomAuthToken.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
