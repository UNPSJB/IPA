from django.conf.urls import url

from ..views.permisos import *

app_name = 'permisos'
urlpatterns = [
	url(r'^alta$', AltaPermiso.as_view(), name='alta'),
	url(r'^listar$', ListadoPermisos.as_view(), name='listar'),
	url(r'^detalle/(?P<pk>.+)/$', DetallePermiso.as_view(), name='detalle'),
	url(r'^eliminar/(?P<pk>\d+)$', PermisoDelete.as_view(), name='delete'),
]