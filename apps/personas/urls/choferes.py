
from django.conf.urls import url

from ..views.choferes import *

app_name = 'choferes'

urlpatterns = [
	url(r'^promover/(?P<pk>.+)/$', AltaChofer.as_view(), name='promover'),
	url(r'^listado$', ListadoChoferes.as_view(), name='listado'),
	url(r'^modificar/(?P<pk>.+)/$', ModificarChofer.as_view(), name='modificar'),
	url(r'^eliminar/(?P<pk>.+)/$', EliminarChofer.as_view(), name='eliminar')

]