from django.conf.urls import url

from .views import ListadoLocalidades, AltaLocalidad, ModificarLocalidad, Detalle_Localidad, LocalidadDelete

app_name = 'localidades'


urlpatterns = [

	url(r'^alta_localidad$', AltaLocalidad.as_view(), name='alta_localidad'),
	url(r'^listar_localidades$', ListadoLocalidades.as_view(), name='listar_localidades'),
	url(r'^detalle_localidad/(?P<pk>.+)/$', Detalle_Localidad.as_view(), name='detalle_localidad'),
	url(r'^modificar_localidad/(?P<pk>.+)/$', ModificarLocalidad.as_view(), name='modificar_localidad'),
	url(r'^eliminar/(?P<pk>.+)/$', LocalidadDelete.as_view(), name='delete_localidad'),

]