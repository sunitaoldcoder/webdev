"""Serve the built PWA and API from one origin; never expose private media."""
from django.conf import settings
from django.http import FileResponse, JsonResponse, HttpResponse
from django.views.decorators.cache import never_cache
@never_cache
def index(request):
    file=settings.PWA_ROOT/'index.html'
    if not file.exists():
        return HttpResponse('Build the frontend first: npm --prefix frontend run build',status=503)
    return FileResponse(file.open('rb'),content_type='text/html; charset=utf-8')
def health(request):
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        return JsonResponse({'status':'ok'})
    except Exception:
        return JsonResponse({'status':'unavailable'},status=503)
