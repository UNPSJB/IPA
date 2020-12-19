from django.conf.urls import url

from ..views.permisos import *

app_name = 'permisos'
urlpatterns = [
	url(r'^listar$', ListadoPermisos.as_view(), name='listar'),
	url(r'^nuevo', AltaPermiso.as_view(), name='alta'),

	url(r'^detalle/(?P<pk>\d+)/$', DetallePermiso.as_view(), name='detalle'),
	url(r'^detalle/(?P<pk>\d+)/documentos/$', ListadoDocumentacionPermiso.as_view(), name='listarDocumentacionPermiso'),
	url(r'^detalle/(?P<pks>\d+)/documentos/(?P<pkd>\d+)/visar/$', visar_documento_solicitud, name='visarDocumentoSolicitud'),
	url(r'^eliminar/(?P<pk>\d+)/$', PermisoDelete.as_view(), name='eliminar'),

]