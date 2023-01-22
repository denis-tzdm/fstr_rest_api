from .models import AddedMPass
from rest_framework import viewsets

from .serializers import MPassSerializer


class MPassViewset(viewsets.ModelViewSet):
    queryset = AddedMPass.objects.all()
    serializer_class = MPassSerializer
    http_method_names = ['post', ]
