
from django.conf.urls import url

from ..views import AltaDirector, ListadoDirectores, DirectorUpdate, DirectorDelete

app_name = 'directores'

urlpatterns = [
	url(r'^promover/(?P<pk>.+)/$', AltaDirector.as_view(), name='promover'),
	url(r'^listado$', ListadoDirectores.as_view(), name='listado'),
	url(r'^modificar/(?P<pk>.+)/$', DirectorUpdate.as_view(), name='modificar'),
	url(r'^eliminar/(?P<pk>.+)/$', DirectorDelete.as_view(), name='eliminar')
]