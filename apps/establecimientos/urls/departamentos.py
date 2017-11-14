from django.conf.urls import url

from ..views.departamentos import *

app_name = 'departamentos'
urlpatterns = [
	url(r'^alta$', AltaDepartamento.as_view(), name='alta'),
	url(r'^listar$', ListadoDepartamentos.as_view(), name='listar'),
	url(r'^detalle/(?P<pk>.+)/$', DetalleDepartamento.as_view(), name='detalle'),
	url(r'^eliminar/(?P<pk>\d+)$', DeleteDepartamento.as_view(), name='eliminar'),
	url(r'^modificar/(?P<pk>\d+)$', ModificarDepartamento.as_view(), name='modificar'),

]