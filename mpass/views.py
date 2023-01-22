from rest_framework import viewsets
from rest_framework.views import exception_handler

from .models import AddedMPass
from .serializers import MPassSerializer


class MPassViewset(viewsets.ModelViewSet):
    queryset = AddedMPass.objects.all()
    serializer_class = MPassSerializer
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        response = super(MPassViewset, self).create(request, *args, **kwargs)
        if response.status_code == 201:
            response.status_code = 200
        response_data = {
            'status': response.status_code,
            'message': response.status_text,
            'id': response.data['id'] if response.status_code == 200 else None,
        }
        response.data = response_data
        response.content_type = 'application/json'
        return response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        rd = response.data
        response.data = {
            'status': response.status_code,
            'message': rd,
            'id': None,
        }
        response.content_type = 'application/json'

    return response
