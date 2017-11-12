from django.conf.urls import url

from ..views.tiposUso import *

app_name = 'tiposDeUso'
urlpatterns = [
	url(r'^alta$', AltaTipoDeUso.as_view(), name='alta'),
	url(r'^listar$', ListadoTiposDeUso.as_view(), name='listar'),
	url(r'^detalle/(?P<pk>.+)/$', DetalleTipoDeUso.as_view(), name='detalle'),
	url(r'^eliminar/(?P<pk>\d+)$', DeleteTipoDeUso.as_view(), name='eliminar'),
]