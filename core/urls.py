from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.contrib import admin


urlpatterns = [
    re_path(r"^$", RedirectView.as_view(url="/api/v1/", permanent=True)),
    path("api/v1/", include("api.urls", namespace="api")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "api/v1/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
        path('api/v1/admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
