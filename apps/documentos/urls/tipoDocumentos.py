from django.conf.urls import url

from ..views import *

app_name = 'tipoDocumentos'
urlpatterns = [
	url(r'^alta$', AltaTipoDocumento.as_view(), name='alta'),
	url(r'^listar$', ListadoTipoDocumentos.as_view(), name='listar'),
	url(r'^modificar/(?P<pk>.+)/$', ModificarTipoDocumento.as_view(), name='modificar'),
	url(r'^detalle/(?P<pk>.+)/$', DetalleTipoDocumento.as_view(), name='detalle'),
	url(r'^eliminar/(?P<pk>\d+)$', DeleteTipoDocumento.as_view(), name='eliminar'),
]