from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse


@require_http_methods(['POST', 'GET'])
def root(request):
    data = {
        "status": 1,
        "message": "Page Not Allowed",
        "data": {}
    }
    return HttpResponse(status=404)
