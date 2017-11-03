from django.conf.urls import url

from . import views

app_name = 'permisos'
urlpatterns = [
	url(r'^alta$', views.AltaPermiso.as_view(), name='alta'),
	url(r'^listar$', views.ListadoPermisos.as_view(), name='listar'),
	url(r'^detalle/(?P<pk>.+)/$', views.DetallePermiso.as_view(), name='detalle'),
	url(r'^eliminar/(?P<pk>\d+)$', views.PermisoDelete.as_view(), name='delete'),
]