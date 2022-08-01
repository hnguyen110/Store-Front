import logging

import requests
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.request import Request
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class HelloView(APIView):
    @method_decorator(cache_page(60 * 10))
    def get(self, request: Request):
        try:
            logger.info('CALLING HTTPBIN')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('RECEIVED THE RESPONSE')
            data = response.json()
            return HttpResponse(data)
        except request.ConnectionError:
            logger.critical('HTTPBIN SERVER OFFLINE')
