from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from core.views import health_check, dashboard_stats, register_user, api_root

# 🔥 Importar vista pública personalizada
from config.public_schema import public_schema

from drf_spectacular.views import (
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", api_root, name="api_root"),
    path("health", health_check),
    path("api/health", health_check),
    path("api/auth/login", TokenObtainPairView.as_view()),
    path("api/auth/refresh", TokenRefreshView.as_view()),
    path("api/auth/register", register_user),
    path("api/", include("apps.events.urls")),
    path("api/", include("apps.tickets.urls")),
    path("api/", include("apps.attendees.urls")),
    path("api/", include("apps.sponsors.urls")),
    path("api/dashboard", dashboard_stats),
    
    # 🔥 Schema público custom
    path("api/schema", public_schema, name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)