from django.contrib import admin
from django.urls import path

from mpass.views import MPassViewset

mpass_list = MPassViewset.as_view({
    'post': 'create',
})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('submitData', mpass_list, name='mpass-list'),
]
