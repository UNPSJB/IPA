from django.conf.urls import url

from .views import ListadoEdictos, AltaEdicto, Detalle_Edicto, EdictoDelete, ModificarEdicto

app_name = 'edictos'

urlpatterns = [

	url(r'^alta_edictos$', AltaEdicto.as_view(), name='alta_edictos'),
	url(r'^detalle_edicto/(?P<pk>.+)/$', Detalle_Edicto.as_view(), name='detalle_edicto'),
	url(r'^modificar_edicto/(?P<pk>.+)/$', ModificarEdicto.as_view(), name='modificar_edicto'),
	url(r'^listar_edicto$', ListadoEdictos.as_view(), name='listar_edicto'),
	url(r'^eliminar/(?P<pk>.+)/$', EdictoDelete.as_view(), name='delete_edicto'),
	
]