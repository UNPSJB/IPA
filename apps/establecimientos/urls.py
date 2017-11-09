from django.conf.urls import url

from . import views

app_name = 'establecimientos'
urlpatterns = [
	url(r'^altaEstablecimiento$', views.AltaEstablecimiento.as_view(), name='altaEstablecimiento'),
	url(r'^listarEstablecimiento$', views.ListadoEstablecimientos.as_view(), name='listarEstablecimiento'),

	url(r'^altaAfluente$', views.AltaAfluente.as_view(), name='altaAfluente'),
	url(r'^detalleAfluente/(?P<pk>.+)/$', views.DetalleAfluente.as_view(), name='detalleAfluente'),
	url(r'^modificarAfluente/(?P<pk>.+)/$', views.ModificarAfluente.as_view(), name='modificarAfluente'),
	url(r'^listarAfluente$', views.ListadoAfluentes.as_view(), name='listarAfluente'),
	url(r'^eliminarAfluente/(?P<pk>.+)/$', views.AfluenteDelete.as_view(), name='deleteAfluente'),

	url(r'^altaDepartamento$', views.AltaDepartamento.as_view(), name='altaDepartamento'),
	url(r'^detalleDepartamento(?P<pk>.+)/$', views.DetalleDepartamento.as_view(), name='detalleDepartamento'),
	url(r'^modificarDepartamento(?P<pk>.+)/$', views.ModificarDepartamento.as_view(), name='modificarDepartamento'),
	url(r'^listarDepartamento$', views.ListadoDepartamentos.as_view(), name='listarDepartamento'),
	url(r'^eliminarDepartamento(?P<pk>.+)/$', views.DeleteDepartamento.as_view(), name='deleteDepartamento'),

	url(r'^altaLocalidad$', views.AltaLocalidad.as_view(), name='altaLocalidad'),
	url(r'^listarLocalidad$', views.ListadoLocalidades.as_view(), name='listarLocalidad'),
	url(r'^detalleLocalidad/(?P<pk>.+)/$', views.Detalle_Localidad.as_view(), name='detalleLocalidad'),
	url(r'^modificarLocalidad/(?P<pk>.+)/$', views.ModificarLocalidad.as_view(), name='modificarLocalidad'),
	url(r'^eliminarLocalidad/(?P<pk>.+)/$', views.LocalidadDelete.as_view(), name='eliminarLocalidad'),
]