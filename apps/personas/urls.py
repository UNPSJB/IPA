from django.conf.urls import url

from .views import AltaPersona, ListadoPersonas, AltaDirector, AltaAdministrativo, DetallePersona

app_name = 'personas'


urlpatterns = [

	url(r'^alta_personas$', AltaPersona.as_view(), name='alta_personas'),
	url(r'^listado_personas$', ListadoPersonas.as_view(), name='listado_personas'),
	url(r'^detalle_persona/(?P<pk>.+)/$', DetallePersona.as_view(), name='detalle_persona'),
	url(r'^promover_a_director/(?P<pk>.+)/$', AltaDirector.as_view(), name='promover_a_director'),
	url(r'^promover_a_administrativo/(?P<pk>.+)/$', AltaAdministrativo.as_view(), name='promover_a_administrativo'),
	
]