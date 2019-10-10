from django.conf.urls import url

from ..views.localidades import *

app_name = 'localidades'
urlpatterns = [
	url(r'^alta$', AltaLocalidad.as_view(), name='alta'),
	url(r'^listar$', ListadoLocalidades.as_view(), name='listar'),
	url(r'^detalle/(?P<pk>.+)/$', DetalleLocalidad.as_view(), name='detalle'),
	url(r'^modificar/(?P<pk>.+)/$', ModificarLocalidad.as_view(), name='modificar'),
	url(r'^eliminar/(?P<pk>.+)/$', LocalidadDelete.as_view(), name='eliminar'),
	]


