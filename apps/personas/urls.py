from django.conf.urls import url

from .views import AltaPersona, ListadoPersonas, AltaDirector, AltaAdministrativo, DetallePersona

app_name = 'personas'


urlpatterns = [

	url(r'^alta$', AltaPersona.as_view(), name='alta'),
	url(r'^listado$', ListadoPersonas.as_view(), name='listado'),
	url(r'^detalle/(?P<pk>.+)/$', DetallePersona.as_view(), name='detalle'),
	url(r'^promover_a_director/(?P<pk>.+)/$', AltaDirector.as_view(), name='promover_a_director'),
	url(r'^promover_a_administrativo/(?P<pk>.+)/$', AltaAdministrativo.as_view(), name='promover_a_administrativo'),
	
]