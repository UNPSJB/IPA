from django.conf.urls import url

from ..views.solicitudes import *

app_name = 'solicitudes'
urlpatterns = [
	url(r'^alta$', AltaSolicitud.as_view(), name='alta'),
	url(r'^listar$', ListadoSolicitudes.as_view(), name='listar'),
	url(r'^detalle/(?P<pk>.+)/$', DetalleSolicitud.as_view(), name='detalle'),
	url(r'^eliminar/(?P<pk>\d+)$', SolicitudDelete.as_view(), name='eliminar'),
]