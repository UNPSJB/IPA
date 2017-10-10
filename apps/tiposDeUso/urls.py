from django.conf.urls import url

from . import views

app_name = 'tiposDeUso'
urlpatterns = [
	url(r'^alta$', views.AltaTipoDeUso.as_view(), name='alta'),
	url(r'^listar$', views.ListadoTiposDeUso.as_view(), name='listado'),
	url(r'^detalle/(?P<pk>.+)/$', views.DetalleTipoDeUso.as_view(), name='detalle'),
	url(r'^eliminar/(?P<pk>\d+)$', views.TipoDeUsoDelete.as_view(), name='delete'),
]