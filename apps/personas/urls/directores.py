
from django.conf.urls import url

from ..views.directores import *

app_name = 'directores'

urlpatterns = [
	url(r'^promover/(?P<pk>.+)/$', AltaDirector.as_view(), name='promover'),
	url(r'^listado$', ListadoDirectores.as_view(), name='listado'),
	url(r'^modificar/(?P<pk>.+)/$', ModificarDirector.as_view(), name='modificar'),
	url(r'^eliminar/(?P<pk>.+)/$', EliminarDirector.as_view(), name='eliminar')
]