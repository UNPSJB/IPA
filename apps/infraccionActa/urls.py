from django.conf.urls import url

from .views import ListadoInfraccionActas, AltaInfraccionActa, DetalleInfraccionActa, DeleteInfraccionActa, ModificarInfraccionActa

app_name = 'infraccionActas'

urlpatterns = [

	url(r'^alta$', AltaInfraccionActa.as_view(), name='alta'),
	url(r'^detalle(?P<pk>.+)/$', DetalleInfraccionActa.as_view(), name='detalle'),
	url(r'^modificar(?P<pk>.+)/$', ModificarInfraccionActa.as_view(), name='modificar'),
	url(r'^listar$', ListadoInfraccionActas.as_view(), name='listar'),
	url(r'^eliminar(?P<pk>.+)/$', DeleteInfraccionActa.as_view(), name='delete'),

	
]