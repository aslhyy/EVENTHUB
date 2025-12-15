"""
Override para forzar que Spectacular sea público.
"""
from drf_spectacular.views import SpectacularAPIView as BaseSpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView as BaseSpectacularSwaggerView
from drf_spectacular.views import SpectacularRedocView as BaseSpectacularRedocView


class SpectacularAPIView(BaseSpectacularAPIView):
    permission_classes = []
    authentication_classes = []
    
    def check_permissions(self, request):
        # No verificar permisos
        pass
    
    def check_throttles(self, request):
        # No verificar throttles
        pass


class SpectacularSwaggerView(BaseSpectacularSwaggerView):
    permission_classes = []
    authentication_classes = []
    
    def check_permissions(self, request):
        pass
    
    def check_throttles(self, request):
        pass


class SpectacularRedocView(BaseSpectacularRedocView):
    permission_classes = []
    authentication_classes = []
    
    def check_permissions(self, request):
        pass
    
    def check_throttles(self, request):
        pass