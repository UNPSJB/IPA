from django.conf.urls import url

from .views import AltaAModulo, DetalleModulo, ListadoModulo, ModificarModulo, DeleteModulo

app_name = 'modulo'

urlpatterns = [

	url(r'^alta$', AltaAModulo.as_view(), name='alta'),
	url(r'^detalle/(?P<pk>.+)/$', DetalleModulo.as_view(), name='detalle'),
	url(r'^listar$', ListadoModulo.as_view(), name='listar'),
	url(r'^modificar/(?P<pk>.+)/$', ModificarModulo.as_view(), name='modificar'),
	url(r'^eliminar/(?P<pk>.+)/$', DeleteModulo.as_view(), name='delete'),
	
]