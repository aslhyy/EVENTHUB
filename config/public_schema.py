"""
Vista de schema completamente pública sin ninguna verificación.
"""
from django.http import JsonResponse
from drf_spectacular.generators import SchemaGenerator
from rest_framework.decorators import api_view


@api_view(['GET'])
def public_schema(request):
    """
    Genera y devuelve el schema OpenAPI sin verificaciones de permisos.
    """
    generator = SchemaGenerator()
    schema = generator.get_schema(request=request, public=True)
    return JsonResponse(schema)