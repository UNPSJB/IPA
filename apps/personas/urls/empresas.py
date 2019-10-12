from django.conf.urls import url
from django.views.generic import TemplateView
from ..views.empresas import AltaEmpresa, DetalleEmpresa, Listado, ModificarEmpresa, EliminarEmpresa, DataEmpresas

app_name = 'empresas'
urlpatterns = [
	url(r'^alta$', AltaEmpresa.as_view(), name='alta'),
	url(r'^detalle/(?P<pk>.+)$', DetalleEmpresa.as_view(), name='detalle'),
	url(r'^listado$', Listado.as_view(), name='listado'),
	url(r'^modificar/(?P<pk>.+)/$', ModificarEmpresa.as_view(), name='modificar'),
	url(r'^eliminar/(?P<pk>.+)/$', EliminarEmpresa.as_view(), name='eliminar'),
	url(r'^data/$', DataEmpresas.as_view(), name='data')
]