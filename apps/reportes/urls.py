from django.conf.urls import url

from .views import *
from . import views

app_name = 'reportes'

urlpatterns = [
    url(r'^recaudacion$', Recaudacion.as_view(), name='recaudacion'),
    #url(r'^recaudacion/series_temporales$', RecaudacionTemporal.as_view(), name='recaudacion-series_temporales'),
    #url(r'^recaudacion/valores_modulos$', RecaudacionTemporal.as_view(), name='recaudacion-valores_modulos'),
    url(r'^', DashBoardReportes.as_view(), name='dashboard'),
    
]