from django.conf.urls import url

from .views import AltaOposicion, DetalleOposicion, ListadoOpisicion, ModificarOposicion, OposicionDelete

app_name = 'oposicion'

urlpatterns = [

	url(r'^alta$', AltaOposicion.as_view(), name='alta'),
	url(r'^detalle/(?P<pk>.+)/$', DetalleOposicion.as_view(), name='detalle'),
	url(r'^modificar/(?P<pk>.+)/$', ModificarOposicion.as_view(), name='modificar'),
	url(r'^listar$', ListadoOpisicion.as_view(), name='listado'),
	url(r'^eliminar/(?P<pk>.+)/$', OposicionDelete.as_view(), name='delete'),
	
]