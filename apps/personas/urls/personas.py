from django.conf.urls import url

from ..views import AltaPersona, ListadoPersonas, DetallePersona, ModificarPersona

app_name = 'personas'
urlpatterns = [
	url(r'^alta$', AltaPersona.as_view(), name='alta'),
	url(r'^listado$', ListadoPersonas.as_view(), name='listado'),
	url(r'^detalle/(?P<pk>.+)/$', DetallePersona.as_view(), name='detalle'),
	url(r'^modificar/(?P<pk>.+)/$', ModificarPersona.as_view(), name='modificar'),
]