from django.conf.urls import url

from ..views.localidades import *

app_name = 'localidades'
urlpatterns = [

	url(r'^listar$', ListadoLocalidades.as_view(), name='listar'),
	url(r'^detalle/(?P<pk>.+)/$', DetalleLocalidad.as_view(), name='detalle'),
]


