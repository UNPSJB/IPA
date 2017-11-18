from django.conf.urls import url

from ..views.permisos import *

app_name = 'permisos'
urlpatterns = [
	url(r'^listar$', ListadoPermisos.as_view(), name='listar'),
	#url(r'^detalle/(?P<pk>.+)/$', DetallePermiso.as_view(), name='detalle'),
	url(r'^eliminar/(?P<pk>\d+)$', PermisoDelete.as_view(), name='eliminar'),


	url(r'^listarPermisosCompletos$', ListadoPermisosDocumentacionCompleta.as_view(), name='listarPermisosCompletos'),
	url(r'^detallePermisoCompleto/(?P<pk>\d+)/$', DetallePermisoCompleto.as_view(), name='detallePermisoCompleto'),

	url(r'^listarPermisosPublicados$', ListadoPermisosPublicados.as_view(), name='listarPermisosPublicados'),
	url(r'^detallePermisoPublicado/(?P<pk>\d+)/$', DetallePermisoPublicado.as_view(), name='detallePermisoPublicado'),


]