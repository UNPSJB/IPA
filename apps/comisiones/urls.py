from django.conf.urls import url

from .views import ListadoComision, AltaComision, ModificarComision, DetalleComision, DeleteComision

app_name = 'comisiones'


urlpatterns = [

	url(r'^alta$', AltaComision.as_view(), name='alta'),
	url(r'^listar$', ListadoComision.as_view(), name='listar'),
	url(r'^detalle/(?P<pk>.+)/$', DetalleComision.as_view(), name='detalle'),
	url(r'^modificar/(?P<pk>.+)/$', ModificarComision.as_view(), name='modificar'),
	url(r'^eliminar/(?P<pk>.+)/$', DeleteComision.as_view(), name='eliminar'),

]