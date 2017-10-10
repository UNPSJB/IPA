from django.conf.urls import url

from . import views

app_name = 'permisos'
urlpatterns = [
	#URLS SOLICITUDES
	url(r'^solicitud/alta$', views.AltaSolicitud.as_view(), name='altaSolicitud'),
	url(r'^solicitud/listar$', views.ListadoSolicitudes.as_view(), name='listadoSolicitud'),
	url(r'^solicitud/detalle/(?P<pk>.+)/$', views.DetalleSolicitud.as_view(), name='detalleSolicitud'),
	url(r'^solicitud/eliminar/(?P<pk>\d+)$', views.SolicitudDelete.as_view(), name='deleteSolicitud'),
	
	#URLS PERMISOS
	url(r'^/alta$', views.AltaPermiso.as_view(), name='altaPermiso'),
	url(r'^/listar$', views.ListadoPermisos.as_view(), name='listadoPermiso'),
	url(r'^/detalle/(?P<pk>.+)/$', views.DetallePermiso.as_view(), name='detallePermiso'),
	url(r'^/eliminar/(?P<pk>\d+)$', views.PermisoDelete.as_view(), name='deletePermiso'),
]