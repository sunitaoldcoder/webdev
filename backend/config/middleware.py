"""Log timing and status only; never profile, question, token or image contents."""
import logging
from time import monotonic
logger=logging.getLogger('api')
class APILogMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        start=monotonic()
        response=self.get_response(request)
        if request.path.startswith('/api/'):
            logger.info('%s %s status=%d elapsed_ms=%.1f',request.method,request.path,response.status_code,(monotonic()-start)*1000)
        return response
