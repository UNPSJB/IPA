from django.conf.urls import url

from .views import AltaValorDeModulo, ListadoValoresDeModulo, EliminarValorDeModulo, AltaCobro

app_name = 'pagos'

urlpatterns = [

	url(r'^modulo/alta$', AltaValorDeModulo.as_view(), name='altaModulo'),
	url(r'^modulo/listar$', ListadoValoresDeModulo.as_view(), name='listarModulos'),
	url(r'^modulo/eliminar/(?P<pk>.+)/$', EliminarValorDeModulo.as_view(), name='eliminarModulo'),

	url(r'^cobro/alta/(?P<pk>.+)/$', AltaCobro.as_view(), name='altaCobro'),
	

]