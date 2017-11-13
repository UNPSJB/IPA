from django.conf.urls import url

from ..views.establecimientos import *

app_name = 'establecimientos'
urlpatterns = [
	url(r'^alta$', AltaEstablecimiento.as_view(), name='alta'),
	url(r'^listar$', ListadoEstablecimientos.as_view(), name='listar'),
	url(r'^detalle/(?P<pk>.+)/$', DetalleEstablecimiento.as_view(), name='detalle'),
	url(r'^eliminar/(?P<pk>.+)$', DeleteEstablecimiento.as_view(), name='eliminar'),
]