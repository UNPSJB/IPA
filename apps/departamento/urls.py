from django.conf.urls import url

from .views import ListadoDepartamentos, AltaDepartamento, DetalleDepartamento, DeleteDepartamento, ModificarDepartamento

app_name = 'departamentos'

urlpatterns = [
	#url(r'^$', views.listar_tiposDocumentacion, name='index_afluente'),
	url(r'^alta$', AltaDepartamento.as_view(), name='alta'),
	url(r'^detalle(?P<pk>.+)/$', DetalleDepartamento.as_view(), name='detalle'),
	url(r'^modificar(?P<pk>.+)/$', ModificarDepartamento.as_view(), name='modificar'),
	url(r'^listar$', ListadoDepartamentos.as_view(), name='listar'),
	url(r'^eliminar(?P<pk>.+)/$', DeleteDepartamento.as_view(), name='delete'),
	#url(r'^listar_afluentes$', listar_afluentes, name='listar_afluentes'),
	
]