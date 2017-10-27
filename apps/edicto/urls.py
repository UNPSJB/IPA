from django.conf.urls import url

from .views import ListadoEdictos, AltaEdicto, Detalle_Edicto, EdictoDelete, ModificarEdicto

app_name = 'edictos'

urlpatterns = [

	url(r'^alta$', AltaEdicto.as_view(), name='alta'),
	url(r'^detalle/(?P<pk>.+)/$', Detalle_Edicto.as_view(), name='detalle'),
	url(r'^modificar/(?P<pk>.+)/$', ModificarEdicto.as_view(), name='modificar'),
	url(r'^listar$', ListadoEdictos.as_view(), name='listar'),
	url(r'^eliminar/(?P<pk>.+)/$', EdictoDelete.as_view(), name='delete'),
	
]