from django.conf.urls import url

from ..views.permisos import *

app_name = 'permisos'
urlpatterns = [
	url(r'^listar$', ListadoPermisos.as_view(), name='listar'),
	url(r'^nuevo', AltaPermiso.as_view(), name='alta'),

	url(r'^detalle/(?P<pk>\d+)/$', DetallePermiso.as_view(), name='detalle'),
	url(r'^eliminar/(?P<pk>\d+)/$', PermisoDelete.as_view(), name='eliminar'),


	url(r'^listar/Completos$', ListadoPermisosDocumentacionCompleta.as_view(), name='listarPermisosCompletos'),
	url(r'^detalle/Completo/(?P<pk>\d+)/$', DetallePermisoCompleto.as_view(), name='detallePermisoCompleto'),

	url(r'^listar/Publicados$', ListadoPermisosPublicados.as_view(), name='listarPermisosPublicados'),
	url(r'^detalle/Publicado/(?P<pk>\d+)/$', DetallePermisoPublicado.as_view(), name='detallePermisoPublicado'),

	url(r'^listar/Otorgados$', ListadoPermisosOtorgados.as_view(), name='listarPermisosOtorgados'),
	url(r'^detalle/Otorgado/(?P<pk>\d+)/$', DetallePermisoOtorgado.as_view(), name='detallePermisoOtorgado'),

	url(r'^listar/Baja$', ListadoPermisosDeBaja.as_view(), name='listarPermisosDeBaja'),
	url(r'^detalle/Baja/(?P<pk>\d+)/$', DetallePermisoDeBaja.as_view(), name='detallePermisoDeBaja'),

]