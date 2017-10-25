from django.conf.urls import url

from .views import AltaReclamo, DetalleReclamo, ListadoReclamo, ModificarReclamo, ReclamoDelete

app_name = 'reclamo'

urlpatterns = [

	url(r'^alta$', AltaReclamo.as_view(), name='alta'),
	url(r'^detalle/(?P<pk>.+)/$', DetalleReclamo.as_view(), name='detalle'),
	url(r'^modificar/(?P<pk>.+)/$', ModificarReclamo.as_view(), name='modificar'),
	url(r'^listar$', ListadoReclamo.as_view(), name='listar'),
	url(r'^eliminar/(?P<pk>.+)/$', ReclamoDelete.as_view(), name='delete'),
	
]