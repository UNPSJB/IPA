from django.conf.urls import url

from . import views

app_name = 'establecimientos'
urlpatterns = [
	url(r'^altaEstablecimiento$', views.AltaEstablecimiento.as_view(), name='alta'),
	url(r'^listarEstablecimiento$', views.ListadoEstablecimientos.as_view(), name='listar'),

	url(r'^altaAfluente$', views.AltaAfluente.as_view(), name='alta'),
	url(r'^detalleAfluente/(?P<pk>.+)/$', views.DetalleAfluente.as_view(), name='detalle'),
	url(r'^modificarAfluente/(?P<pk>.+)/$', views.ModificarAfluente.as_view(), name='modificar'),
	url(r'^listarAfluente$', views.ListadoAfluentes.as_view(), name='listar'),
	url(r'^eliminarAfluente/(?P<pk>.+)/$', views.AfluenteDelete.as_view(), name='delete'),

	url(r'^altaDepartamento$', views.AltaDepartamento.as_view(), name='alta'),
	url(r'^detalleDepartamento(?P<pk>.+)/$', views.DetalleDepartamento.as_view(), name='detalle'),
	url(r'^modificarDepartamento(?P<pk>.+)/$', views.ModificarDepartamento.as_view(), name='modificar'),
	url(r'^listarDepartamento$', views.ListadoDepartamentos.as_view(), name='listar'),
	url(r'^eliminarDepartamento(?P<pk>.+)/$', views.DeleteDepartamento.as_view(), name='delete'),

	url(r'^altaLocalidad$', views.AltaLocalidad.as_view(), name='alta'),
	url(r'^listarLocalidad$', views.ListadoLocalidades.as_view(), name='listar'),
	url(r'^detalleLocalidad/(?P<pk>.+)/$', views.Detalle_Localidad.as_view(), name='detalle'),
	url(r'^modificarLocalidad/(?P<pk>.+)/$', views.ModificarLocalidad.as_view(), name='modificar'),
	url(r'^eliminarLocalidad/(?P<pk>.+)/$', views.LocalidadDelete.as_view(), name='delete'),
]