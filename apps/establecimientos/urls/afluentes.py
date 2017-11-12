from django.conf.urls import url

from ..views.afluentes import *

app_name = 'afluentes'
urlpatterns = [
	url(r'^alta$', AltaAfluente.as_view(), name='alta'),
	url(r'^detalle/(?P<pk>.+)/$',DetalleAfluente.as_view(), name='detalle'),
	url(r'^modificar/(?P<pk>.+)/$', ModificarAfluente.as_view(), name='modificar'),
	url(r'^listar$', ListadoAfluentes.as_view(), name='listar'),
	url(r'^eliminar/(?P<pk>.+)/$', DeleteAfluente.as_view(), name='eliminar'),
]