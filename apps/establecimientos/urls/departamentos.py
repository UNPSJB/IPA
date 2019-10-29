from django.conf.urls import url

from ..views.departamentos import *

app_name = 'departamentos'
urlpatterns = [
	
	url(r'^listar$', ListadoDepartamentos.as_view(), name='listar'),
	url(r'^detalle/(?P<pk>.+)/$', DetalleDepartamento.as_view(), name='detalle'),

]