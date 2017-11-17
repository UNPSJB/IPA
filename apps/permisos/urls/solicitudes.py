from django.conf.urls import url

from ..views.solicitudes import *

app_name = 'solicitudes'
urlpatterns = [
	url(r'^alta$', AltaSolicitud.as_view(), name='alta'),
	url(r'^listar$', ListadoSolicitudes.as_view(), name='listar'),
	url(r'^listar/solicitudes$', ListadoActasSolicitudes.as_view(), name='listarSolicitudes'),
	url(r'^detalle/(?P<pk>\d+)/$', DetalleSolicitud.as_view(), name='detalle'),
	url(r'^detalle/(?P<pk>\d+)/documentos/$', ListadoDocumentacionPresentada.as_view(), name='listarDocumentacionPresentada'),
	url(r'^detalle/(?P<pks>\d+)/documentos/(?P<pkd>\d+)/visar/$', visar_documento_solicitud, name='visarDocumentoSolicitud'),
	url(r'^detalleSolicitud/(?P<pk>\d+)/$', DetalleActasSolicitud.as_view(), name='detalleSolicitud'),
	url(r'^eliminar/(?P<pk>\d+)$', SolicitudDelete.as_view(), name='eliminar'),
]