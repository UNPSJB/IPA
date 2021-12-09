from django.conf.urls import url

from .views import *
from . import views

app_name = 'reportes'

urlpatterns = [
    url(r'^recaudacion$', Recaudacion.as_view(), name='recaudacion'),
    url(r'^gestion$', Productividad.as_view(), name='gestion'),
    url(r'^comisiones$', RepComisiones.as_view(), name='comisiones'),
    url(r'^', DashBoardReportes.as_view(), name='dashboard'),
    
]