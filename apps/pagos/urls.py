from django.conf.urls import url

from .views import *

app_name = 'pagos'

urlpatterns = [

	url(r'^modulo/alta$', AltaValorDeModulo.as_view(), name='altaModulo'),
	#url(r'^modificar/(?P<pk>.+)/$', ModificarLocalidad.as_view(), name='modificar'),
	url(r'^modulo/modificar/(?P<pk>.+)/$', ModificarValorDeModulo.as_view(), name='modificarModulo'),
	url(r'^modulo/listar$', ListadoValoresDeModulo.as_view(), name='listarModulos'),
	url(r'^modulo/eliminar/(?P<pk>.+)/$', EliminarValorDeModulo.as_view(), name='eliminarModulo'),

	url(r'^cobro/alta/(?P<pk>.+)/$', AltaCobro.as_view(), name='altaCobro'),
	url(r'^cobro/listar/(?P<pk>.+)/$', ListarCobros.as_view(), name='listarCobros'),
	
	url(r'^pago/alta/(?P<pk>.+)/$', AltaPago.as_view(), name='altaPago'),
	url(r'^pago/listar/(?P<pk>.+)/$', ListarPagos.as_view(), name='listarPagos'),

	url(r'^pago/listarcobros/$', ListarTodosLosCobros.as_view(), name='listarTodosLosCobros'),
	url(r'^pago/listarpagos/$', ListarTodosLosPagos.as_view(), name='listarTodosLosPagos'),

	url(r'^cobro/infraccion/alta/(?P<pk>.+)/$', AltaCobroInfraccion.as_view(), name='altaCobroInfraccion'),
	url(r'^pago/infraccion/alta/(?P<pk>.+)/$', AltaPagoInfraccion.as_view(), name='AltaPagoInfraccion'),
]