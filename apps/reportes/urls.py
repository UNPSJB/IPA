from django.conf.urls import url

from .views import *
from . import views

app_name = 'reportes'

urlpatterns = [
    url(r'^ingresos$', IngresoTipoPermiso.as_view(), name='ingresos'),
]