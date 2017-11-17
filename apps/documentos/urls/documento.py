from django.conf.urls import url

from ..views import *

app_name = 'documentos'

urlpatterns = [
	url(r'^alta/(?P<pk>.+)/$', AltaDocumento.as_view(), name='alta'),
	url(r'^listar$', ListadoDocumentacionPresentada.as_view(), name='listar'),
	url(r'^detalle/(?P<pk>.+)/$', DetalleDocumento.as_view(), name='detalle'),
	url(r'^modificar/(?P<pk>.+)/$', ModificarDocumento.as_view(), name='modificar'),
	url(r'^eliminar/(?P<pk>.+)/$', DeleteDocumento.as_view(), name='eliminar'),

]