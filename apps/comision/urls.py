from django.conf.urls import url

from .views import ListadoComision, AltaComision, ModificarComision, DetalleComision, DeleteComision

app_name = 'comisiones'


urlpatterns = [

	url(r'^altaComision$', AltaComision.as_view(), name='alta'),
	url(r'^listarComision$', ListadoComision.as_view(), name='listar'),
	url(r'^detalleComision/(?P<pk>.+)/$', DetalleComision.as_view(), name='detalle'),
	url(r'^modificarComision/(?P<pk>.+)/$', ModificarComision.as_view(), name='modificar'),
	url(r'^eliminarComision/(?P<pk>.+)/$', DeleteComision.as_view(), name='eliminar'),

]