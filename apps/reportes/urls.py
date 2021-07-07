from django.conf.urls import url

from .views import *
from . import views

app_name = 'reportes'

urlpatterns = [
    url(r'^reportes$', DashBoardReportes.as_view(), name='dashboard'),
    url(r'^recaudacion$', RecaudacionTipoPermiso.as_view(), name='recaudacion'),
]