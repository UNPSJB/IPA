from django.conf.urls import url

from ..views import *

app_name = 'documentos'

urlpatterns = [
	url(r'^alta/(?P<pk>.+)/$', AltaDocumento.as_view(), name='alta'),
	url(r'^listar$', ListadoDocumentacionPresentada.as_view(), name='listar'),
	url(r'^detalle/(?P<pk>.+)/$', DetalleDocumento.as_view(), name='detalle'),
	url(r'^modificar/(?P<pk>.+)/$', ModificarDocumento.as_view(), name='modificar'),
	url(r'^eliminar/(?P<pk>.+)/$', DeleteDocumento.as_view(), name='eliminar'),

	url(r'^agregarExpediente/(?P<pk>.+)/$', AgregarExpediente.as_view(), name='agregarExpediente'),
	url(r'^agregarEdicto/(?P<pk>.+)/$', AgregarEdicto.as_view(), name='agregarEdicto'),
	url(r'^agregarOposicion/(?P<pk>.+)/$', AgregarOposicion.as_view(), name='agregarOposicion'),
	url(r'^agregarResolucion/(?P<pk>.+)/$', AgregarResolucion.as_view(), name='agregarResolucion')
	#url(r'^agregarInfraccion/(?P<pk>.+)/$', AgregarInfraccion.as_view(), name='agregarInfraccion'),


]