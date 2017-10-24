from django.conf.urls import url

from . import views

app_name = 'tipoDocumentacion'
urlpatterns = [
	url(r'^alta$', views.AltaTipoDocumentacion.as_view(), name='alta'),
	url(r'^listar$', views.ListadoTipoDocumentacion.as_view(), name='listado'),
	url(r'^modificar/(?P<pk>.+)/$', views.ModificarTipoDocumentacion.as_view(), name='modificar'),
	url(r'^detalle/(?P<pk>.+)/$', views.DetalleTipoDocumentacion.as_view(), name='detalle'),
	url(r'^eliminar/(?P<pk>\d+)$', views.TipoDocumentacionDelete.as_view(), name='delete'),
]